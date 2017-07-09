#! /usr/bin/python3

from VenC.threads.thread import Thread

class Main(Thread):
    def __init__(self, prompt, datastore):
        super().__init__(prompt, datastore)
        self.OrganizeEntries([
            entry for entry in datastore.GetEntries(
                datastore.blogConfiguration["reverseThreadOrder"]
            )
        ])

        self.SetupProcessor()

    def GetRelativeOrigin(self):
        return str()
