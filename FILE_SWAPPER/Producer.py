import sys
import os
import Settings
import WorkerManager
import FilePathWrapper
import Utils
from WorkerManager import WorkerType
from WorkerManager import WorkerStatus

# Producer produces data for a buffer.

#################################################################################################################

# This extends the WorkerManager.Worker class:
class Producer(WorkerManager.Worker):

    # A worker is eligible if its input file exists.
    def isEligibleWorker(self):
        try:
            fw = self.args[0]
            return fw.isExistingFile()
        except IndexError:
            return False

    def getOutputFilePrefix(self):
        # Get static (schedule-time) args:
        args = self.args
        try:
            fw = args[0]
            outfileprefix = "%s/%s.%s"%(args[1], fw.getBasename(), Settings.gPartExt)
            return outfileprefix
        except IndexError:
            return None

    def getOutputFile(self):
        return FilePathWrapper.FilePathWrapper("%s%d"%(self.getOutputFilePrefix(), self.manager.runcount))


    def work(self, rtargs):
        # Mandatory:
        self.prework()

        # Get static (schedule-time) args:
        args = self.args

        # Insert your work here
        # ---------------------
        try:
            inputfile = str(args[0])
            outfile = self.getOutputFile()
            buffersize = args[2] # In MB         

            s = ""
        
            # Are we currently eligible to work?
            if self.isEligibleWorker():

                # Are we waiting on a consumer (have we already produced)?
                if not outfile.isExistingFile():

                    eligibleWorkerCount = self.manager.getEligibleWorkerCount()
                    assert(eligibleWorkerCount > 0)

                    # Work out this worker's buffer size.
                    # Eg. if the total buffer size is 10MB, and there are 2 eligible workers,
                    # then this worker's buffer allocation is 5MB.
                    buffersize = buffersize / eligibleWorkerCount
                    assert(buffersize > 0)

                    # Convert from MB -> bytes
                    buffersize = Utils.MBtoBytes(buffersize)

                    size = os.path.getsize(inputfile)
                    bs = Settings.gBS
                 
                    assert((buffersize % bs) == 0)
      
                    skip = 0
                    count = Utils.getRequiredBlockCount(size, bs)   
                   # s += "Producer %d requires %d blocks for %s (%d bytes)\n"%(self.index, count, inputfile, size)       
                    if size > buffersize:
                        #skip = (size - buffersize) / bs
                        skip = Utils.getRequiredBlockCount((size - buffersize), bs)
                        count = buffersize / bs

                   # s += "Producer %d running 'dd' with: skip=%d, bs=%d, count=%d\n"%(self.index, skip, bs, count) 

                    # Use 'dd' to copy (bs * count) bytes from END of input to output:
                    # dd if=<inputfile> of=<outputfile> skip=<skip> bs=<bs> count=<count>     <--- using a blocksize of 1, results in a SLOW SPEED
                    #                                                                              hence convert to blocksize 4096
                    if not Utils.runProcess(["dd", "if=%s"%(inputfile), "of=%s"%(str(outfile)), "skip=%d"%(skip), "bs=%d"%(bs), "count=%d"%(count)]):
                        print "Producer %d: fatal error"%(self.index)
                        self.postwork(WorkerStatus.completed_fatal_error)

                    s += "Producer %d produced: %s (%d bytes)\n"%(self.index, str(outfile), os.path.getsize(str(outfile))) 

                    # Use 'truncate' to truncate the input file (from its end)... remember the value you pass to truncate is what it will be truncated to!
                    outsize = os.path.getsize(str(outfile))
                    insize = os.path.getsize(inputfile)
                    if (outsize >= insize):
                        cmd_list = ["rm", "-rf", "%s"%(inputfile)]
                    else:
                        cmd_list = ["truncate", "-s", "%d"%(insize - outsize), "%s"%(inputfile)]

                   # s += "Producer %d truncating '%s' by %d bytes\n"%(self.index, inputfile, outsize) 
       
                    if not Utils.runProcess(cmd_list):
                        print "Producer %d: fatal error"%(self.index)
                        self.postwork(WorkerStatus.completed_fatal_error)

                else:
                    # PROBABLY SHOULD NOT EVER GET HERE (YOUR MULTI-THREAD SYNC LOGIC IS INCORRECT)
                    print "Producer %d has already produced: %s"%(self.index, str(outfile))
                    self.postwork(WorkerStatus.completed_general_failure)

            else:
                # IT IS POSSIBLE TO REACH HERE
                print "Producer %d: nothing to produce"%(self.index)
                self.postwork(WorkerStatus.completed_general_failure)
                    
        #except IndexError:
        #except OSError:
        #except AssertionError:
        except:
            self.postwork(WorkerStatus.completed_fatal_error)

        print s

        # Mandatory:   
        self.postwork(WorkerStatus.completed_success) 
               
    def __init__(self):
        # Invoke the super (WorkerManager.Worker) class constructor:
        super(Producer, self).__init__()
        
#################################################################################################################

# This extends the WorkerManager.WorkerManager class:
class ProducerManager(WorkerManager.WorkerManager):

    def getEligibleWorkerCount(self):
        count = 0
        for worker in self.workers:
            if worker.isEligibleWorker():
                count += 1
        return count

    def hasWork(self):
        if self.getEligibleWorkerCount() > 0:
            return True
        return False


    # IN: 'inputfiles' : a list of FilePathWrapper objects encapsulating the input files to "produce" data from
    # IN: 'outfile' : buffer swap space directory destination (eg. "/mnt/ramfs/buffer/")
    # IN: 'buffersize' : total buffer swap space size (in MB)
    def __init__(self, inputfiles, outfile, buffersize): 

        # Invoke the super (WorkerManager.WorkerManager) class constructor:
        super(ProducerManager, self).__init__(Settings.gWorkerType)
        self.inputfiles = inputfiles

        for inputfile in self.inputfiles:
            # Create a worker:
            producer = Producer()
            # Schedule the worker with its work function and args:
            args = [inputfile, outfile, buffersize]
            self.scheduleWorker(producer, producer.work, args)   

    
    def run(self):

        # Start the workers:
        self.startWorkers()

        # Join the workers (blocking):
        if not self.joinWorkers():
            if self.haveFatalError():
                raise AssertionError("At least one worker suffered a fatal error!")

        print self.getDuration()


    # Retrieves a list of FilePathWrapper(input files) to present to consumer manager:
    def getConsumerInputs(self):
        infiles = []
        map(lambda worker: infiles.append(worker.getOutputFilePrefix()), self.workers)
        return list(reversed(infiles))

    # Retrieves a list of FilePathWrapper(output dirs) to present to consumer manager:
    def getConsumerOutputs(self):
        outdirs = []
        for fw in self.inputfiles:
            outdirs.append(fw.getLeadingPathAsWrapper())
        return outdirs

    # Retrieves a list of args to present to an instance of a consumer manager:
    def getConsumerArgs(self):
        args = []
        infiles = self.getConsumerInputs()
        outdirs = self.getConsumerOutputs()
        i = 0
        for inputfile in self.inputfiles:
            args.append([infiles[i], outdirs[i]])
            i += 1 
        return args




