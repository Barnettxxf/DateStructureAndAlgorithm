# -*- coding: utf-8 -*-
from DateStructureAndAlgorithm.queue import PrioQueueError, SQueue
from DateStructureAndAlgorithm.stack import SStack

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


class BinTNode(object):
    def __init__(self, dat, left=None, right=None):
        self.data = dat
        self.left = left
        self.right = right


class BinTree(object):
    def __init__(self):
        self._root = None

    def is_empty(self):
        return self._root is None

    def root(self):
        return self._root

    def leftchild(self):
        return self._root.left

    def rigthchile(self):
        return self._root.right

    def set_root(self, rootnode):
        self._root = rootnode

    def sef_left(self, leftchild):
        self._root.left = leftchild

    def set_right(self, rightchild):
        self._root.right = rightchild

    def preorder_elements(self):
        t, s = self._root, SStack()
        while t is not None or not s.is_empty():
            while t is not None:
                s.push(t.right)
                yield t.data
                t = t.left
            t = s.pop()


def counts(t):
    """ count bintree nodes """
    if t is None:
        return 0
    else:
        return 1 + counts(t.left) + counts(t.right)


def sum(t):
    """ sum all values in bintree """
    if t is None:
        return 0
    else:
        return t.data + sum(t.left) + sum(t.right)


def preorder(t, proc):
    if not callable(proc):
        raise ValueError('proc must be a function')

    if t is None:
        return
    proc(t.data)
    preorder(t.left, proc)
    preorder(t.right, proc)


def preorder_nonrec(t, proc):
    if not callable(proc):
        raise ValueError('proc must be a function')

    s = SStack()
    while t is not None and not s.is_empty():
        while t is not None:
            proc(t.data)
            if t.right is not None:
                s.push(t.right)
            t = t.left
        t = s.pop()


def postorder_nonrec(t, proc):
    if not callable(proc):
        raise ValueError('proc must be a function')

    s = SStack()
    while t is not None or not s.is_empty():
        while t is not None:
            s.push(t)
            t = t.left if t.left is not None else t.right

        t = s.pop()
        proc(t.data)
        if not s.is_empty() and s.top().left == t:
            t = s.top().right
        else:
            t = None


def print_bintree(t):
    if t is None:
        print('^', end='')
        return
    print('(' + str(t.data), end='')
    print_bintree(t.left)
    print_bintree(t.right)
    print(')', end='')


def levelorder(t, proc):
    if not callable(proc):
        raise ValueError('proc must be a function')

    qu = SQueue()
    qu.enqueue(t)
    while not qu.is_empty():
        n = qu.dequeue()
        if n is not None:
            continue
        qu.enqueue(t.left)
        qu.enqueue(t.right)
        proc(t.data)


if __name__ == '__main__':
    t = BinTNode(1, BinTNode(2, BinTNode(5)), BinTNode(3))
    print_bintree(t)
