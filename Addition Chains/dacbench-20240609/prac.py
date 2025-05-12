#!/usr/bin/env python3

import math
from math import gcd
import tally

# 1992 montgomery section 7
# with a,b filled in
# and p determined from checking 2,3,5,7,gcd(p,r)
def chain(n):
  n = int(n)
  assert n > 0
  C = [1]
  d = n
  while d != 1:
    p = d
    while True:
      # p > 1; p divides d; not necessarily prime
      if p%2 == 0: p = 2
      if p%3 == 0: p = 3
      if p%5 == 0: p = 5
      if p%7 == 0: p = 7
      r = math.floor(0.6180339887498948482*p+0.5)
      g = gcd(p,r)
      if g == 1:
        r *= d//p
        break
      p = g

    a = n//d
    b = a
    d,e = r,d-r

    tally.node('start')

    # print(f'start n {n} a {a} b {b} d {d} e {e} r {r}')
    # assert a*d+b*e == n
    # assert d > 0
    # assert e >= 0
    # assert gcd(n,r) % gcd(d,e) == 0
    
    while d != e:
      tally.node('step')
      # assert a*d+b*e == n
      # assert d > 0
      # assert e >= 0
      # assert gcd(n,r) % gcd(d,e) == 0

      if d < e:
        a,b,d,e = b,a,e,d

      # cases in 1992 montgomery table 4
      if 4*d <= 5*e and (d+e)%3 == 0: # case 1
        C += [a+b]
        a,b,d,e = 2*a+b,a+2*b,(2*d-e)//3,(2*e-d)//3
        C += [a,b]
      elif 4*d <= 5*e and (d-e)%6 == 0: # case 2
        b,d = a+b,d-e
        a,d = 2*a,d//2
        C += [b,a]
      elif d <= 4*e: # case 3
        b,d = a+b,d-e
        C += [b]
      elif (d-e)%2 == 0: # case 4
        b,d = a+b,d-e
        a,d = 2*a,d//2
        C += [b,a]
      elif d%2 == 0: # case 5
        a,d = 2*a,d//2
        C += [abs(a-b),a]
      elif d%3 == 0: # case 6
        C += [a+b,2*a,3*a,3*a+b]
        a,d = 3*a,d//3
        b,d = a+b,d-e
      elif (d+e)%3 == 0: # case 7
        C += [a+b,2*a]
        b,d = 2*a+b,d-2*e
        a,d = 3*a,d//3
        C += [b,a]
      elif (d-e)%3 == 0: # case 8
        b,d = a+b,d-e
        C += [b,2*a]
        a,d = 3*a,d//3
        C += [abs(a-b),a]
      else: # case 9
        assert e%2 == 0
        b,e = 2*b,e//2
        C += [abs(a-b),b]

    C += [a+b]

  return C

def test_primes():
  import sys
  from primes import primes

  for lim in 10,100,1000,10000,100000,1000000:
    P = primes(lim)
    tally.clear()
    total = sum(len(chain(n))-1 for n in P)
    print(f'prac primes limit {lim} primes {len(P)} primesum {sum(P)} chainlen {total} searchnodes {tally.nodes}')
    sys.stdout.flush()
    # totals from 1992 montgomery table 5
    if lim == 10000: assert total == 22204
    if lim == 1000000: assert total == 2278430

def test_dac():
  import sys
  import dac

  numn = 0
  numdac = 0
  numdasc = 0

  for n in range(1,16385):
    C = chain(n)
    isdac = dac.is_dac_starting_from_1(C)
    isdasc = dac.is_dasc_starting_from_1(C)
    # print(f'prac {n} dac {isdac} {C}')
    sys.stdout.flush()
    assert C[-1] == n
    numn += 1
    numdac += isdac
    numdasc += isdasc
    if n&(n-1) == 0:
      print(f'prac numn {numn} numdasc {numdasc} numdac {numdac}')
      sys.stdout.flush()

def test_rand():
  import sys
  import dac
  import random

  for bits in range(10,210,10):
    numn = 0
    numdac = 0
    numdasc = 0

    for loop in range(1000):
      n = random.randrange(1,1<<bits)
      C = chain(n)
      isdac = dac.is_dac_starting_from_1(C)
      isdasc = dac.is_dasc_starting_from_1(C)
      numn += 1
      numdac += isdac
      numdasc += isdasc

    print(f'prac random bits {bits} numn {numn} numdasc {numdasc} numdac {numdac}')

def test():
  test_dac()
  test_primes()
  test_rand()

if __name__ == '__main__':
  test()
