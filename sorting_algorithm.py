#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  7 16:25:48 2023

@author: anthony
"""

import random
import time

# generate a list of random integers between 0 and 100
random_list = [random.randint(0, 10000) for i in range(1000000)]
random_list2 = random_list.copy()

def insertion_sort(L):
    for i in range(1,len(L)):
        while i > 0:
            if L[i-1] > L[i]:
                L[i-1], L[i] = L[i], L[i-1]
            i -= 1
            
            
def quick_sort(L):
    if len(L) > 1:
        pivot = random.choice(L)
        left = [x for x in L if x < pivot]
        middle = [x for x in L if x == pivot]
        right = [x for x in L if x > pivot]
        return quick_sort(left) + middle + quick_sort(right)
    return L
      
    
start_time = time.time()

random_list.sort()

end_time = time.time()
    
print("Elapsed time: {:.2f} seconds".format(end_time - start_time))


 
start_time = time.time()

L=quick_sort(random_list2)

end_time = time.time()

     
print("Elapsed time: {:.2f} seconds".format(end_time - start_time))