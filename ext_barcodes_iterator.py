from itertools import islice, chain, starmap, pairwise, product
from sortedcontainers import SortedList
from copy import copy
from functools import reduce
from math import inf
from random import shuffle


def birth(bar):
  return bar[0]


def death(bar):
  return bar[1]


def union_iterator(index_set, operand):
  return chain.from_iterable(map(operand, index_set))


def lpnormtothep(barcode, p = 2):
  q = p if p != inf else 1
  s = map(lambda bar: abs(death(bar)-birth(bar))**q if birth(bar)<death(bar) else 0,
          barcode)
  if p == inf:
    return max(map( lambda bar: 
                      abs(death(bar)-birth(bar)) if birth(bar)<death(bar) else 0,
                    barcode))
  else:
    return sum(map( lambda bar: 
                      abs(death(bar)-birth(bar))**q if birth(bar)<death(bar) else 0,
                    barcode))


""" This function returns an iterator for the set \pi(Ext(X,Y)) (see the thesis). Though, duplicates can occur.

The order of x_bars DOES matter here: They need to satsify 
  i < j  ==>  not( birth(x_bars[j]) < birth(x_bars[i]) <= death(x_bars[j]) < death(x_bars[i]) )
If this condition is not satisfied, then the second part ($\supseteq$) of the proof of Corollary 4.2 does not work, and so the following functions might return barcodes not in pi(Ext(X,Y)). One order that is the lexicographical one (e.g. x_bars = SortedList(x_bars)). The order of y_bars does not matter. """
def ext_barcodes(x_bars, y_bars, antichains_func=None):
  y_bars = SortedList(y_bars)
  
  def ext_barcodes_given_x_bars(bars, x_bars_dropped = 0):
    if x_bars_dropped == len(x_bars):
      yield bars
    else:
      x_bar = x_bars[x_bars_dropped]
      yield from union_iterator(ext_barcodes_spec(x_bar, bars, antichains_func),
                                lambda mixed_bars: ext_barcodes_given_x_bars(mixed_bars, x_bars_dropped+1))
  
  return ext_barcodes_given_x_bars(y_bars)


""" See the documentation of 'ext_barcodes'. This function probably not of use by it self - it is just to be able to write the function 'ext_barcodes_with_antichain_seq' """
def ext_barcodes_with_info(x_bars, y_bars, antichains_func=None):
  y_bars = SortedList(y_bars)
  
  def ext_barcodes_given_x_bars(bars, x_bars_dropped = 0):
    if x_bars_dropped == len(x_bars):
      yield (bars, [bars])
    else:
      x_bar = x_bars[x_bars_dropped]
      yield from union_iterator(ext_barcodes_spec(x_bar, bars, antichains_func),
                                lambda mixed_bars: ((barcode, [bars]+info_list) for (barcode, info_list) in ext_barcodes_given_x_bars(mixed_bars, x_bars_dropped+1)))
  
  return ext_barcodes_given_x_bars(y_bars)


def minus(xs, ys):
      xs=copy(xs)
      for y in ys:
        xs.discard(y)
      return xs


""" Thus functions returns an iterator, which in turn gives pairs whose first component is a barcode in \pi(Ext(X,Y)) and second component is the tuple of antichains whose image under the map \phi is this barcode (see Corollary 4.3 in the thesis). Equivelently, the function returns an iterator for the graph of \phi. """
def ext_barcodes_with_antichain_seq(x_bars, y_bars, antichains_func=None):
  return  (
            (barcode, list(starmap(minus, pairwise(info_list))))
            for barcode, info_list in ext_barcodes_with_info(x_bars, y_bars, antichains_func)
          )


def non_zero_ext_cond(x_bar, y_bar):
  return (birth(x_bar) < birth(y_bar) and
                         birth(y_bar) <= death(x_bar) and
                                         death(x_bar) < death(y_bar))


def zero_ext_cond(x_bar, y_bar):
  return not non_zero_ext_cond(x_bar, y_bar)


def shift(list_of_pairs):
  if len(list_of_pairs) <= 1:
    return list_of_pairs
  else:
    return ( (a,b_shifted) for ((a,b), (a_shifted, b_shifted)) in zip(list_of_pairs, list_of_pairs[1:]+[list_of_pairs[0]]) )


def unshift(list_of_pairs):
  if len(list_of_pairs) <= 1:
    return list_of_pairs
  else:
    return ( (a,b_shifted) for ((a,b), (a_shifted, b_shifted)) in zip(list_of_pairs, [list_of_pairs[-1]]+list_of_pairs[:-1]) )


def antichains(sorted_list):
  if len(sorted_list) == 0 :
    yield []
  else:
    sorted_list_without_maximum = copy(sorted_list)
    maximum = sorted_list_without_maximum.pop()
    acs_without_maximum = antichains(sorted_list_without_maximum)
    for ac in acs_without_maximum:
      yield ac
      ac_and_maximum_form_antichain = len(ac) == 0 or death(maximum) < death(ac[-1])
      if ac_and_maximum_form_antichain:
        yield ac+[maximum]


def incomparable(u, v):
  return (birth(u) < birth(v) and death(v) < death(u) or
          birth(v) < birth(u) and death(u) < death(v))


def maximals(sorted_list):
  if len(sorted_list) == 0:
    return SortedList([])
  else:
    sorted_list_without_maximum = copy(sorted_list)
    maximum = sorted_list_without_maximum.pop()
    maximals = SortedList([maximum])
    for x in reversed(sorted_list_without_maximum):
      leftmost_maximum = maximals[0]
      if incomparable(leftmost_maximum, x):
        maximals.add(x)
    return maximals


""" This function returns an iterator for \pi(Ext(x_bar,y_bars)) (see Theorem 3.1 in the thesis). """
def ext_barcodes_spec(x_bar, y_bars, antichains_func=None):
  valid_y_bars = list(filter(lambda y_bar: non_zero_ext_cond(x_bar, y_bar), y_bars)) # denoted F^{ab}(Y) in the thesis.
  acs = antichains(valid_y_bars)\
        if not antichains_func else\
        antichains_func(valid_y_bars) 
  for ac in acs:
    # The remaining lines computes and returns \psi(ac)
    barcode = copy(y_bars)
    for bar in ac:
      barcode.remove(bar)
    barcode.update(shift([x_bar]+ac))
    yield barcode


def max_ext_barcode(x_bars,y_bars):
  return list(ext_barcodes( x_bars,
                            y_bars,
                            antichains_func=lambda bars: SortedList([maximals(bars)])))[0]


def max_ext_barcode_with_antichain_seq(x_bars,y_bars):
  return list(ext_barcodes_with_antichain_seq(x_bars,
                                              y_bars,
                                              antichains_func=lambda bars: SortedList([maximals(bars)])))[0]


def product_leq(pair1, pair2):
  return pair1[0]<=pair2[0] and pair1[1]<=pair2[1]


def antichain_leq(A, B):
  for a in A:
    if any(product_leq(a,b) for b in B):
      continue
    else:
      return False
  return True
  
  
def ext_dim(x_bars, y_bars):
  return reduce(lambda dim, x_bar_y_bar:
                  dim + non_zero_ext_cond(*x_bar_y_bar),
                product(x_bars, y_bars),
                0)


""" This function returns a copy of bars, but reordered in a way as to satsify the condition x_bars must satisfy in the function 'ext_barcodes'. There are many possible such reorderings, but this function constructs one at RANDOM. """
def rand_valid_sort(bars):
  if len(bars) == 0:
    return []
  bars=copy(bars)
  indcs = list(range(len(bars)))
  shuffle(indcs)
  for i in indcs:
    first_candidate = bars[i]
    for bar in bars:
      if non_zero_ext_cond(bar, first_candidate):
        break
    else:
      bars.pop(i)
      return [first_candidate]+rand_valid_sort(bars)


# def antichain_seq_leq(As, Bs):
  # assert len(As)==len(Bs)
  # n=len(As)
  # for k in range(n):
    # union = lambda Cs: reduce(lambda C, Cp: C+Cp, islice(Cs, k+1))
    # union_A = union(As)
    # union_B = union(Bs)
    # max_supp = lambda M: maximals(SortedList(set(M)))
    # while len(union_A)>0:
      # max_supp_A = max_supp(union_A)
      # max_supp_B = max_supp(union_B)
      # union_A = minus(union_A, max_supp_A)
      # union_B = minus(union_B, max_supp_B)
      # if antichain_leq( max_supp_A, max_supp_B ):
        # continue
      # else:
        # return False
  
  # return True