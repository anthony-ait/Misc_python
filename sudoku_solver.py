#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  6 20:10:11 2023

@author: anthony
"""

import numpy as np


grid = np.array([    
    [1, 0, 0, 0, 0, 7, 0, 9, 0],
    [0, 3, 0, 0, 2, 0, 0, 0, 8],
    [0, 0, 9, 6, 0, 0, 5, 0, 0],
    [0, 0, 5, 3, 0, 0, 9, 0, 0],
    [0, 1, 0, 0, 8, 0, 0, 0, 2],
    [6, 0, 0, 0, 0, 4, 0, 0, 0],
    [3, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 4, 0, 0, 0, 0, 0, 0, 7],
    [0, 0, 7, 0, 0, 0, 3, 0, 0]
])


# define a function to know if we can put or not a number n in position (x,y)
def possible(x,y,n):
    # give access to grid outside the function
    global grid
    for i in range(9):
        if grid[i][y] == n:
            return False
        if grid[x][i] == n:
            return False
        # define in which bloc n is
        x0 = (x//3)*3
        y0 = (y//3)*3
        for i in range(3):
            for j in range(3):
                if grid[x0+i][y0+j] == n:
                    return False
    return True


def solve():
    global grid
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0 :
                for n in range(1,10):
                    if possible(i,j,n):
                        grid[i][j] = n
                        # each time we put a new number, we recall the function
                        solve()
                        grid[i][j] = 0
                return
    print(grid)
    input("More?")
                
     
solve()