# Author: André Clérigo Nmec: 98485
# Coded discussed with:
# Bruno Lemos Nmec: 98221
# João Amaral Nmec: 98373
# João Viegas Nmec: 98372
# Pedro Rocha Nmec: 98256

from tree_search import *
from cidades import *

class MyNode(SearchNode):
    def __init__(self, state, parent, depth, cost, heuristic):
        super().__init__(state,parent)
        self.depth = depth
        self.cost = cost
        self.heuristic = heuristic
        self.eval = round(self.cost + self.heuristic)
        self.children = []


class MyTree(SearchTree):
    def __init__(self, problem, strategy='breadth', seed=0): 
        super().__init__(problem, strategy, seed)
        root = MyNode(problem.initial, None, 0, 0, problem.domain.heuristic(problem.initial, problem.goal))
        self.all_nodes = [root]
        self.terminals = 0
        self.solution_tree = None
        self.used_shortcuts = []

    # add lnewnodes to the open nodes according to astar strategy
    def astar_add_to_open(self, lnewnodes):
        self.open_nodes.extend(lnewnodes)
        return self.open_nodes.sort(key = lambda index : self.all_nodes[index].cost + self.all_nodes[index].heuristic)

    def propagate_eval_upwards(self, node):
        best_node = min(node.children, key=lambda node: node.eval)
        node.eval = best_node.eval
        
        if node.parent != None:
            self.propagate_eval_upwards(self.all_nodes[node.parent])

    # search algorithm that supports astar
    def search2(self, atmostonce=False):
        while self.open_nodes != []:
            nodeID = self.open_nodes.pop(0)
            node = self.all_nodes[nodeID]

            if self.problem.goal_test(node.state):
                self.solution = node
                self.terminals = len(self.open_nodes) + 1
                return self.get_path(node)

            lnewnodes = []
            self.non_terminals += 1

            for a in self.problem.domain.actions(node.state):
                newstate = self.problem.domain.result(node.state, a)
                if newstate not in self.get_path(node):
                    newnode = MyNode(newstate, nodeID, node.depth + 1, node.cost + self.problem.domain.cost(node.state, a), self.problem.domain.heuristic(newstate, self.problem.goal))                   
                    # add newnode(child) to his respective parent(node)
                    node.children.append(newnode)
                    # propagate eval attribute to all parents
                    self.propagate_eval_upwards(node)

                    if atmostonce:
                        # flag to check state existence
                        exists = False
                        # check all nodes
                        for n in self.all_nodes:
                            # check if newstate is already added
                            if n.state == newstate:
                                exists = True
                                if n.cost > newnode.cost:
                                    # update node 
                                    n.__init__(newstate, newnode.parent, newnode.depth, newnode.cost, newnode.heuristic)
                                    n.children = newnode.children
                                    # propagate eval attribute to all parents (not working)
                                    # self.propagate_eval_upwards(n)

                        if not exists:
                            self.all_nodes.append(newnode)
                            lnewnodes.append(len(self.all_nodes) - 1)
                    else:
                        self.all_nodes.append(newnode)
                        lnewnodes.append(len(self.all_nodes) - 1)
                    
            self.add_to_open(lnewnodes)
        return None

    def repeated_random_depth(self, numattempts=3, atmostonce=False):
        # set the initial best_tree and best_search
        best_tree = self
        best_search = best_tree.search2(atmostonce)

        for i in range(numattempts):
            # create a new tree
            tree = MyTree(self.problem, 'rand_depth', i)
            # search it
            search = tree.search2(atmostonce)
            # check if it is better
            if tree.solution.cost < best_tree.solution.cost:
                best_tree = tree
                best_search = search
        
        # save the solution_tree as the best_tree
        self.solution_tree = best_tree
        return best_search

    # create a new path for the solution that uses shortcuts
    def make_shortcuts(self):
        # get the list of cities
        path = self.get_path(self.solution)

        # iterate the path and walk through left to right
        for i in range(len(path)):
            # check if index exist for the new shrinked path
            if i >= len(path): 
                break
            location = path[i]
            shortcuts = self.problem.domain.actions(location)

            for shortcut in shortcuts:
                result = shortcut[1]

                if location == shortcut[0] and result in path:
                    result_index = path.index(result)
                    # check if result is after location in path list
                    if result_index - i > 1:
                        self.used_shortcuts.append(shortcut)
                        # delete cities between the shortcut
                        del path[i + 1 : result_index]
                        break

        return path


class MyCities(Cidades):
    def maximum_tree_size(self, depth):   # assuming there is no loop prevention        
        # neighbors list
        neighbors = []

        # for every city coordinates calulate the number of neighbors
        for coord in self.coordinates:
            neighbors.append(len(self.actions(coord)))
        
        # sum elements in list of neighbors
        neighbors_sum = sum(neighbors)
        avg_branching_factor = neighbors_sum/len(neighbors)
        
        return (avg_branching_factor**(depth + 1) -1) / (avg_branching_factor - 1)
