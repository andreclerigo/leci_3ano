from constraintsearch import *

region = ['A', 'B', 'C', 'D', 'E']
colors = ['red', 'blue', 'green', 'yellow', 'white']

domains = {r: colors for r in region}

def restricao(r1, c1, r2, c2):
    return c1 != c2

arestas = [ (v, 'E') for v in region if v != 'E' ]
arestas += [ ('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'A') ]
arestas += [ (v2, v1) for (v1, v2) in arestas]

constraints = { a:restricao for a in arestas }

cs = ConstraintSearch(domains, constraints)

print(cs.search())
