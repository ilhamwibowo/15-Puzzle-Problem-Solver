class priorityQueue:
    def __init__(self):
        self.queue = []
 
    def push(self, node):
        self.queue.append(node)
 
    def pop(self):
        minidx = 0
        for i in range(len(self.queue)): #ambil cost
            if (self.queue[i].cost < self.queue[minidx].cost):
                minidx = i
        min = self.queue[minidx]
        del self.queue[minidx]
        return min
 
    def empty(self):
        if not self.queue:
            return True
        else:
            return False
    def printqueuecost(self):
        for i in range(len(self.queue)):
            print(self.queue[i].cost, end=" ")
        print()