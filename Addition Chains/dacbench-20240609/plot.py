#!/usr/bin/env python3

chromium = False

import sys
import math
import itertools

data = {}

for line in sys.stdin:
  line = line.split()
  assert line[0] == 'p'
  assert line[2] == 'target'
  assert line[4] == 'nodes'
  assert line[6] == 'ns'
  assert line[8] == 'len'
  p,target,nodes,ns,adds = line[1:10:2]
  p,nodes,ns,adds = map(int,(p,nodes,ns,adds))
  if target not in data: data[target] = []
  data[target] += [(p,nodes,ns,adds)]

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

if 0:
  plt.rcParams.update({
    "text.usetex": True,
    "font.family": "sans-serif",
    "font.sans-serif": "Helvetica",
  })

linewidth = 0.8
sqrt10 = 3.1622776601683793319988935444327185337

colors = {
  'ladder': 'tab:blue',
  'prac': 'tab:orange',
  'cfrc': 'tab:green',
  'sibc': 'tab:red',
  'ctidh': 'tab:purple',
  'prune': 'tab:brown',
  'mitm': 'tab:pink',
  'mitm2': 'tab:gray',
}

for what in 'len','nodes','ns':
  for average in False,True:
    fig,ax = plt.subplots()

    averagetitle = 'runningavg' if average else ''
    
    ax.set_xscale('log')
    ax.xaxis.set_major_locator(matplotlib.ticker.LogLocator(10,numticks=12))
    ax.xaxis.set_minor_locator(matplotlib.ticker.LogLocator(base=10,subs=(0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9),numticks=12))
    ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())

    if what == 'len':
      ax.set_ylim([1.0,2.1])
      ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(0.05))
      def extract(p,nodes,ns,adds): return adds
      def plot(p,y): return y/math.log(p,2.0)
      plt.title(f'{averagetitle}additions / $\log_2(p)$')
    elif what == 'nodes':
      ax.set_ylim([0.0,2.1])
      ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(0.1))
      def extract(p,nodes,ns,adds): return nodes
      def plot(p,y): return math.log(1+y,2.0)/math.log(p,2.0)
      plt.title(f'$\log_2$(1+{averagetitle}nodes) / $\log_2(p)$')
    elif what == 'ns':
      ax.set_ylim([0.0,5.0])
      ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(0.2))
      def extract(p,nodes,ns,adds): return ns
      def plot(p,y): return math.log(1+y,2.0)/math.log(p,2.0)
      plt.title(f'$\log_2$(1+{averagetitle}ns) / $\log_2(p)$')
    else:
      raise Exception('unknown graph')
    ax.grid(which='both',axis='both',lw=0.3)
    ax.set_axisbelow(True)

    legend_pieces = []

    for target in data:
      color = colors[target]

      marker = (3,2,0)
      if target == 'prac': marker = (3,2,15)
      if target == 'cfrc': marker = (3,2,30)
      if target == 'sibc': marker = (3,2,45)
      if target == 'ctidh': marker = (3,2,60)
      if target == 'prune': marker = (3,2,75)
      if target == 'mitm': marker = (3,2,90)
      if target == 'mitm2': marker = (3,2,105)

      x = [p for p,nodes,ns,adds in data[target]]
      y = list(itertools.starmap(extract,data[target]))
      if average:
        yavg = []
        pos2 = 0
        ysum2 = 0 # sum at positions <pos2
        pos = 0
        ysum = 0 # sum at positions <pos
        while pos < len(x):
          p = x[pos]
          while x[pos2]*2 <= p:
            ysum2 += y[pos2]
            pos2 += 1
          assert pos2 <= pos
          assert x[pos2]*2 > p
          if pos2 > 0: assert x[pos2-1]*2 <= p
          ysum += y[pos]
          pos += 1
          yavg += [(ysum-ysum2)/(pos-pos2)]
        y = yavg
      z = list(itertools.starmap(plot,zip(x,y)))

      if chromium:
        plt.scatter([],[],label=target,marker=marker,lw=linewidth,s=10,color=color)
        for xi,zi in zip(x,z):
          plt.plot([xi],[zi],marker=marker,mew=linewidth,lw=0,ms=sqrt10,color=color)
      else:
        plt.scatter(x,z,label=target,marker=marker,lw=linewidth,s=10,color=color)

      legend_pieces += [matplotlib.lines.Line2D([0],[0],marker=marker,mew=3.0*linewidth,markersize=3.0*sqrt10,lw=0,color=color,label=target)]

    if what == 'len':
      legend = ax.legend(handles=legend_pieces,loc='upper left')
    else:
      legend = ax.legend(handles=legend_pieces,loc='upper right')
    for text in legend.get_texts():
      plt.setp(text,color=colors[text.get_text()])

    fig.tight_layout()
    
    fnpdf = f'plot-{what}-average.pdf' if average else f'plot-{what}.pdf'
    with PdfPages(fnpdf) as pdf:
      pdf.savefig()
      plt.close()
