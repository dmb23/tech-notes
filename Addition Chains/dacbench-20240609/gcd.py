#!/usr/bin/env python3

from math import gcd

def test():
  print('gcd')

  for a in range(-100,100):
    for b in range(-100,100):
      g = gcd(a,b)
      assert g == gcd(b,a)
      assert g == gcd(-a,b)
      assert g == gcd(a,-b)
      if (a,b) == (0,0): assert g == 0
      if (a,b) != (0,0):
        assert g > 0
        assert a%g == 0
        assert b%g == 0

  for a in range(0,1000):
    assert gcd(a,0) == abs(a)
    assert gcd(a,1) == 1
    assert gcd(a,2) == 2 if a%2 == 0 else 1
    assert gcd(a,3) == 3 if a%3 == 0 else 1
    assert gcd(a,4) == 4 if a%4 == 0 else 2 if a%2 == 0 else 1
    assert gcd(a,5) == 5 if a%5 == 0 else 1
    assert gcd(a,6) == 6 if a%6 == 0 else 3 if a%3 == 0 else 2 if a%2 == 0 else 1

if __name__ == '__main__':
  test()
