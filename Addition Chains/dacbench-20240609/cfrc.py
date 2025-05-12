#!/usr/bin/env python3

from math import gcd
import tally

# 1992 montgomery section 5
def cfrc(n,r):
  n = int(n)
  r = int(r)
  assert 0 < r and r <= n
  assert gcd(r,n) == 1
  a,b,d,e = 1,1,r,n-r
  C = [1]
  while e != 0:
    tally.node('step')
    if d > e:
      b,d = a+b,d-e
      C += [b]
    else:
      a,e = a+b,e-d
      C += [a]
  return C

def chain(n):
  n = int(n)
  result = None
  for r in range(1,n+1):
    if gcd(n,r) == 1:
      C = cfrc(n,r)
      if result is None or len(C) < len(result):
        result = C
  return result

def test_primes():
  import sys
  from primes import primes

  for lim in 10,100,1000,10000:
    P = primes(lim)
    tally.clear()
    total = sum(len(chain(n))-1 for n in P)
    print(f'cfrc primes limit {lim} primes {len(P)} primesum {sum(P)} chainlen {total} searchnodes {tally.nodes}')
    sys.stdout.flush()
    # total from 1992 montgomery table 5
    if lim == 10000: assert total == 21558

def test_dac():
  import sys
  import dac

  for n in range(1,513):
    C = chain(n)
    assert C[-1] == n
    assert dac.is_dac_starting_from_1(C)
    for r in range(1,n+1):
      if gcd(n,r) == 1:
        C = cfrc(n,r)
        assert C[-1] == n
        assert dac.is_dac_starting_from_1(C)
    if n&(n-1) == 0:
      print(f'cfrc dac {n}')
      sys.stdout.flush()

def test():
  test_dac()
  test_primes()

if __name__ == '__main__':
  test()
