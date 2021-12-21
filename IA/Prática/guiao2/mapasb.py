from constraintsearch import *

region = ['A', 'B', 'C', 'D', 'E', 'F']
colors = ['red', 'blue', 'green', 'yellow', 'white']

edges = [('E', r) for r in region if r != 'E']
edges += [('A', 'B'), ('B', 'C'), ('C', 'F'), ('F', 'D'), ('D', 'A')]
edges += [(r1, r2) for (r2, r1) in edges]

domains = {r: colors for r in region}
constraints = {e:(lambda r1, c1, r2, c2: c1 != c2) for e in edges}

cs = ConstraintSearch(domains, constraints)

print(cs.search())
