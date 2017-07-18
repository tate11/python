#!/usr/bin/python

import random
import sys
import os
import WorkerManager
from WorkerManager import WorkerType
from WorkerManager import WorkerStatus

#################################################################################################################

adjectives = ["Rabid",
              "Crispy",
              "Insolent",
              "Intrepid",
              "Luminous",
              "Opaque",
              "Turgid",
              "Kinky",
              "Kinetic",
              "Caustic",
              "Noxious",
              "Languid",
              "Obtuse",
              "Poxy",
              "Pernicious",
              "Seismic",
              "Chromium",
              "Majestic",
              "Nebulous",
              "Scurrilous",
              "Neurotic",
              "Disruptive",
              "Prickly",
              "Nostalgic",
              "Bearded",
              "Husky"]

nouns = ["Smelter",
         "Acorn",
         "Reindeer",
         "Mushroom",
         "Megawatt",
         "Viper",
         "Follicle",
         "Coccyx",
         "Amethyst",
         "Mandrill",
         "Barrister",
         "Homunculus",
         "Turbin",
         "Falcon",
         "Shank",
         "Carrot", 
         "Governor",
         "Baron",
         "Nightshade",
         "Manatee",
         "Fandangle",
         "Pickle",
         "Bishop",
         "Replicant",
         "Whiskey",
         "Popsicle"]


#################################################################################################################

# This extends the WorkerManager.Worker class:
class MyWorker(WorkerManager.Worker):

    # 'rtargs' : run-time args (as opposed to the static args specified at schedule-time)
    def work(self, rtargs):
        # Mandatory:
        self.prework()

        # Insert your work here:
        print "%s (%d of %d): %d"%(self.identity, (self.index + 1), len(self.manager.workers), self.args[0])

        # Mandatory:   
        self.postwork(WorkerStatus.completed_success) 
               
    def __init__(self, identity):
        # Invoke the super (WorkerManager.Worker) class constructor:
        super(MyWorker, self).__init__()
        self.identity = identity
        
#################################################################################################################

# This extends the WorkerManager.WorkerManager class:
class MyWorkerManager(WorkerManager.WorkerManager):

    def __init__(self, seed, workercount, workertype):
        # Invoke the super (WorkerManager.WorkerManager) class constructor:
        super(MyWorkerManager, self).__init__(workertype)
      
        random.seed(seed)

        for i in range(0, workercount):
            noun = nouns[random.randint(0, (len(nouns) - 1))]
            adjective = adjectives[random.randint(0, (len(adjectives) - 1))]

            # Create a worker:
            myworker = MyWorker((adjective + noun))

            # Schedule the worker with its work function and static args:
            args = [random.randint(0,100)]
            self.scheduleWorker(myworker, myworker.work, args)



    def run(self):

        # Start the workers:
        self.startWorkers()

        # Join the workers:
        if not self.joinWorkers():
            raise AssertionError("Not all workers have completed without error.")

        return self.getDuration()


#################################################################################################################

if __name__ == "__main__":

    if (len(sys.argv) > 1):
        try:
            seed = int(sys.argv[1])
        except ValueError:
            print "Please specify integer! This is invalid: %s"%(sys.argv[1])
            exit(-1)
    else:
        seed = 0

    myworkermanager1 = MyWorkerManager(seed, 10, WorkerType.thread)
    myworkermanager2 = MyWorkerManager(seed, 10, WorkerType.process)


    for i in range(0, 5):
        print"\nTHREAD WORKERS:"
        duration = myworkermanager1.run()
        print "DURATION: %f"%(duration)
        print "\nPROCESS WORKERS:"
        duration = myworkermanager2.run()
        print "DURATION: %f"%(duration)
        print ""   
        print "------------------"





