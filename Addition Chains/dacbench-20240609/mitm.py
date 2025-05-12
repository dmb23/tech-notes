#!/usr/bin/env python3

import ast, math
from typing import List, Tuple
from dataclasses import dataclass
import ladder
from primes import is_prime,inverse_table
import tally

@dataclass
class Chain:
    v_0 : int = 1
    v_1 : int = 2
    v_2 : int = 3
    value : int = 0
    len : int = 0

@dataclass 
class CombiChain:
    p : int
    q : int
    b : int
    c : int
    value : int
    len : int

    def __hash__(self):
        return hash(self.value)

@dataclass
class Boundary:
    fullchain_target : int
    leftside_target : int
    leftside_minend : int
    leftside_maxend : int
    leftside_maxlen : int # counting length after 1 2 3
    leftside_too_small: list
    rightside_maxlen : int = 0
    rightside_too_small : tuple = ()

def create_boundaries(l : int, exp : float, scale : float, factor : float) -> Boundary:
    """Filling up the boundaries dataclass with the proper boundaries"""
    leftside_target = math.ceil(scale*l**exp)
    leftside_minend = math.ceil(leftside_target/factor)
    leftside_maxend = math.floor(leftside_target*factor)
    leftside_maxlen = math.floor(1.5*math.log(leftside_maxend,2))
    leftside_too_small = create_fib_bound(leftside_maxlen, leftside_minend)
    bounds = Boundary(l, leftside_target, leftside_minend, leftside_maxend, leftside_maxlen, leftside_too_small)
    return bounds

def create_fib_bound(maxlen: int, minend: int) -> list:
    """Creates the list of Fibonacci bounds"""
    f0 = 1
    f1 = 1
    too_small = [0]*maxlen
    for j in range(maxlen - 1, -1, -1):
        too_small[j] = int((minend-1)/f1)
        f2 = f0 + f1
        f0 = f1
        f1 = f2
    too_small += [minend-1]
    return too_small

def left_search(chain : Chain, bounds : Boundary):
    """Doing one step in the left search, with recursiveness"""
    tally.node('left')
    if chain.len > bounds.leftside_maxlen: #Chain is longer than accepted
        return
    if chain.v_2 > bounds.leftside_maxend: #Chain overshoots the range we are looking for 
        return
    if chain.v_2 >= bounds.leftside_minend: #Chain is within the bounds of the range we found so save it
        yield chain
    if chain.len >= bounds.leftside_maxlen: #Chain is at maximum length; no descendants
        return
    if chain.v_2 <= bounds.leftside_too_small[chain.len]: #Chain undershoots
        return
    for result in left_search(Chain(chain.v_1, chain.v_2, chain.v_1 + chain.v_2, chain.value*2, chain.len + 1), bounds):
        yield result
    for result in left_search(Chain(chain.v_0, chain.v_2, chain.v_0 + chain.v_2, chain.value*2 + 1, chain.len + 1), bounds):
        yield result

def right_search(chain : Chain, bounds : Boundary):
    """Doing one step in the right search, with recursiveness"""
    tally.node('right')

    if chain.len > bounds.rightside_maxlen: #Chain passed the (maybe negative) upper bound of the right side
        return

    p,q = chain.v_2
    assert q >= 0

    cmin = bounds.leftside_minend
    cmax = bounds.leftside_maxend
    bmin = math.ceil(cmin/2)
    bmax = cmax

    bpmin = p*bmax if p < 0 else p*bmin
    if bpmin+q*cmin > bounds.fullchain_target: #overshoot
        return

    bpmax = p*bmin if p < 0 else p*bmax
    if bpmax+q*cmax <= bounds.rightside_too_small[chain.len]: #undershoot
        return

    yield chain
    if chain.len == bounds.rightside_maxlen: #Chain is at maximum length; no descendants
        return
    for result in right_search(Chain(chain.v_1, chain.v_2, [chain.v_1[0] + chain.v_2[0], chain.v_1[1] + chain.v_2[1]], chain.value*2, chain.len + 1), bounds):
        yield result
    for result in right_search(Chain(chain.v_0, chain.v_2, [chain.v_0[0] + chain.v_2[0], chain.v_0[1] + chain.v_2[1]], chain.value*2 + 1, chain.len + 1), bounds):
        yield result

def dictionaries(left_options : List[Chain], mod : int) -> dict:
    """Creates a dictionary of the left side chains with keys as their moduli """
    result = {}
    for left in left_options:
        tally.node('dictionary')
        key = left.v_1%mod,left.v_2%mod
        if key in result:
            result[key].append(left)
        else:
            result[key] = [left]
    return result

def indices(l : int, mod : int, dic : dict, right_options, fullchain_maxlen : int) -> List[CombiChain]:
    """Finds the b, c, p and q for which the b_mod * p + c_mod * q = target_mod holds """

    invert = inverse_table(mod)

    l_mod = l%mod
    for right in right_options:
        for b_mod in range(mod):
            # want: right.v_2[0]*b_mod + right.v_2[1]*c_mod == l_mod
            x = right.v_2[1]%mod
            z = (l_mod-right.v_2[0]*b_mod)%mod
            # want: x*c_mod == z
            if x == 0 and z == 0:
                clist = list(range(mod))
            elif x == 0:
                clist = []
            else:
                clist = [z*invert[x]%mod]

            for c_mod in clist:
                tally.node('index')
                # assert (right.v_2[0]*b_mod + right.v_2[1]*c_mod)%mod == l_mod
                if (b_mod, c_mod) not in dic: continue
                for chain in dic[b_mod, c_mod]:
                    if chain.len + right.len > fullchain_maxlen: continue
                    yield CombiChain(right.v_2[0],right.v_2[1], chain.v_1, chain.v_2,chain.value*2**right.len + right.value, chain.len + right.len)

def dac(l : int, factor_left : float = 1.1, mod_size : float = 1/3, mod_scale : float = 1.0, left_exp : float = 2/3, left_scale : float = 1.0):
    """The actual algorithm with input the target and a lot of parameters, returns the shortest found chain"""

    while True:
        bounds = create_boundaries(l, left_exp, left_scale, factor_left)
        left_options = list(left_search(Chain(1,2,3,0,0), bounds))

        if len(left_options) == 0:
            factor_left *= 1.1
            continue

        moduli = int(mod_scale*l**mod_size)
        while not is_prime(moduli): moduli += 1
        dic = dictionaries(left_options, moduli)

        # assert min(left.v_2 for left in left_options) >= bounds.leftside_minend
        # assert max(left.v_2 for left in left_options) <= bounds.leftside_maxend
        # could narrow bounds, but many experiments show that minend and maxend are consistently achieved
        leftside_minlen = min(left.len for left in left_options)

        for fullchain_maxlen in range(math.ceil(1.44*math.log(l-1,2)-2.34),math.ceil(1.5*math.log(l,2))+1):
            bounds.rightside_maxlen = fullchain_maxlen - leftside_minlen
            bounds.rightside_too_small = create_fib_bound(bounds.rightside_maxlen, l)

            right_options = right_search(Chain([-1,1],[1,0], [0,1], 0, 0), bounds)

            options = indices(l, moduli, dic, right_options, fullchain_maxlen)

            best = None
            bestlen = None

            for chain in options:
                tally.node('final')
                if chain.p * chain.b + chain.q * chain.c == l:
                    if bestlen is None or chain.len < bestlen:
                        best,bestlen = chain.value,chain.len

            if bestlen is not None:
                return best,bestlen

        factor_left *= 1.1

def chain(n):
  if n <= 3: return ladder.chain(n)
  best,bestlen = dac(n)
  C = [1,2,3]
  r0,r1,r2 = C
  for j in range(bestlen):
    if 1&(best>>(bestlen-1-j)):
      r0,r1 = r1,r0
    r0,r1,r2 = r1,r2,r1+r2
    C += [r2]
  return C

def test_primes():
  import sys
  from primes import primes

  for lim in 10,100,1000,10000:
    P = primes(lim)
    tally.clear()
    total = sum(len(chain(n))-1 for n in P)
    print(f'mitm primes limit {lim} primes {len(P)} primesum {sum(P)} chainlen {total} searchnodes {tally.nodes} {tally.nodesdetail}')
    sys.stdout.flush()

def test_dac():
  import sys
  import dac

  assert chain(29) == [1,2,3,4,7,11,18,29]

  for n in range(1,1025):
    tally.clear()
    C = chain(n)
    print(f'mitm dac {n} {C} {tally.nodesdetail}')
    sys.stdout.flush()
    assert C[-1] == n
    assert dac.is_dac_starting_from_1(C)
    if n&(n-1) == 0:
      print(f'mitm dac {n}')
      sys.stdout.flush()

def test():
  test_dac()
  test_primes()

if __name__ == '__main__':
  test()
