import sys
import os
import Settings
import WorkerManager
import FilePathWrapper
import Utils
from WorkerManager import WorkerType
from WorkerManager import WorkerStatus

# Consumer consumes data from a buffer.

#################################################################################################################

# This extends the WorkerManager.Worker class:
class Consumer(WorkerManager.Worker):

    def getInputFile(self):
        args = self.args
        return FilePathWrapper.FilePathWrapper("%s%d"%(args[0], self.manager.runcount))

    #def getPrevInputFile(self):
    #    args = self.args
    #    return FilePathWrapper.FilePathWrapper("%s%d"%(args[0], (self.manager.runcount - 1)))

    def getOutputFile(self):
        args = self.args
        input_fw = self.getInputFile()
        output_fw = args[1]
        return FilePathWrapper.FilePathWrapper("%s/%s"%(str(output_fw), input_fw.getBasename()))


    def getFinalOutputFile(self):
        args = self.args
        input_fw = self.getInputFile()
        output_fw = args[1]
        return FilePathWrapper.FilePathWrapper("%s/%s"%(str(output_fw), input_fw.getBasenameWoutExt(1)))

    #def getPrevOutputFile(self):
    ##    args = self.args
    #    prev_input_fw = self.getPrevInputFile()
    #    output_fw = args[1]
    #    return FilePathWrapper.FilePathWrapper("%s/%s"%(str(output_fw), prev_input_fw.getBasename()))
        

    def work(self, rtargs):
        # Mandatory:
        self.prework()

        # Get static (schedule-time) args:      
        args = self.args
        #
        # Format of static args:
        # [ <input file> , <output file> ]
        #
        # Note: all files are FilePathWrapper encapsulated.

        # Insert your work here
        # ---------------------
        try:
            # Consumer work:
            # (1) Copy <input file> to <output file 'n'>
            # (2) Merge <output file 'n-1'> with <output file 'n'>
            # (3) Delete <input file>
            
            input_fw = self.getInputFile()
            output_fw = args[1]

            s = ""

            # Is there data to consume/does the consumption file exist?
            if input_fw.isExistingFile():
                            
                # (1)            
                if not Utils.runProcess(["cp", "%s"%(str(input_fw)), "%s"%(str(self.getOutputFile()))]):
                    print "Consumer %d: fatal error"%(self.index)
                    self.postwork(WorkerStatus.completed_fatal_error)
               
                s += "Consumer %d copied (consumed) '%s' (%d bytes) to: %s\n"%(self.index, str(input_fw), os.path.getsize(str(input_fw)), str(self.getOutputFile()))

                # (2)            
                if self.manager.runcount > 0:
                    #    $ perl merge.pl <input1> <input2>
                    #    This will join the files, updating <input2> but destroying <input1>
                    if not Utils.runProcess(["perl", "%s"%(Settings.gPerlMerger), "%s"%(str(self.getFinalOutputFile())), "%s"%(str(self.getOutputFile()))]):
                        print "Consumer %d: fatal error"%(self.index)
                        self.postwork(WorkerStatus.completed_fatal_error)
                 
                if not Utils.runProcess(["mv", "%s"%(str(self.getOutputFile())), "%s"%(str(self.getFinalOutputFile()))]):
                    print "Consumer %d: fatal error"%(self.index)
                    self.postwork(WorkerStatus.completed_fatal_error)
                    
                # (3)
                if not Utils.runProcess(["rm", "-rf", "%s"%(str(input_fw))]):
                    print "Consumer %d: fatal error"%(self.index)
                    self.postwork(WorkerStatus.completed_fatal_error)

            else:
                # IT IS POSSIBLE TO REACH HERE
               # print "Consumer %d: nothing to consume (expecting: %s)"%(self.index, str(input_fw))
                print "Consumer %d: nothing to consume"%(self.index)
                self.postwork(WorkerStatus.completed_general_failure)

        except OSError, IndexError:
            self.postwork(WorkerStatus.completed_fatal_error)

        print s

        # Mandatory:   
        self.postwork(WorkerStatus.completed_success) 
               
    def __init__(self):
        # Invoke the super (WorkerManager.Worker) class constructor:
        super(Consumer, self).__init__()
        
#################################################################################################################

# This extends the WorkerManager.WorkerManager class:
class ConsumerManager(WorkerManager.WorkerManager):

    # 'argslist' goes like this:
    # [
    #   [ <input file prefix> , <output dir> ] ,            <--- for worker 0
    #   [ <input file prefix> , <output dir> ] ,            <--- for worker 1
    #   etc.                                                etc.
    # ]
    # 
    # Note: only <output dir> is FilePathWrapper encapsulated.
    def __init__(self, argslist): 

        # Invoke the super (WorkerManager.WorkerManager) class constructor:
        super(ConsumerManager, self).__init__(Settings.gWorkerType)
        for args in argslist:
            # Create a worker:
            consumer = Consumer()
            # Schedule the worker with its work function and args:
            self.scheduleWorker(consumer, consumer.work, args)   
            


    def run(self):

        # Start the workers:
        self.startWorkers()

        # Join the workers (blocking):
        if not self.joinWorkers():
            if self.haveFatalError():
                raise AssertionError("At least one worker suffered a fatal error!")

        print self.getDuration()


   
