

# Guiao de representacao do conhecimento
# -- Redes semanticas
# 
# Inteligencia Artificial & Introducao a Inteligencia Artificial
# DETI / UA
#
# (c) Luis Seabra Lopes, 2012-2020
# v1.9 - 2019/10/20
#


# Classe Relation, com as seguintes classes derivadas:
#     - Association - uma associacao generica entre duas entidades
#     - Subtype     - uma relacao de subtipo entre dois tipos
#     - Member      - uma relacao de pertenca de uma instancia a um tipo
#

class Relation:
    def __init__(self,e1,rel,e2):
        self.entity1 = e1
#       self.relation = rel  # obsoleto
        self.name = rel
        self.entity2 = e2
    def __str__(self):
        return self.name + "(" + str(self.entity1) + "," + \
               str(self.entity2) + ")"
    def __repr__(self):
        return str(self)


# Subclasse Association
class Association(Relation):
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,e2)

#   Exemplo:
#   a = Association('socrates','professor','filosofia')

# Subclasse Subtype
class Subtype(Relation):
    def __init__(self,sub,super):
        Relation.__init__(self,sub,"subtype",super)


#   Exemplo:
#   s = Subtype('homem','mamifero')

# Subclasse Member
class Member(Relation):
    def __init__(self,obj,type):
        Relation.__init__(self,obj,"member",type)

#   Exemplo:
#   m = Member('socrates','homem')

# classe Declaration
# -- associa um utilizador a uma relacao por si inserida
#    na rede semantica
#
class Declaration:
    def __init__(self,user,rel):
        self.user = user
        self.relation = rel
    def __str__(self):
        return "decl("+str(self.user)+","+str(self.relation)+")"
    def __repr__(self):
        return str(self)

#   Exemplos:
#   da = Declaration('descartes',a)
#   ds = Declaration('darwin',s)
#   dm = Declaration('descartes',m)

# classe SemanticNetwork
# -- composta por um conjunto de declaracoes
#    armazenado na forma de uma lista
#
class SemanticNetwork:
    def __init__(self,ldecl=None):
        self.declarations = [] if ldecl==None else ldecl
    
    def __str__(self):
        return str(self.declarations)
    
    def insert(self,decl):
        self.declarations.append(decl)
    
    def query_local(self,user=None,e1=None,rel=None,e2=None):
        self.query_result = \
            [ d for d in self.declarations
                if  (user == None or d.user==user)
                and (e1 == None or d.relation.entity1 == e1)
                and (rel == None or d.relation.name == rel)
                and (e2 == None or d.relation.entity2 == e2) ]
        return self.query_result
    
    def show_query_result(self):
        for d in self.query_result:
            print(str(d))

    def list_associations(self):
        return list(set([ d.relation.name for d in self.declarations if isinstance(d.relation, Association) ]))

    def list_objects(self):
        return list(set([ d.relation.entity1 for d in self.declarations if isinstance(d.relation, Member) ]))

    def list_users(self):
        return list(set([ d.user for d in self.declarations ]))

    def list_types(self):
        return list(set([ d.relation.entity1 for d in self.declarations if isinstance(d.relation, Subtype) ] + 
                        [ d.relation.entity2 for d in self.declarations if isinstance(d.relation, Subtype) 
                                                                        or isinstance(d.relation, Member) ]))

    def list_local_associations(self, entity):
        return list(set([ d.relation.name for d in self.declarations if d.relation.entity1 == entity and isinstance(d.relation, Association)]))
    
    def list_relations_by_user(self, user):
        return list(set([ d.relation.name for d in self.declarations if d.user == user ]))

    def associations_by_user(self, user):
        return len( list(set([ d.relation.name for d in self.declarations if d.user == user and isinstance(d.relation, Association) ])) )

    def list_local_associations_by_user(self, entity):
        return list(set([ (d.relation.name, d.user) for d in self.declarations if d.relation.entity1 == entity and isinstance(d.relation, Association) ]))
    
    def predecessor(self, prd, dsc):
        ldeclartions = self.query_local(e1=dsc)
        lparents = [ d.relation.entity2 for d in ldeclartions if not isinstance(d.relation, Association) ]

        if prd in lparents:
            return True
        
        for p in lparents:
            if prd == p or self.predecessor(prd, p):
                return True

        return False

    def predecessor_path(self, prd, dsc):
        ldeclartions = self.query_local(e1=dsc)
        lparents = [ d.relation.entity2 for d in ldeclartions if not isinstance(d.relation, Association) ]

        if prd in lparents:
            return [prd, dsc]
        
        for p in lparents:
            path = self.predecessor_path(prd, p)
            if  path != None:
                return path + [dsc]

        return None

    def query(self, entity, association_name=None):
        ldeclartions = self.query_local(e1=entity)
        lparents = [ d.relation.entity2 for d in ldeclartions if not isinstance(d.relation, Association) ]

        lassoc = [ d for d in ldeclartions if isinstance(d.relation, Association) 
                                            and (d.relation.name == association_name or association_name == None) ]
        
        for p in lparents:
            lassoc += self.query(p, association_name)
        return lassoc

    def query2(self, entity, relation_name=None):
        query_result = self.query(entity)

        ldeclartions = self.query_local(e1=entity)
        lassoc = [ d for d in ldeclartions if not isinstance(d.relation, Association) 
                                            and (d.relation.name == relation_name or relation_name == None) ]

        return query_result + lassoc

    def query_cancel(self, entity, association_name):
        ldeclartions = self.query_local(e1=entity)
        lparents = [ d.relation.entity2 for d in ldeclartions if not isinstance(d.relation, Association) ]

        lassoc = [ d for d in ldeclartions if isinstance(d.relation, Association) and d.relation.name == association_name ]
        
        if lassoc == []:
            for p in lparents:
                lassoc += self.query_cancel(p, association_name)

        print(f'lassoc: {lassoc}')
        return lassoc

    def query_down(self, entity, association_name, child=False):
        ldeclartions = self.query_local(e2=entity)
        lchildren = [ d.relation.entity1 for d in ldeclartions if not isinstance(d.relation, Association) ]

        lassoc = []
        if child:
            lassoc = [ d for d in self.query_local(e1=entity) if isinstance(d.relation, Association) 
                                                                and d.relation.name == association_name ]
    
        for c in lchildren:
            lassoc += self.query_down(c, association_name, child=True)

        return lassoc
        