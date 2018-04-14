# -*- coding: utf-8 -*-
from DateStructureAndAlgorithm.bintree import PrioQueue
from DateStructureAndAlgorithm.stack import SStack

__author__ = 'barnett'


class GraphError(Exception):
    pass


class Graph(object):
    def __init__(self, mat, unconn=0):
        vnum = len(mat)
        for x in mat:
            if len(x) != vnum:
                raise ValueError('Agument for Graph.')
        self._mat = [mat[i][:] for i in range(vnum)]
        self._unconn = unconn
        self._vnum = vnum

    def vertex_num(self):
        return self._vnum

    def _invalid(self, v):
        return 0 > v or v >= self._vnum

    def add_vertex(self):
        raise GraphError('Adj-Matrix doex not support "add_vertex"')

    def add_edge(self, vi, vj, val=1):
        if self._invalid(vi) or self._invalid(vj):
            raise GraphError(str(vi) or str(vj) + " is not a valid vertex")
        self._mat[vi][vj] = val

    def get_edge(self, vi, vj):
        if self._invalid(vi) or self._invalid(vj):
            raise GraphError(str(vi) or str(vj) + " is not a valid vertex")

        return self._mat[vi][vj]

    def out_edge(self, vi):
        if self._invalid(vi):
            raise GraphError(str(vi) + " is not a valid vertex.")
        return self._out_edge(self._mat[vi], self._unconn)

    @staticmethod
    def _out_edge(row, unconn):
        edges = []
        for i in range(len(row)):
            if row[i] != unconn:
                edges.append((i, row[i]))
        return edges

    def __str__(self):
        return "[\n" ",\n".join(map(str, self._mat)) + "\n]" + "\nUnconnected: " + str(self._unconn)


class GraphAL(Graph):
    def __init__(self, mat=list(), unconn=0):
        vnum = len(mat)
        for x in mat:
            if len(x) != vnum:
                raise ValueError('Argument for GraphAL')
        self._mat = [super(GraphAL, self)._out_edge(mat[i], unconn) for i in range(vnum)]
        self._vnum = vnum
        self._unconn = unconn

    def add_vertex(self):
        self._mat.append([])
        self._vnum += 1
        return self._vnum - 1

    def add_edge(self, vi, vj, val=1):
        if self._vnum == 0:
            raise GraphError("Cannot add edge to empty graph")
        if self._invalid(vi) or self._invalid(vj):
            raise GraphError(str(vi) or str(vj) + " is not a valid vertex")
        row = self._mat[vi]
        i = 0
        while i < len(row):
            if row[i][0] == vj:
                self._mat[vi][i] = (vj, val)
                return
            if row[i][0] > vj:
                break
            i += 1
        self._mat[vi].insert(i, (vj, val))

    def get_edge(self, vi, vj):
        if self._invalid(vi) or self._invalid(vj):
            raise GraphError(str(vi) or str(vj) + " is not a valid vertex")
        for i, val in self._mat[vi]:
            if i == vj:
                return val
        return self._unconn

    def out_edge(self, vi):
        if self._invalid(vi):
            raise GraphError(str(vi) + " is not a valid vertex")
        return self._mat[vi]


def DFS_graph(graph, v0):
    """ Depth-First Search graph """
    vnum = graph.vertex_num()
    visited = [0] * vnum
    visited[v0] = 1
    DFS_seq = [v0]
    st = SStack()
    st.push((0, graph.out_edge(v0)))
    while not st.is_empty():
        i, edges = st.pop()
        if i < len(edges):
            v, e = edges[i]
            st.push((i + 1, edges))
            if not visited[v]:
                DFS_seq.append(v)
                st.push((0, graph.out_edge(v)))
    return DFS_seq


def DFS_span_forest(graph):
    """ spanning tree """
    vnum = graph.vertex_num()
    span_forest = [None] * vnum

    def dfs(graph, v):
        nonlocal span_forest
        for u, w in graph.out_edge(v):
            if span_forest[u] is None:
                span_forest[u] = (v, w)
                dfs(graph, v)

    for v in range(vnum):
        if span_forest[v] is None:
            span_forest[v] = (v, 0)
            dfs(graph, v)

    return span_forest


def kruskal(graph):
    """ obtain min spanning tree using Kruskal Algorithm """

    vnum = graph.vertex_num()
    reps = [i for i in range(vnum)]
    mst, edges = [], []

    for vi in range(vnum):
        for v, w in graph.out_edge(vi):
            edges.append((w, vi, v))
    edges.sort()
    for w, vi, vj in edges:
        if reps[vi] !=reps[vj]:
            mst.append(((vi, vj), w))
            if len(mst) == vnum - 1:
                break
            rep, orep = reps[vi], reps[vj]
            for i in range(vnum):
                if reps[i] == orep:
                    reps[i] = rep


def prim(graph):
    """ obtain min spanning tree using Prim Algorithm """
    vnum = graph.vertex_num()
    mst = [None] * vnum
    cands = PrioQueue([(0, 0, 0)])                      # recording candidate edges
    count = 0
    while count < vnum and not cands.is_empty():
        w, u, v = cands.dequeue()                       # obtain current min edge
        if mst[v]:
            continue
        mst[v] = ((u, v), w)                            # recording new MST edge and point
        count += 1
        for vi, w in graph.out_edge(v):                 # v's neighbouring point vi
            if not mst[vi]:                             # if vi not in mst, it must be in candidate set
                cands.enqueue((w, v, vi))
    return mst