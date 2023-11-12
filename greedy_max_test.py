#from tools import coherent_barcodes, births_deaths
from ext_barcodes_iterator import(ext_barcodes,
                                  max_ext_barcode,
                                  lpnormtothep,
                                  non_zero_ext_cond,
                                  rand_valid_sort)
from random import (randint,
                    seed,
                    choice)
from copy import copy
from multiset import FrozenMultiset
from math import inf
seed()


# Parameters (feel free to change them): 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
x_bars_sort_func = rand_valid_sort
low = 0
high = 30
#   The time complexity is abyssmal for the following parameter. Recommend it to be not much larger than 12
max_n_bars = 12
#   Setting the following parameter to False should benefit performence slightly
count_barcodes = True
n_tests = 3000
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


tests_cleared = 0
max_iterations = -1
max_number_of_barcodes = -1
while True:
    if tests_cleared >= n_tests:
      break
    tests_cleared+=1
    
    p = choice([2, inf])
    rand_bars = lambda : [(randint(low,high),randint(low,high)) for _ in range(max_n_bars)]
    x_bars = rand_bars()  
    y_bars = rand_bars()
    x_bars = x_bars_sort_func(list(filter(lambda bar: bar[0]<bar[1], x_bars)))
    y_bars = sorted(list(filter(lambda bar: bar[0]<bar[1], y_bars)))
    print("Number of X-bars: ", len(x_bars))
    print("Number of Y-bars: ", len(y_bars))
    print("Iterating barcodes...")
    
    iterations = 0
    first_place = -1
    barcodes = ext_barcodes(x_bars, y_bars)
    barcodes_set = set()
    for barcode in barcodes:
      iterations+=1
      if count_barcodes: barcodes_set.add(FrozenMultiset(barcode))
        
      current = lpnormtothep(barcode, p)
      if current > first_place:
        first_place = current
    
    greedy = lpnormtothep(max_ext_barcode(x_bars, y_bars), p)
    if greedy != first_place:
      print("Conjecture is false.")
      print(greedy, first_place)
      print(*barcodes_set, sep='\n')
      quit()
    
    if iterations > 0:
      print("Test case", tests_cleared, "cleared.")
      print("Number of iterations/antichain tuples:", iterations)
      if count_barcodes: print("Number of barcodes:", len(barcodes_set))
      
    if iterations > max_iterations:
      max_iterations = iterations
    
    if len(barcodes_set) > max_number_of_barcodes:
      max_number_of_barcodes = len(barcodes_set)
    
    print("The test with most iterations had", max_iterations)
    if count_barcodes: print("The test with most barcodes had", max_number_of_barcodes)
    print()

print("All", tests_cleared, "test are cleared!")