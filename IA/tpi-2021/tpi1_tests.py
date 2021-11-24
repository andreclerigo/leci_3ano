

#import math

from tpi1 import *

cidades_portugal = MyCities( 
                    # Ligacoes por estrada
                    [
                      ('Coimbra', 'Leiria', 73),
                      ('Aveiro', 'Agueda', 35),
                      ('Porto', 'Agueda', 79),
                      ('Agueda', 'Coimbra', 45),
                      ('Viseu', 'Agueda', 78),
                      ('Aveiro', 'Porto', 78),
                      ('Aveiro', 'Coimbra', 65),
                      ('Figueira', 'Aveiro', 77),
                      ('Braga', 'Porto', 57),
                      ('Viseu', 'Guarda', 75),
                      ('Viseu', 'Coimbra', 91),
                      ('Figueira', 'Coimbra', 52),
                      ('Leiria', 'Castelo Branco', 169),
                      ('Figueira', 'Leiria', 62),
                      ('Leiria', 'Santarem', 78),
                      ('Santarem', 'Lisboa', 82),
                      ('Santarem', 'Castelo Branco', 160),
                      ('Castelo Branco', 'Viseu', 174),
                      ('Santarem', 'Evora', 122),
                      ('Lisboa', 'Evora', 132),
                      ('Evora', 'Beja', 105),
                      ('Lisboa', 'Beja', 178),
                      ('Faro', 'Beja', 147),
                      # extra
                      ('Braga', 'Guimaraes', 25),
                      ('Porto', 'Guimaraes', 44),
                      ('Guarda', 'Covilha', 46),
                      ('Viseu', 'Covilha', 57),
                      ('Castelo Branco', 'Covilha', 62),
                      ('Guarda', 'Castelo Branco', 96),
                      ('Lamego','Guimaraes', 88),
                      ('Lamego','Viseu', 47),
                      ('Lamego','Guarda', 64),
                      ('Portalegre','Castelo Branco', 64),
                      ('Portalegre','Santarem', 157),
                      ('Portalegre','Evora', 194) ],

                    # City coordinates
                     { 'Aveiro': (41,215),
                       'Figueira': ( 24, 161),
                       'Coimbra': ( 60, 167),
                       'Agueda': ( 58, 208),
                       'Viseu': ( 104, 217),
                       'Braga': ( 61, 317),
                       'Porto': ( 45, 272),
                       'Lisboa': ( 0, 0),
                       'Santarem': ( 38, 59),
                       'Leiria': ( 28, 115),
                       'Castelo Branco': ( 140, 124),
                       'Guarda': ( 159, 204),
                       'Evora': (120, -10),
                       'Beja': (125, -110),
                       'Faro': (120, -250),
                       #extra
                       'Guimaraes': ( 71, 300),
                       'Covilha': ( 130, 175),
                       'Lamego' : (125,250),
                       'Portalegre': (130,170) }
                     )


p = SearchProblem(cidades_portugal,'Braga','Faro')

print("\n-- ## Ex. 1 --------------------------------")

print(cidades_portugal.maximum_tree_size(3))
print(cidades_portugal.maximum_tree_size(6))

print("\n-- ## Ex. 2 --------------------------------")

t = MyTree(p,'A*')
print(t.search2())
print(t.non_terminals,t.terminals)

print("\n-- ## Ex. 3 --------------------------------")

t = MyTree(p,'rand_depth')
print(t.repeated_random_depth(8))
print(t.solution_tree.solution.cost)
print(t.solution_tree.non_terminals, t.solution_tree.terminals)

print("\n-- ## Ex. 4 --------------------------------")

t = MyTree(p,'depth')
print(t.search2())
print(t.all_nodes[0].heuristic)
print(t.solution.cost)
print(t.all_nodes[0].eval)
print(t.non_terminals,t.terminals)

t = MyTree(p,'A*')
print(t.search2())
print(t.all_nodes[0].heuristic)
print(t.solution.cost)
print(t.all_nodes[0].eval)
print(t.non_terminals,t.terminals)

print("\n-- ## Ex. 5 --------------------------------")

t = MyTree(p,'depth')
print(t.search2(True))
print(t.all_nodes[0].heuristic)
print(t.solution.cost)
#print(t.all_nodes[0].eval)
print(t.non_terminals,t.terminals)

t = MyTree(p,'A*')
print(t.search2(True))
print(t.all_nodes[0].heuristic)
print(t.solution.cost)
#print(t.all_nodes[0].eval)
print(t.non_terminals,t.terminals)

print("\n-- ## Ex. 6 --------------------------------")

t = MyTree(p,'depth')
print(t.search2())
print(t.non_terminals,t.terminals)
print(t.make_shortcuts())
print(t.used_shortcuts)


