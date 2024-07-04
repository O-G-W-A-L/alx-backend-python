#!/usr/bin/env python3
'''Python Variable annotation'''

from typing import Iterable, Tuple, Sequence, List


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    '''computes the length of list of sequences'''
    return [(i, len(i)) for i in lst]
