# -*- coding: utf-8 -*-

__author__ = 'barnett'


class record:
    def __init__(self, key, datnum):
        self.key = key
        self.datnum = datnum


def insert_sort(lst):
    """ insert sort """
    for i in range(1, len(lst)):
        x = lst[i]
        j = i
        while j > 0 and lst[j - 1].key > x.key:
            lst[j] = lst[j - 1]
            j -= 1
        lst[j] = x


def select_sort(lst):
    """ select sort """
    for i in range(len(lst) - 1):
        k = i
        for j in range(i, len(lst)):
            if lst[j].key < lst[k].key:
                k = j
        if i != k:
            lst[i], lst[k] = lst[k], lst[i]


def bubble_sort(lst):
    """ bubble sort """
    for i in range(len(lst)):
        found = False
        for j in range(1, len(lst)):
            if lst[j - 1].key > lst[j].key:
                lst[j - 1], lst[j] = lst[j], lst[j - 1]
                found = True
        if not found:
            break


def quick_sort(lst):
    """ quick sort """

    def qsort_rec(lst, l, r):
        """ quick sort recursion """
        if l > r:
            return
        i = l
        j = r
        pivot = lst[i]
        while i < j:
            while i < j and lst[j].key >= pivot.key:
                j -= 1
                if i < j:
                    lst[i] = lst[j]
                    i += 1
            while i < j and lst[i].key <= pivot.key:
                i += 1
            if i < j:
                lst[j] = lst[i]
                j -= 1
            lst[i] = pivot
            qsort_rec(lst, 1, i - 1)
            qsort_rec(lst, i + 1, r)

    qsort_rec(lst, 0, len(lst) - 1)


def quick_sort1(lst):
    """ other quick sort """

    def qsort(lst, begin, end):
        if begin >= end:
            return
        pivot = lst[begin].key
        i = begin
        for j in range(begin + 1, end + 1):
            if lst[j].key < pivot:
                i += 1
                lst[i], lst[j] = lst[j], lst[i]
        lst[begin], lst[i] = lst[i], lst[begin]
        qsort(lst, begin, i - 1)
        qsort(lst, i + 1, end)

    qsort(lst, 0, len(lst) - 1)


def merge_sort(lst):
    """ merge sort """

    def merge(lfrom, lto, low, mid, high):
        i, j, k = low, m, low
        while i < mid and j < high:
            if lfrom[i].key <= lfrom[j].key:
                lto[k] = lfrom[i]
                i += 1
            else:
                lto[k] = lfrom[i]
                j += 1
            k += 1
        while i < mid:
            lto[k] = lfrom[i]
            i += 1
            k += 1
        while j < high:
            lto[k] = lfrom[j]
            j += 1
            k += 1

    def merge_pass(lfrom, lto, llen, slen):
        i = 0
        while i + 2 * slen < llen:
            merge(lfrom, lto, i + slen, i + 2 * slen)
            i += 2 * slen
        if i + slen < llen:
            merge(lfrom, lto, i, i + slen, llen)
        else:
            for j in range(i, llen):
                lto[j] = lfrom[j]

    slen, llen = 1, len(lst)
    templst = [None] * llen
    while slen < llen:
        merge_pass(lst, templst, llen, slen)
        slen *= 2
        merge_pass(templst, lst, llen, slen)
        slen *= 2


def radix_sort(lst, d):
    rlists = [[] for i in range(10)]
    llen = len(lst)
    for m in range(-1, -d-1, -1):
        for j in range(llen):
            rlists[lst[j].key[m]].append(lst[j])
        j = 0
        for i in range(10):
            tmp = rlists[i]
            for k in range(len(tmp)):
                lst[j] = tmp[k]
                j += 1
            rlists[i].clear()


if __name__ == '__main__':
    pass
