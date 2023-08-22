#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  6 20:42:53 2023

@author: anthony
"""
import numpy as np

# function to know if we can place a queen
def issafe(x,y):
    global board
    board_size = len(board)
    for i in range(board_size):
        # check if queen on column
        if board[x][i] == 1:
            return False
        # check if queen on row
        if board[i][y] == 1:
            return False
    # check if queen on top-left diagonal
    i, j = x, y
    while i >=0 and j >= 0:
        if board[i][j] == 1:
            return False
        i -= 1
        j -= 1
    # check if queen on top-right diagonal
    i, j = x, y
    while i >=0 and j < board_size:
        if board[i][j] == 1:
            return False
        i -= 1
        j += 1
    # check if queen on bottom-left diagonal
    i, j = x, y
    while i < board_size and j >= 0:
        if board[i][j] == 1:
            return False
        i += 1
        j -= 1
    # check if queen on bottom-right diagonal
    i, j = x, y
    while i < board_size and j < board_size:
        if board[i][j] == 1:
            return False
        i += 1
        j += 1 
    
    return True

# find all combinations of possible solutions
def solve_all_solutions(x, y):
    global board, nb_solutions
    board_size = len(board)
    for i in range(x, board_size):
        for j in range(board_size):
            if issafe(i,j):
                board[i][j] = 1
                solve_all_solutions(i+1,0)
                board[i][j] = 0
        return
    nb_solutions +=1
   
# find one solution
def solve(x, y):
    global board, nb_solutions
    board_size = len(board)
    for i in range(x, board_size):
        for j in range(board_size):
            if issafe(i,j):
                board[i][j] = 1
                if solve(i+1,0):
                    return True
                board[i][j] = 0
        return False
    print(board)
    return True



# define size of board
n = int(input("Which size of board ? "))

board = np.zeros((n,n))

nb_solutions = 0
solve_all_solutions(0, 0)
print("There is ", nb_solutions, " solutions")
        
solve(0,0)
