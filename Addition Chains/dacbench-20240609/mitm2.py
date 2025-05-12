#!/usr/bin/env python3

import ast, math
from typing import List, Tuple
from dataclasses import dataclass
import ladder
from primes import is_prime,inverse_table
import tally

tracing = False

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
    fullchain_len : int
    fullchain_too_small: list
    leftside_len : int # counting length after 1 2 3
    rightside_len : int
    leftside_minend : int = 0
    leftside_maxend : int = 0

def create_boundaries(n : int, chainlen : int) -> Boundary:
    """Filling up the boundaries dataclass with the proper boundaries"""
    fullchain_target = n
    fullchain_len = chainlen
    fullchain_too_small = create_fib_bound(fullchain_len, fullchain_target)
    leftside_len = (2*chainlen)//3
    rightside_len = chainlen-leftside_len
    return Boundary(fullchain_target, fullchain_len, fullchain_too_small, leftside_len, rightside_len)

def create_fib_bound(maxlen: int, minend: int) -> list:
    """Creates the list of Fibonacci bounds"""
    f0 = 1
    f1 = 2
    too_small = [0]*maxlen
    for j in range(maxlen - 1, -1, -1):
        too_small[j] = int((minend-1)/f1)
        f2 = f0 + f1
        f0 = f1
        f1 = f2
    too_small += [minend-1]
    return too_small

def left_search(chain : Chain, bounds : Boundary):
    """Doing one step in the left search, with recursion"""
    tally.node('left')
    if tracing: print(f'left_search {chain}')
    if chain.len == bounds.leftside_len: #Found a chain of the correct length
        yield chain
    if chain.len >= bounds.leftside_len: #No descendants after the correct length
        return
    if chain.v_2 <= bounds.fullchain_too_small[chain.len]: #Chain undershoots, prune descendants
        return
    # XXX: could also prune overshoot if chain.v_2+chain.v_1*(bounds.fullchain_len-chain.len) > bounds.fullchain_target
    # but large chains should not encounter this for reasonable leftside_len
    for result in left_search(Chain(chain.v_1, chain.v_2, chain.v_1 + chain.v_2, chain.value*2, chain.len + 1), bounds):
        yield result
    for result in left_search(Chain(chain.v_0, chain.v_2, chain.v_0 + chain.v_2, chain.value*2 + 1, chain.len + 1), bounds):
        yield result

def right_search(chain : Chain, bounds : Boundary):
    """Doing one step in the right search, with recursion"""
    tally.node('right')
    if tracing: print(f'right_search {chain}')

    p,q = chain.v_2
    assert q >= 0

    cmin = bounds.leftside_minend
    cmax = bounds.leftside_maxend
    bmin = math.ceil(cmin/2)
    bmax = cmax

    bpmin = p*bmax if p < 0 else p*bmin
    if bpmin+q*cmin > bounds.fullchain_target: #overshoot
        if tracing: print('overshoot')
        return

    bpmax = p*bmin if p < 0 else p*bmax
    if bpmax+q*cmax <= bounds.fullchain_too_small[bounds.leftside_len+chain.len]: #undershoot
        if tracing: print(f'undershoot max {bpmax+q*cmax} len {bounds.leftside_len+chain.len} bound {bounds.fullchain_too_small[bounds.leftside_len+chain.len]}')
        return

    if chain.len == bounds.rightside_len:
        yield chain
    if chain.len >= bounds.rightside_len: #No descendants after the correct length
        return

    for result in right_search(Chain(chain.v_1, chain.v_2, [chain.v_1[0] + chain.v_2[0], chain.v_1[1] + chain.v_2[1]], chain.value*2, chain.len + 1), bounds):
        yield result
    for result in right_search(Chain(chain.v_0, chain.v_2, [chain.v_0[0] + chain.v_2[0], chain.v_0[1] + chain.v_2[1]], chain.value*2 + 1, chain.len + 1), bounds):
        yield result

def leftright_search(n : int, mod : int, left_dictionary : dict, right_options) -> List[CombiChain]:
    """Finds the b, c, p and q for which the b_mod * p + c_mod * q = n_mod holds """

    invert = inverse_table(mod)

    n_mod = n%mod
    for right in right_options:
        if tracing: print(f'right {right}')
        for b_mod in range(mod):
            # want: right.v_2[0]*b_mod + right.v_2[1]*c_mod == n_mod
            x = right.v_2[1]%mod
            z = (n_mod-right.v_2[0]*b_mod)%mod
            # want: x*c_mod == z
            if x == 0 and z == 0:
                clist = list(range(mod))
            elif x == 0:
                clist = []
            else:
                clist = [z*invert[x]%mod]

            for c_mod in clist:
                tally.node('index')
                assert (right.v_2[0]*b_mod + right.v_2[1]*c_mod)%mod == n_mod
                if (b_mod, c_mod) not in left_dictionary: continue
                for left in left_dictionary[b_mod, c_mod]:
                    yield CombiChain(right.v_2[0],right.v_2[1], left.v_1, left.v_2,left.value*2**right.len + right.value, left.len + right.len)

def chain_of_len(n,chainlen):
    bounds = create_boundaries(n,chainlen)
    if tracing: print(f'bounds {bounds}')

    left_options = left_search(Chain(1,2,3,0,0), bounds)

    mod = int(n**(1/3)) # XXX: allow tuning, maybe also depending on chainlen
    while not is_prime(mod): mod += 1
    if tracing: print(f'modulus {mod}')

    leftside_minend = None
    leftside_maxend = None

    left_dictionary = {}
    for left in left_options:
        tally.node('dictionary')
        if tracing: print(f'left {left}')
        key = left.v_1%mod,left.v_2%mod
        if key in left_dictionary:
            left_dictionary[key].append(left)
        else:
            left_dictionary[key] = [left]
        
        end = left.v_2
        if leftside_minend is None or end < leftside_minend: leftside_minend = end
        if leftside_maxend is None or end > leftside_maxend: leftside_maxend = end

    if len(left_dictionary) == 0: return
    bounds.leftside_minend = leftside_minend
    bounds.leftside_maxend = leftside_maxend
    if tracing: print(f'leftside_minend {leftside_minend}')
    if tracing: print(f'leftside_maxend {leftside_maxend}')

    right_options = right_search(Chain([-1,1],[1,0],[0,1],0,0), bounds)

    leftright_options = leftright_search(n, mod, left_dictionary, right_options)

    for chain in leftright_options:
        tally.node('final')
        if chain.p * chain.b + chain.q * chain.c == n:
            return chain.value

def chain(n):
  if n <= 3: return ladder.chain(n)

  chainlen = 0
  while True:
    compressed = chain_of_len(n,chainlen)
    if compressed is not None: break
    chainlen += 1

  C = [1,2,3]
  r0,r1,r2 = C
  for j in range(chainlen):
    if 1&(compressed>>(chainlen-1-j)):
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
    print(f'mitm2 primes limit {lim} primes {len(P)} primesum {sum(P)} chainlen {total} searchnodes {tally.nodes} {tally.nodesdetail}')
    sys.stdout.flush()

def test_dac():
  import sys
  import dac

  assert chain(29) == [1,2,3,4,7,11,18,29]
  
  for n in range(1,1025):
    tally.clear()
    C = chain(n)
    print(f'mitm2 dac {n} {C} {tally.nodesdetail}')
    sys.stdout.flush()
    assert C[-1] == n
    assert dac.is_dac_starting_from_1(C)
    if n&(n-1) == 0:
      print(f'mitm2 dac {n}')
      sys.stdout.flush()

def test():
  test_dac()
  test_primes()

if __name__ == '__main__':
  test()
