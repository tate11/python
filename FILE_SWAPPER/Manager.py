import sys
import os
import WorkerManager
from WorkerManager import WorkerType
from WorkerManager import WorkerStatus

#################################################################################################################

# This extends the WorkerManager.Worker class:
class MultiWorker(WorkerManager.Worker):

    def work(self, args):
        # Do some work:
        print "%s (%d of %d): %d"%(self.identity, (self.index + 1), self.creator.workercount, args[0])

        # Finish work:   
        self.finish(WorkerStatus.completed_success) 
               
    def __init__(self, creator, identity):
        # Invoke the super (WorkerManager.Worker) class constructor:
        super(MultiWorker, self).__init__(creator)
        self.identity = identity
        
#################################################################################################################

class Manager(object):

    def __init__(self, seed, workercount, workertype):
        random.seed(seed)
        self.workercount = workercount

        # Create a WorkerManager:
        self.workermanager = WorkerManager.WorkerManager(workertype) 

    def run(self):
        for i in range(0, self.workercount):
            noun = nouns[random.randint(0, (len(nouns) - 1))]
            adjective = adjectives[random.randint(0, (len(adjectives) - 1))]

            # Create a worker:
            multiworker = MultiWorker(self, (adjective + noun))

            args = [random.randint(0,100)]

            # Schedule the worker:
            self.workermanager.scheduleWorker(multiworker, multiworker.work, args)   

        # Start the workers:
        self.workermanager.startWorkers()

        # Join the workers:
        if not self.workermanager.joinWorkers():
            raise AssertionError("Not all workers have completed succesfully!")

        return self.workermanager.duration

