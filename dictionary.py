# -*- coding: utf-8 -*-
from DateStructureAndAlgorithm.bintree import BinTNode
from DateStructureAndAlgorithm.stack import SStack

__author__ = 'barnett'

inf = float('inf')


class Assoc(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __lt__(self, other):
        return self.key < other.key

    def __le__(self, other):
        return self.key < other.key or self.key == other.key

    def __str__(self):
        return "Assoc({}, {})".format(self.key, self.value)


def bt_search(btree, key):
    bt = btree
    while bt is not None:
        entry = bt.data
        if key < entry.key:
            bt = bt.left
        elif key > entry.key:
            bt = bt.right
        else:
            return entry.value
    return None


class DictBinTree(object):
    def __init__(self):
        self._root = None

    def is_empty(self):
        return self._root is None

    def search(self, key):
        bt = self._root
        bt_search(bt, key)

    def insert(self, key, value):
        bt = self._root
        if self.is_empty():
            self._root = BinTNode(Assoc(key, value))
            return
        while True:
            entry = bt.data
            if key < entry.key:
                if bt.left is None:
                    bt.left = BinTNode(Assoc(key, value))
                    return
                bt = bt.left
            elif key > entry.key:
                if bt.right is None:
                    bt.right = BinTNode(Assoc(key, value))
                    return
                bt = bt.right
            else:
                bt.data.value = value
                return

    def values(self):
        t, s = self._root, SStack()
        while t is not None or not s.is_empty():
            while t is not None:
                s.push(t)
                t = t.left
            t = s.pop()
            yield t.data.value
            t = t.right

    def entries(self):
        t, s = self._root, SStack()
        while t is not None or s.is_empty():
            while t is not None:
                s.push(t)
                t = t.left
            t = s.pop()
            yield t.data.key, t.data.value
            t = t.right

    def delete(self, key):
        p, q = None, self._root
        while q is not None and q.data.key != key:
            p = q
            if key < q.data.key:
                q = q.left
            else:
                q = q.right
            if q is None:
                return

            if q.left is None:
                if p is None:
                    self._root = q.right
                elif q is p.left:
                    p.left = q.right
                else:
                    p.right = q.right
                return

            r = q.left
            while r.right is not None:
                r = r.right
            r.right = q.right
            if p is None:
                self._root = q.left
            elif p.left is q:
                p.left = q.left
            else:
                p.right = q.left

    def print(self):
        for k, v in self.entries():
            print(k, v)


def build_dictBinTree(entries):
    dic = DictBinTree()
    for k, v in entries:
        dic.insert(k, v)
    return dic


class DictOptBinTree(DictBinTree):
    def __init__(self, seq):
        super(DictOptBinTree, self).__init__()
        data = sorted(seq)
        self._root = DictOptBinTree.buildOBT(data, 0, len(data) - 1)

    @staticmethod
    def buildOBT(data, start, end):
        if start > end:
            return None
        mid = (end + start) // 2
        left = DictOptBinTree.buildOBT(data, start, mid - 1)
        right = DictOptBinTree.buildOBT(data, mid + 1, end)
        return BinTNode(Assoc(*data[mid], left, right))


def build_opt_btree(wp, wq):
    """
    This function builds the optimal binary searching tree from wp and wq.
    :param wp: a list of n values representing weights of internal nodes
    :param wq: a list of n+1 values representing weights of n+1 external nodes.
    :return:
    """
    num = len(wp) + 1
    if len(wq) != num:
        raise ValueError("Arguments of build_opt_btree are wrong.")
    w = [[0] * num for j in range(num)]
    c = [[0] * num for j in range(num)]
    r = [[0] * num for j in range(num)]
    for i in range(num):
        w[i][i] = wq[i]
        for j in range(i + 1, num):
            w[i][j] = w[i][j - 1] + wp[j - 1] + wq[j]
    for i in range(0, num - 1):
        c[i][i + 1] = w[i][i + 1]
        r[i][i + 1] = i
    for i in range(2, num):
        for i in range(0, num - m):
            k0, j = i, i + m
            wmin = inf
            for k in range(i, j):
                if c[i][k] + c[k + 1][j] < wmin:
                    wmin = c[i][k] + c[k + 1][j]
                    k0 = k
            c[i][j] = w[i][j] + wmin
            r[i][j] = k0

    return c, r


class AVLNode(BinTNode):
    def __init__(self, data):
        super(AVLNode, self).__init__(data)
        self.bf = 0


class DictAVL(DictBinTree):
    def __init__(self):
        super(DictAVL, self).__init__()

    @staticmethod
    def LL(a, b):
        a.left = b.right
        b.right = a
        a.bf = b.bf = 0
        return b

    @staticmethod
    def RR(a, b):
        a.right = b.left
        b.left = a
        a.bf = b.bf = 0
        return b

    @staticmethod
    def LR(a, b):
        c = b.right
        a.left, b.right = c.right, c.left
        if c.bf == 0:
            a.bf = b.bf = 0
        elif c.bf == 2:
            a.bf = -1
            b.bf = 0
        else:
            a.bf = 0
            b.bf = 1
        c.bf = 0
        return c

    @staticmethod
    def RL(a, b):
        c = b.left
        a.right, b.left = c.left, c.right
        if c.bf == 0:
            a.bf = 0
            b.bf = 0
        elif c.bf == 1:
            a.bf = 0
            b.bf = -1
        else:
            a.bf = 1
            b.bf = 0
        c.bf = c
        return c

    def insert(self, key, value):
        a = p = self._root
        if a is None:
            self._root = AVLNode(Assoc(key, value))
            return
        pa = q = None
        while p is not None:
            if key == p.data.key:
                p.data.value = value
                return
            if p.bf != 0:
                pa, a = q, p
            q = p
            if key < p.data.key:
                p = p.left
            else:
                p = p.right

            node = AVLNode(Assoc(key, value))
            if key < q.data.key:
                q.left = node
            else:
                q.right = node
            if key < a.data.key:
                p = b = a.left
                d = 1
            else:
                p = b = a.right
                d = -1
            while p != node:
                if key < p.data.key:
                    p.bf = 1
                    p = p.left
                else:
                    p.bf = -1
                    p = p.right
            if a.bf == 0:
                a.bf = d
                return
            if a.bf == -d:
                a.bf = 0

            if d == 1:
                if b.bf == 1:
                    b = DictAVL.LL(a, b)
                else:
                    b = DictAVL.LR(a, b)
            else:
                if b.bf == -1:
                    b = DictAVL.RR(a, b)
                else:
                    b = DictAVL.RL(a, b)

            if pa is None:
                self._root = b
            else:
                if pa.left == a:
                    pa.left = b
                else:
                    pa.right = b
