import threading
import multiprocessing
import time
from enum import Enum

#################################################################################################################
#
# WorkerManager:
#
# A useful bunch of Python code that wraps around multi threaded/process 'dumb worker' functionality.
# By 'dumb workers', we mean a bunch of workers that go off and do something individually at the same
# time under the direction of the WorkManager. At this stage, the only thing that the workers return is
# a success/failure flag. There is provision for threaded workers to return actual output worker data back
# to the WorkManager: however, this code is currently commented out (see below). 
#
# Remember that for workers that are spawned as processes, they will have their own copy of program-state
# memory that if changed (eg. you update a variable) will NOT be reflected back in the parent (spawning)
# process. What does this mean exactly? Essentially, if you are a worker spawned as a process, it is best NOT 
# to access 'self.manager' in your worker code because you will be accessing copies, not the original!
#
#################################################################################################################

class WorkerStatus(Enum):
    not_started = 0                     # My work has not started.
    started = 1                         # My work is in progress...
    completed_fatal_error = 2           # My work was compromised by fatal errors!
    completed_non_fatal_error = 3       # My work was compromised by non-fatal errors!
    completed_not_successful = 4        # My work was unsuccessful (but no errors)!
    completed_success = 5               # My work was successful!

#################################################################################################################

class WorkerType(Enum):
    thread = 0
    process = 1    

#################################################################################################################

# EXTEND ME
class Worker(object):
    # Workers maintain reference to:
    #
    # - self.manager (the WorkerManager instance that this Worker instance is managed by)
    #
    # If your worker is a process, these will be COPIES of the original, therefore
    # BACKWARDS PROPAGATION of data will NOT work (eg. passing the output of work 
    # back to the manager).

    def __init__(self, manager=None):
        super(Worker, self).__init__()
        self.manager = manager
        self.status = WorkerStatus.not_started
        # Output data (for thread workers only!):
        #self.outdata = None                     

    # Must be called at the beginning of your work function.
    def prework(self):
        self.status = WorkerStatus.started

    # Must be called at the end of your work function.
    def postwork(self, status=WorkerStatus.completed_success): 
        if self.type == WorkerType.process:
            # Processes have to use an exit code in order to backpropagate a status value.
            exit(status.value)
        else:
            self.status = status

    # 'rtargs' : run-time args (as opposed to the static args specified at schedule-time)
    def start(self, rtargs=None):
        # Process worker:
        if self.type == WorkerType.process:
            self.worker = multiprocessing.Process(target=self.workfunc, args=(rtargs,))
        # Thread worker:
        else:
            self.worker = threading.Thread(target=self.workfunc, args=(rtargs,))
        self.starttime = time.time()
        # Launch/spawn new process/thread:
        self.worker.start()


    def join(self):
        # Block on completion of process/thread:
        self.worker.join()
        self.endtime = time.time()
        # Processes use an exit code in order to backpropagate a status value.
        if self.type == WorkerType.process:
            self.status = WorkerStatus(self.worker.exitcode)      #  <--------------------------       FIX ME CHECK - process error codes ???? !!!!

#################################################################################################################

# EXTEND ME
class WorkerManager(object):

    # IN: workertype : thread | process
    def __init__(self, workertype=WorkerType.thread):
        super(WorkerManager, self).__init__()
        self.workertype = workertype
        self.reset()
        # For thread workers only: 
        #self.workeroutdata = {}

    def __len__(self):
        return len(self.workers)

    def __iter__(self):
        return iter(self.workers)

    def reset(self):
        self.workers = []
        self.starttime = 0
        self.endtime = 0
        self.runcount = 0


    def scheduleWorker(self, worker, workfunc, args=None):
        worker.manager = self 
        worker.index = len(self)
        worker.type = self.workertype
        worker.workfunc = workfunc
        worker.args = args
        self.workers.append(worker)


    # 'rtargs' : run-time args (as opposed to the static args specified at schedule-time)
    def startWorkers(self, rtargs=None):     
        self.starttime = time.time()
        map(lambda worker: worker.start(rtargs), self.workers)
        
    def joinWorkers(self):
        map(lambda worker: worker.join(), self.workers)
        self.endtime = time.time()
        self.runcount += 1
        return self.haveCompletedNoErrors()

    # There was at least one worker that suffered a fatal error attempting to do work.
    # This allows your WorkerManager to terminate gracefully.
    def haveFatalError(self):
        for worker in self:
            if worker.status == WorkerStatus.completed_fatal_error:
                return True
        return False


    # Have all workers completed with no errors?
    def haveCompletedNoErrors(self):
        for worker in self:
            if not ((worker.status == WorkerStatus.completed_success) or
                    (worker.status == WorkerStatus.completed_not_successful)):
                return False
        return True

    # All workers completed successfully.
    def haveCompletedSuccess(self):
        for worker in self:
            if worker.status != WorkerStatus.completed_success:
                return False
        return True

    def getDuration(self):
        return (self.endtime - self.starttime)


