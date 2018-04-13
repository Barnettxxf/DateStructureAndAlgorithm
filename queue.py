# -*- coding: utf-8 -*-
from DateStructureAndAlgorithm.stack import SStack

__author__ = 'barnett'


class QueueUnderflow(ValueError):
    pass


class SQueue(object):
    """ based on simple list """

    def __init__(self, init_len=8):
        self._len = init_len
        self._elems = [0] * init_len
        self._head = 0
        self._num = 0

    def is_empty(self):
        return self._num == 0

    def peek(self):
        if self.is_empty():
            raise QueueUnderflow('in SQueue.peek')
        return self._elems[self._head]

    def dequeue(self):
        if self.is_empty():
            raise QueueUnderflow('in SQueue.dequeue')
        e = self._elems[self._head]
        self._head = (self._head + 1) % self._len
        self._num -= 1
        return e

    def enqueue(self, e):
        if self.is_empty():
            self.__extand()
        self._elems[(self._head + self._num) % self._num] = e
        self._num += 1

    def __extand(self):
        old_len = self._len
        self._len *= 2
        new_elems = [0] * self._len
        for i in range(old_len):
            new_elems[i] = self._elems[(self._head + i) % old_len]
        self._elems, self._head = new_elems, 0


""" Maze problem """

dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def mark(maze, pos):
    maze[pos[0]][pos[1]] = 2


def passable(maze, pos):
    return maze[pos[0]][pos[1]] == 0


def find_path(maze, pos, end):
    """ Recursion solution, based on stack """
    mark(maze, pos)
    if pos == end:
        return True
    for i in range(4):
        nextp = pos[0] + dirs[i][0], pos[0] + dirs[i][1]

        if passable(maze, nextp):
            if find_path(maze, nextp, end):
                return True
    return False


def maze_solver(maze, start, end):
    """ Backtracking solution , based on stack"""
    if start == end:
        print(start)
        return True
    st = SStack()
    mark(maze, start)
    st.push((start, 0))
    while not st.is_empty():
        pos, nxt = st.pop()
        for i in range(nxt, 4):
            nextp = pos[0] + dirs[i][0], pos[1] + dirs[i][1]
            if nextp == end:
                return True
            if passable(maze, nextp):
                st.push((pos, i + 1))
                mark(maze, nextp)
                st.push((nextp, 0))
                break
    print('No path found.')


def maze_solve_queue(maze, start, end):
    """ based on queue """
    if start == end:
        return True
    qu = SQueue()
    mark(maze, start)
    qu.enqueue(start)
    while not qu.is_empty():
        pos = qu.dequeue()
        for i in range(4):
            nextp = (pos[0] + dirs[i][0], pos[1] + dirs[i][1])
            if passable(maze, nextp):
                if nextp == end:
                    return True
                mark(maze, nextp)
                qu.enqueue(nextp)
    print('No path found.')


class PrioQueueError(ValueError):
    pass


class PriorityQueue(object):
    def __init__(self, elist=list()):
        self._elems = list(elist)
        self._elems.sort(reverse=True)

    def is_empty(self):
        return len(self._elems) == 0

    def enqueue(self, e):
        i = len(self._elems) - 1
        while i >= 0 :
            if self._elems[i] <= e:
                i -= 1
            else:
                break
        self._elems.insert(i+1, e)

    def peek(self):
        if self.is_empty():
            raise PrioQueueError()
        return self._elems[-1]

    def dequeue(self):
        if self.is_empty():
            raise PrioQueueError()
        return self._elems.pop()