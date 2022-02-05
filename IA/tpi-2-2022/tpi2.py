#encoding: utf8
# Author: André Clérigo Nmec: 98485
# Coded discussed with:
# Bruno Lemos Nmec: 98221
# Claudio Asensio Nmec: 98433
# João Amaral Nmec: 98373
# João Viegas Nmec: 98372
# Pedro Rocha Nmec: 98256


from semantic_network import *
from bayes_net import *
from collections import Counter

class MySemNet(SemanticNetwork):
    def __init__(self):
        SemanticNetwork.__init__(self)
        pass

    def source_confidence(self, user):
        correct = 0
        wrong = 0

        # The method collects all declarations of AssocOne relations introduced by the given user
        ldecl = [d for d in self.declarations if isinstance(d.relation, AssocOne) and d.user == user]

        for decl in ldecl:
            # The method collects all declarations of AssocOne relations introduced by other users
            ldecl_total = [d for d in self.declarations if isinstance(d.relation, AssocOne)]

            # The method collects all relations of AssocOne relations introduced by all users,
            # which have the same first argument as the one declared by the given user
            # and which have the same relation name as the one declared by the given user
            lrel_same_e1_same_relname = [d.relation.__repr__() for d in ldecl_total if d.relation.entity1 == decl.relation.entity1 and d.relation.name == decl.relation.name]

            # Get a tuple with the most common relations
            lrel_counter = Counter(lrel_same_e1_same_relname)
            lcommon = lrel_counter.most_common(2)

            if len(lcommon) == 1:                                   # There is only one declaration, correct!
                correct += 1
            else:
                if lcommon[0][1] == lcommon[1][1]:                  # There is a tie, correct!
                    correct += 1
                else:
                    if lcommon[0][0] == decl.relation.__repr__():   # The decl is the most common, correct!
                        correct += 1
                    else:
                        wrong += 1
            
        
        return (1 - 0.75**correct)*(0.75**wrong)

    def query_with_confidence(self, entity, assoc):
        # Get all entity1 declarations
        ldeclartions = self.query_local(e1=entity)
        # Filter the declarations to get only AssocOne declarations
        lrel_str = [d.relation.__repr__() for d in ldeclartions if isinstance(d.relation, AssocOne) and d.relation.name == assoc]
        lrel = [d.relation for d in ldeclartions if isinstance(d.relation, AssocOne) and d.relation.name == assoc]
        t = len(lrel_str)

        # Count the number of occurrences of rel in entity
        lrel_counter = Counter(lrel_str)
        
        # Associate an assoc entity2 with a confidence value
        local_confidence_dict = {}
        for rel in lrel:
            n = lrel_counter[rel.__repr__()]
            local_confidence = (n / (2*t)) + (1 - (n / (2*t))) * (1 - (0.95**n))*(0.95**(t-n))            
            local_confidence_dict[rel.entity2] = local_confidence

        # Get all parents (no duplicates)
        lparents = list(set([d.relation.entity2 for d in ldeclartions if not isinstance(d.relation, AssocOne) and not isinstance(d.relation, AssocSome)]))

        # Sum the confidence values for each parent
        inherited_confidence_dict = {}
        for p in lparents:
            query_res = self.query_with_confidence(p, assoc)
            for k,v in query_res.items():
                if k in inherited_confidence_dict:
                    inherited_confidence_dict[k] += v
                else:
                    inherited_confidence_dict[k] = v

        # Average the confidence values for each entity2
        inherited_confidence_dict.update((k, v/len(lparents)) for k, v in inherited_confidence_dict.items())

        # If there are no inherited results, the local results should be returned.
        if inherited_confidence_dict == {}:
            return local_confidence_dict

        # If there are no local results, the inherited results should be returned with a discount of 10%
        if local_confidence_dict == {}:
            inherited_confidence_dict.update((k, v*0.9) for k, v in inherited_confidence_dict.items())
            return inherited_confidence_dict
        
        # In all other cases, the final confidence values are computed by weighted average, with 0.9 for the local confidences and 0.1 for the inherited confidences 
        # Sum and merge the two dictionaries
        return {k: inherited_confidence_dict.get(k, 0)*0.1 + local_confidence_dict.get(k, 0)*0.9 for k in set(inherited_confidence_dict) | set(local_confidence_dict)}

class MyBN(BayesNet):
    def __init__(self):
        BayesNet.__init__(self)
        pass

    def conjunct(self, variables):
        if variables == []:
            return [[]]
        
        lconjunct = []

        # Get all conjuncts of the first variable (True and False)
        # and add them to the list of conjuncts
        for sublst in [ [[(variables[0], False)] + conj, [(variables[0], True)] + conj] 
                    for conj in self.conjunct(variables[1:]) ]:
            for _ in sublst:
                lconjunct.append(_)

        return lconjunct

    def mothers(self, var):
        ancestors = { v for (v, _) in list(self.dependencies[var].keys())[0] }
        all_ancestors = ancestors.copy()
        
        # Get all ancestors of ancestors
        for v in ancestors:
            all_ancestors.update(self.mothers(v))

        return list(all_ancestors)
    
    def individual_probabilities(self):
        probs = {}

        # Iterate over all variables
        for var in self.dependencies:
            mothers = self.mothers(var)

            # Check if the variable is a root
            if mothers == []:
                probs[var] = self.dependencies[var][frozenset()]
                continue
            
            # Get the conjuncts of the mothers
            all_conjuncts = self.conjunct(mothers)
            var_prob = 0

            # Iterate over all conjuncts
            for conj in all_conjuncts:
                var_prob += self.jointProb([(var, True)] + conj)
            probs[var] = var_prob      

        return probs
