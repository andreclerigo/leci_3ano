#encoding: utf8


from tpi2 import *

# ----------------------------------------------------------------------
# Redes semânticas
# ----------------------------------------------------------------------

## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
z = MySemNet()
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
z.insert('confidenceengineer',Subtype('cartooncharacter','animate'))
z.insert('confidenceengineer',AssocOne('cartooncharacter','vocalization','speech'))
z.insert('simao',AssocOne('cartooncharacter','vocalization','squawks'))
##
z.insert('confidenceengineer',Subtype('animal','animate'))
##
z.insert('confidenceengineer',Subtype('vertebrate','animal'))
z.insert('confidenceengineer',AssocOne('vertebrate','hasmother','female'))
z.insert('confidenceengineer',AssocOne('vertebrate','feeding','herbivore'))
##
z.insert('knowledgeengineer',Subtype('bird','vertebrate'))
##
z.insert('confidenceengineer',Subtype('penguin','bird'))
z.insert('confidenceengineer',AssocOne('penguin','vocalization','squawks'))
z.insert('ursula',AssocOne('penguin','vocalization','gluglu'))
##
z.insert('descartes',Subtype('mammal','vertebrate'))
z.insert('darwin',Subtype('mammal','vertebrate'))
z.insert('confidenceengineer',AssocOne('mammal','numlegs',4))
z.insert('ursula',AssocOne('mammal','numlegs',6))
z.insert('confidenceengineer',AssocOne('mammal','feeding','carnivore'))
z.insert('ursula',AssocOne('mammal','feeding','herbivore'))
##
z.insert('knowledgeengineer',Subtype('marsupial','mammal'))
z.insert('confidenceengineer',AssocOne('marsupial','feeding','herbivore'))
##
z.insert('knowledgeengineer',Subtype('feline','mammal'))
z.insert('confidenceengineer',AssocOne('feline','numlegs',4))
##
z.insert('knowledgeengineer',Subtype('lion','feline'))
z.insert('confidenceengineer',AssocOne('lion','feeding','carnivore'))
##
z.insert('knowledgeengineer',Subtype('cat','feline'))
##
z.insert('knowledgeengineer',Subtype('tiger','feline'))
##
z.insert('knowledgeengineer',Subtype('primate','mammal'))
z.insert('confidenceengineer',AssocOne('primate','feeding','omnivore'))
z.insert('confidenceengineer',AssocOne('primate','likesphilosophy',False))
##
z.insert('knowledgeengineer',Subtype('human','primate'))
z.insert('confidenceengineer',AssocOne('human','numlegs',2))
z.insert('manuel',AssocOne('human','numlegs',2))
z.insert('confidenceengineer',AssocOne('human','feeding','omnivore'))
##
z.insert('confidenceengineer',Subtype('man','human'))
z.insert('confidenceengineer',Subtype('man','male'))
##
z.insert('confidenceengineer',Subtype('woman','human'))
z.insert('confidenceengineer',Subtype('woman','female'))
##
z.insert('confidenceengineer',AssocOne('philosopher','likesphilosophy',True))
##
z.insert('descartes',Member('socrates','man'))
z.insert('damasio',Member('socrates','philosopher'))
z.insert('knowledgeengineer',AssocOne('socrates','hasFather','pericles'))
z.insert('aristotle',AssocOne('socrates','hasFather','plato'))
z.insert('descartes',AssocSome('socrates','professorOf','philosophy'))
z.insert('descartes',AssocSome('socrates','professorOf','mathematics'))
z.insert('simao',AssocSome('socrates','professorOf','mathematics'))
##
z.insert('descartes',Member('plato','man'))
z.insert('knowledgeengineer',AssocOne('plato','hasFather','pericles'))
z.insert('descartes',AssocSome('plato','professorOf','philosophy'))
z.insert('simao',AssocSome('plato','professorOf','philosophy'))
##
z.insert('descartes',Member('aristotle','man'))
z.insert('simao',AssocOne('aristotle','hasFather','ariston'))
z.insert('manuel',AssocOne('aristotle','hasFather','nicomachus'))
z.insert('antonio',AssocOne('aristotle','hasFather','nicomachus'))
##
z.insert('confidenceengineer',Member('madonna','woman'))
z.insert('confidenceengineer',AssocOne('madonna','livingstate','alive'))
z.insert('simao',AssocOne('madonna','livingstate','alive'))
z.insert('ursula',AssocOne('madonna','livingstate','dead'))
z.insert('confidenceengineer',AssocOne('madonna','livingplace','sintra'))
z.insert('simao',AssocOne('madonna','livingplace','sintra'))
z.insert('manuel',AssocOne('madonna','livingplace','oeiras'))
z.insert('antonio',AssocOne('madonna','livingplace','aveiro'))
z.insert('ursula',AssocOne('madonna','livingplace','lisboa'))
z.insert('teresa',AssocOne('madonna','livingplace','newyork'))
##
z.insert('confidenceengineer',Member('prince','man'))
z.insert('confidenceengineer',AssocOne('prince','livingstate','dead'))
z.insert('simao',AssocOne('prince','livingstate','alive'))
##
z.insert('confidenceengineer',Member('opus','penguin'))
z.insert('confidenceengineer',Member('opus','cartooncharacter'))
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##


users = [ 'simao', 'ursula', 'manuel', 'confidenceengineer', 'knowledgeengineer' ]

for user in users:
    print(user,":",z.source_confidence(user))

print("..........................................................")

query_cases = [ ('philosopher','likesphilosophy'),
                ('man','likesphilosophy'),
                ('socrates','likesphilosophy'),
                ('opus','vocalization'),
                ('madonna','livingplace'),
                ('madonna','feeding'),
                ('prince','livingstate'),
                ('prince','numlegs') 
]

for (entity,relname) in query_cases:
    print(entity,"/",relname,":",z.query_with_confidence(entity,relname))

print("..........................................................")

# ----------------------------------------------------------------------
# Redes de Bayes
# ----------------------------------------------------------------------

bn = MyBN()

bn.add('a',[],0.003)

bn.add('b_a',[],0.002)

bn.add('c_s',[('a',True )],0.48)
bn.add('c_s',[('a',False)],0.08)

bn.add('d',[],0.01)

bn.add('m_f',[],0.01)

bn.add('b_v',[('c_s',True ),('b_a',True )],0.18)
bn.add('b_v',[('c_s',True ),('b_a',False)],0.02)
bn.add('b_v',[('c_s',False),('b_a',True )],0.90)
bn.add('b_v',[('c_s',False),('b_a',False)],0.68)

bn.add('s_m',[],0.05)

bn.add('s_p',[],0.3)

bn.add('v_p',[('m_f',True),('d',True ),('b_v',True )],0.003)
bn.add('v_p',[('m_f',True),('d',True ),('b_v',False )],0.12)
bn.add('v_p',[('m_f',True),('d',False ),('b_v',True)],0.08)
bn.add('v_p',[('m_f',True),('d',False),('b_v',False )],0.01)
bn.add('v_p',[('m_f',False),('d',True),('b_v',True)],0.04)
bn.add('v_p',[('m_f',False),('d',True ),('b_v',False)],0.07)
bn.add('v_p',[('m_f',False),('d',False),('b_v',True )],0.13)
bn.add('v_p',[('m_f',False),('d',False),('b_v',False)],0.09)

bn.add('h',[('b_v',True )],0.44)
bn.add('h',[('b_v',False)],0.89)

bn.add('s_s',[('s_m',True),('m_f',True ),('b_v',True )],0.3)
bn.add('s_s',[('s_m',True),('m_f',True ),('b_v',False )],0.21)
bn.add('s_s',[('s_m',True),('m_f',False ),('b_v',True)],0.34)
bn.add('s_s',[('s_m',True),('m_f',False),('b_v',False )],0.12)
bn.add('s_s',[('s_m',False),('m_f',True),('b_v',True)],0.15)
bn.add('s_s',[('s_m',False),('m_f',True ),('b_v',False)],0.14)
bn.add('s_s',[('s_m',False),('m_f',False),('b_v',True )],0.132)
bn.add('s_s',[('s_m',False),('m_f',False),('b_v',False)],0.44)

bn.add('s_t',[('d',True )],0.08)
bn.add('s_t',[('d',False)],0.002)

bn.add('s_q',[('s_p',True ),('v_p',True )],0.008)
bn.add('s_q',[('s_p',True ),('v_p',False)],0.4)
bn.add('s_q',[('s_p',False),('v_p',True )],0.51)
bn.add('s_q',[('s_p',False),('v_p',False)],0.13)

bn.add('f_s',[],0.1)

bn.add('c_c',[('s_s',True )],0.49)
bn.add('c_c',[('s_s',False)],0.023)

bn.add('car_s',[('c_c',True),('s_t',True),('s_q',True ),('f_s',True )],0.091)
bn.add('car_s',[('c_c',True),('s_t',True),('s_q',True ),('f_s',False )],0.081)
bn.add('car_s',[('c_c',True),('s_t',True),('s_q',False ),('f_s',True )],0.045)
bn.add('car_s',[('c_c',True),('s_t',True),('s_q',False ),('f_s',False )],0.065)
bn.add('car_s',[('c_c',True),('s_t',False),('s_q',True ),('f_s',True)],0.087)
bn.add('car_s',[('c_c',True),('s_t',False),('s_q',True),('f_s',False )],0.043)
bn.add('car_s',[('c_c',True),('s_t',False),('s_q',False ),('f_s',True)],0.035)
bn.add('car_s',[('c_c',True),('s_t',False),('s_q',False),('f_s',False )],0.067)
bn.add('car_s',[('c_c',False),('s_t',True),('s_q',True),('f_s',True)],0.052)
bn.add('car_s',[('c_c',False),('s_t',True),('s_q',True),('f_s',False)],0.054)
bn.add('car_s',[('c_c',False),('s_t',True),('s_q',False),('f_s',True)],0.056)
bn.add('car_s',[('c_c',False),('s_t',True),('s_q',False),('f_s',False)],0.078)
bn.add('car_s',[('c_c',False),('s_t',False),('s_q',True),('f_s',True )],0.045)
bn.add('car_s',[('c_c',False),('s_t',False),('s_q',True),('f_s',False)],0.031)
bn.add('car_s',[('c_c',False),('s_t',False),('s_q',False),('f_s',True )],0.034)
bn.add('car_s',[('c_c',False),('s_t',False),('s_q',False),('f_s',False)],0.023)



result = bn.individual_probabilities()
print('Individual probabilities:',result)




