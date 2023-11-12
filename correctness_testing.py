#from tools import coherent_barcodes, births_deaths
from ext_barcodes_iterator import(ext_barcodes,
                                  max_ext_barcode, 
                                  lpnormtothep,
                                  non_zero_ext_cond,
                                  birth,
                                  death,
                                  rand_valid_sort)
from random import randint, seed
from copy import copy
from multiset import Multiset
seed()


# Parameters (feel free to change them): 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
x_bars_sort_func = rand_valid_sort
low = 0
high = 30
#   The time complexity is abyssmal for the following parameter. Recommend it to be not much larger than 12
max_n_bars = 12
n_tests = 3000
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

tests_cleared = 0
max_iterations = -1
while True:
    if tests_cleared >= n_tests:
      break
    tests_cleared+=1
    
    rand_bars = lambda : [(randint(low,high),randint(low,high)) for _ in range(max_n_bars)]
    x_bars = rand_bars()  
    y_bars = rand_bars()
    x_bars = rand_valid_sort(list(filter(lambda bar: bar[0]<bar[1], x_bars)))
    y_bars = sorted(list(filter(lambda bar: bar[0]<bar[1], y_bars)))
    print("Number of X-bars: ", len(x_bars))
    print("Number of Y-bars: ", len(y_bars))
    print("Iterating barcodes...")
    
    iterations = 0
    barcodes = ext_barcodes(x_bars, y_bars)
    for barcode in barcodes:
      births = Multiset(map(birth, barcode))
      deaths = Multiset(map(death, barcode))
      trivial_barcode = x_bars+y_bars
      correct_births = Multiset(map(birth, trivial_barcode))
      correct_deaths = Multiset(map(death, trivial_barcode))
      if births != correct_births or deaths != correct_deaths:
        print("The algorithm/implementation is incorrect!")
        quit()
      for bar in barcode:
        if death(bar) < birth(bar):
          print("The algorithm/implementation is incorrect!")
          quit()
      
      iterations+=1
    
    if iterations > 0:
      print("Test case", tests_cleared, "cleared.")
      print("Number of iterations/antichain tuples:", iterations)
      
    if iterations > max_iterations:
      max_iterations = iterations
    print("The test with most iterations had", max_iterations)
    print()
 
print("All", tests_cleared, "test are cleared!")