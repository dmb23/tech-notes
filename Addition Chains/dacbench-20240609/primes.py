#!/usr/bin/env python3

def primes(lim):
  if lim < 2: return []
  result = [1]*lim
  result[0] = 0
  result[1] = 0
  for p in range(2,lim):
    if p*p > lim: break
    if result[p] == 0: continue
    q = p+p
    while q < lim:
      result[q] = 0
      q += p
  return [p for p in range(lim) if result[p]]

def is_prime(n):
  if n < 2: return False
  s = 1
  while s*s <= n: s += 1
  for p in primes(s):
    if n%p == 0: return False
  return True

def inverse_table(p):
  assert is_prime(p)
  result = [0]*p
  for x in range(1,p):
    if result[x]: continue
    xpow = [1,x]
    while xpow[-1] != 1:
      xpow += [x*xpow[-1]%p]
    for i,xi in enumerate(xpow):
      result[xi] = xpow[len(xpow)-1-i]
  return result

def test():
  print('primes')

  assert primes(-1) == []
  assert primes(0) == []
  assert primes(1) == []
  assert primes(2) == []
  assert primes(3) == [2]
  assert primes(4) == [2,3]
  assert primes(5) == [2,3]
  assert primes(6) == [2,3,5]
  assert primes(7) == [2,3,5]
  assert primes(8) == [2,3,5,7]
  assert primes(9) == [2,3,5,7]
  assert primes(10) == [2,3,5,7]

  assert primes(100) == [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]

  P = primes(1000)
  assert len(P) == 168
  Q = [n for n in range(1000) if is_prime(n)]
  assert Q == P

  for p in P:
    T = inverse_table(p)
    for x in range(1,p):
      assert (x*T[x])%p == 1

  assert primes(10000) == [n for n in range(10000) if is_prime(n)]

if __name__ == '__main__':
  test()
