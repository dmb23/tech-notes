#!/usr/bin/env python3

import ladder
import math
import tally

# search() and chain() based on sibc/precompute_sdacs.py
# but using yield to limit memory usage

def search(n,r0,r1,r2,additions):
  tally.node('step')
  if r2 == n:
    yield []
  if r2 < n and additions > 0:
    for D in search(n,r0,r2,r2+r0,additions-1):
      yield [r2+r0]+D
    for D in search(n,r1,r2,r2+r1,additions-1):
      yield [r2+r1]+D

def chain(n):
  C = ladder.chain(n)
  additions = math.floor(1.5*math.log(n,2))
  for D in search(n,1,2,3,additions):
    D = [1,2,3]+D
    if len(D) < len(C):
      C = D
  return C

def test_primes():
  import sys
  from primes import primes

  for lim in 10,100,1000,10000:
    P = primes(lim)
    tally.clear()
    total = sum(len(chain(n))-1 for n in P)
    print(f'sibc primes limit {lim} primes {len(P)} primesum {sum(P)} chainlen {total} searchnodes {tally.nodes}')
    sys.stdout.flush()

def test_dac():
  import sys
  import dac

  assert chain(29) == [1,2,3,4,7,11,18,29]

  for n in range(1,1025):
    C = chain(n)
    # print(f'sibc dac {n} {C}')
    # sys.stdout.flush()
    assert C[-1] == n
    assert dac.is_dac_starting_from_1(C)
    if n&(n-1) == 0:
      print(f'sibc dac {n}')
      sys.stdout.flush()

def test():
  test_dac()
  test_primes()

if __name__ == '__main__':
  test()
