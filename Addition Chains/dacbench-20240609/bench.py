#!/usr/bin/env python3

import sys

lim = 100000000
if len(sys.argv) >= 2: lim = int(sys.argv[1])

import ladder
import prac
import cfrc
import sibc
import ctidh
import prune
import mitm
import mitm2

from primes import is_prime
import dac

import os
import multiprocessing
import time
import tally

try:
  threads = len(os.sched_getaffinity(0))
except:
  threads = cpu_count()
threads = os.getenv('THREADS',default=threads)
threads = int(threads)
if threads < 1: threads = 1

def doit(p,name):
  target = eval(name)
  tally.clear()
  ns = -time.process_time_ns()
  C = target.chain(p)
  ns += time.process_time_ns()
  nodes = tally.nodes
  assert C[-1] == p
  assert dac.is_dasc_starting_from_1(C)
  if name != 'prac':
    assert dac.is_dac_starting_from_1(C)
  return (p,name,nodes,ns,len(C)-1)

todo = []

p = 2
while p < lim:
  for name in 'ladder','prac','cfrc','sibc','ctidh','prune','mitm','mitm2':
    if p > 10000 and name == 'sibc': continue
    if p > 100000 and name == 'cfrc': continue
    if p > 1000000 and name == 'ctidh': continue
    todo += [(p,name)]
  p += 1 + (p>>8)
  while not is_prime(p): p += 1

with multiprocessing.Pool(threads) as p:
  results = p.starmap(doit,reversed(todo),chunksize=1)

for p,name,nodes,ns,lenC1 in reversed(results):
  print(f'p {p} target {name} nodes {nodes} ns {ns} len {lenC1}')
