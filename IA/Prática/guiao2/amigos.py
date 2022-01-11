from constraintsearch import *

amigos = ["Andre", "Bernardo", "Claudio"]
objetos = ['Bicicleta', 'Chapeu']

#edges = 
domains = {a: objetos for a in amigos}

cs = ConstraintSearch(domains, None)

print(cs.search())
