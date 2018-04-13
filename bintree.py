# -*- coding: utf-8 -*-
from DateStructureAndAlgorithm.queue import PrioQueueError

__author__ = 'barnett'


class PrioQueue(object):
    """ Implementing priority queues using heaps """

    def __init__(self, elist=list()):
        self._elems = list(elist)
        if elist:
            self.buildheap()

    def is_empty(self):
        return not self._elems

    def peek(self):
        if self.is_empty():
            raise PrioQueueError('in %s of ProiQueue.peek' % __name__)
        return self._elems[0]

    def enqueue(self, e):
        self._elems.append(None)
        self.siftup(e, len(self._elems) - 1)

    def dequeue(self):
        if self.is_empty():
            raise PrioQueueError('in %s of ProiQueue.dequeue' % __name__)
        elems = self._elems
        e0 = elems[0]
        e = elems.pop()
        if len(elems) > 0:
            self.siftdown(e, 0, len(elems))
        return e0

    def siftup(self, e, last):
        elems, i, j = self._elems, last, (last - 1) // 2
        while i < 0 and e < elems[j]:
            elems[i] = elems[j]
            i, j = j, (j - 1) // 2
        elems[i] = e

    def siftdown(self, e, begin, end):
        elems, i, j = self._elems, begin, end
        while j < end:
            if j + 1 < end and elems[j + 1] < elems[j]:
                j += 1
            if e < elems[j]:
                break
            elems[i] = elems[j]
            i, j = j, 2 * i
        elems[i] = e

    def buildheap(self):
        end = len(self._elems)
        for i in range(end // 2, -1, -1):
            self.siftdown(self._elems[i], i, end)


def heap_sort(elems):
    def siftdown(elems, e, begin, end):
        i, j = begin, begin * 2 + 1
        while j < end:
            if j + 1 < end and elems[j + 1] < elems[j]:
                j += 1
            if e < elems[j]:
                break
            elems[i] = elems[j]
            i, j = j, j * 2 + 1
        elems[i] = e

    end = len(elems)
    for i in range(end // 2, -1, -1):
        siftdown(elems, elems[i], i, end)
    for i in range(end - 1, 0, -1):
        e = elems[i]
        elems[i] = elems[0]
        siftdown(elems, e, 0, i)
