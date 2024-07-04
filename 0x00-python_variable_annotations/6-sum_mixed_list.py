#!/usr/bin/env python3
'''Python - Variable annotation'''


from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    '''computes the sum of a list of integers and floating-point numbers'''
    for i in range(len(mxd_lst)):
        mxd_lst[i] = float(mxd_lst[i])
    return sum(mxd_lst)
