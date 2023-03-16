class EventBroadcast():
    """Allows for functions to be called when certain events happens"""

    def __init__(self):
        self.validEvent = []
        self.eventManager = None
    
    def addListener(self, func, event, owner):
        """Execute the function func when event is realised passing a tuple of args as parameter"""
        if event not in self.validEvent :
            raise AssertionError("Error : invalid event")
        if self.eventManager == None :
            self.eventManager = {event : [] for event in self.validEvent}
        self.eventManager[event].append((func, owner))

    def removeListener(self, func, event, owner):
        """Undo addListener"""
        if event not in self.validEvent :
            raise AssertionError("Error : invalid event")
        if self.eventManager != None :
            for elem in self.eventManager[event] :
                if elem == (func, owner):
                    self.eventManager[event].remove(elem)
                    return
        print("WARNING : no such event function\n", f"func {str(func)} of {str(owner)}", sep="")

    def eventList(self):
        """List all possibles events for this class, should only be used for documentation"""
        return str(self.validEvent)
    
    def _eventTrigger(self, event, args):
        if event not in self.validEvent :
            raise AssertionError("Error : invalid event", event)
        if self.eventManager != None :
            for func, owner in self.eventManager[event]:
                func(args)

        