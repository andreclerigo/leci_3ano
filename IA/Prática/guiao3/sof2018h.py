from bayes_net import *

bn = BayesNet()

variables = ['sc', 'pt', 'cp', 'fr', 'pa', 'cnl']

bn.add('sc', [], 0.6)
bn.add('pt', [], 0.05)

bn.add('cnl', [('sc', True)], 0.9)
bn.add('cnl', [('sc', False)], 0.001)

bn.add('cp', [('st', True), ('pa', True)], 0.02)
bn.add('cp', [('st', False), ('pa', True)], 0.011)
bn.add('cp', [('st', True), ('pa', False)], 0.01)
bn.add('cp', [('st', False), ('pa', False)], 0.001)

bn.add('pa', [('pt', True)], 0.25)
bn.add('pa', [('pt', False)], 0.004)

bn.add('fr', [('pt', True), ('pa', True)], 0.9)
bn.add('fr', [('pt', True), ('pa', False)], 0.9)
bn.add('fr', [('pt', False), ('pa', True)], 0.1)
bn.add('fr', [('pt', False), ('pa', False)], 0.01)

conjunction = [('sc', True), ('pt', True), ('cp', True), ('fr', True), ('pa', True), ('cnl', True)]
conjunction_false = [('sc', False), ('pt', False), ('cp', False), ('fr', False), ('pa', False), ('cnl', False)]

print(bn.jointProb(conjunction))
print(bn.jointProb(conjunction_false))
assert bn.jointProb([('sc', True)]) == round(bn.individualProb('sc', True),5)
assert bn.jointProb([('pt', False)]) == round(bn.individualProb('pt', False),5)
