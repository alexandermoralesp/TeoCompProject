from regularexp import RegularExp

class Automata:
    AEE_algo = "AEE"
    HDM_algo = "HDM"
    NCE_algo = "NCE"
    NCD_algo = "NCD"

    def __init__(self, n, start_state, end_state_list, transition_list, debug=False):
        self.debug = debug

        # Create Adjacency Matrix
        self.adjacency_matrix = [[None for i in range(n+2)] for j in range(n+2)]
        # TRANSITION TUPLE
        # => str:regex, bool:RequiresParenthesis

        # Initalize normalized state
        # Normalized Start: n
        # Normalized End: n+1
        normalized_start_index = n
        normalized_end_index = n+1

        self.adjacency_matrix[normalized_start_index][start_state] = RegularExp("e") # Epsilon
        for state in end_state_list:
            self.adjacency_matrix[state][normalized_end_index] = RegularExp("e") # Epsilon transition


        # Inicializar transiciones
        for (state, transition, next) in transition_list:
            self.add_transition(state, transition, next)

        # Contador de operaciones
        self.operations = 0
        
    def add_transition(self, state, transition, next): # Método para añadir un estado al automata
        if self.adjacency_matrix[state][next] is None: 
            # New Transition
            self.adjacency_matrix[state][next] = RegularExp(str(transition), False)
        else:
            # NORMALIZACION de doble transicion
            self.adjacency_matrix[state][next] = RegularExp(str(transition), False)+self.adjacency_matrix[state][next]

    def display(self):
        print(end="\t")
        for j in range( len(self.adjacency_matrix[0]) ):
            print( j, end="\t")
        print()

        for i in range( len(self.adjacency_matrix) ):
            print(i, end = "\t")
            for j in range( len(self.adjacency_matrix[0]) ):
                print( self.adjacency_matrix[i][j], end="\t")
            print()
    
    # GENERAL CALL:
    def get_regular_expression(self, algo):
        if (algo==Automata.AEE_algo):
            return self.get_regular_expression_AEE()
        elif (algo==Automata.HDM_algo):
            return self.get_regular_expression_HDM()
        elif (algo==Automata.NCE_algo):
            return self.get_regular_expression_NCE()
        elif (algo==Automata.NCD_algo):
            return self.get_regular_expression_NCD()
        else:
            print("Algoritmo escogido invalido")
            return None


    # PREGUNTA 1:
    def get_regular_expression_AEE(self):
        n = len(self.adjacency_matrix)

        for s in range( n -2):
            # s = estado a remover

            # Declarando elemento de loop (*)
            if self.adjacency_matrix[s][s] is None:
                loop = RegularExp("", False)
            else:
                loop = self.adjacency_matrix[s][s].star()

            # Lista de todas las entras y salidas validas
            in_transitions = [i for i in range(s+1,n) if self.adjacency_matrix[i][s] is not None]
            out_transitions = [o for o in range(s+1,n) if self.adjacency_matrix[s][o] is not None]

            # Combinacion de todas las entradas validas con todas las salidas valdias
            for i in in_transitions:
                for o in out_transitions:
                    if self.adjacency_matrix[i][o] is None:
                        self.adjacency_matrix[i][o] = self.adjacency_matrix[i][s] ^ loop ^  self.adjacency_matrix[s][o] 
                    else:
                        self.adjacency_matrix[i][o] = self.adjacency_matrix[i][o] +  (self.adjacency_matrix[i][s] ^ loop ^ self.adjacency_matrix[s][o])

             # Contador de operaciones
            self.operations += len(in_transitions) * len(out_transitions)
            
        return self.adjacency_matrix[n-2][n-1]

    # PREGUNTA 2:
    def get_regular_expression_HDM(self):
        # List of active states and iterable states
        n = len(self.adjacency_matrix)
        active_states = [i for i in range(n-2)]
        iterbale_states = [i for i in range(n)]

        for s in range( n - 2):
            ## TEST LOOP COUNTING:
            #print(self.count_cycles(active_states))
            #print("\n\n\n\n\n")


            # Get state of minimum weight
            minimum_weight_state = None
            minimum_weight_value = None
            for s in active_states:
                l = 0
                m = 0
                in_sum = 0
                out_sum = 0
                loop_len = 0

                for j in iterbale_states:
                    if (j == s):
                        # Loop
                        if (self.adjacency_matrix[s][s] is not None):
                            loop_len += len(self.adjacency_matrix[s][s])
                    else:
                        # In
                        if (self.adjacency_matrix[j][s] is not None):
                            m += 1
                            in_sum += len(self.adjacency_matrix[j][s])
                        # Out
                        if (self.adjacency_matrix[s][j] is not None):
                            l += 1
                            out_sum += len(self.adjacency_matrix[s][j])
                state_w = ((l-1) * in_sum) + ((m-1)*out_sum) + ((m*l - 1) * loop_len)
                if minimum_weight_state is None:
                    minimum_weight_state = s
                    minimum_weight_value = state_w
                elif minimum_weight_value > state_w:
                    minimum_weight_state = s
                    minimum_weight_value = state_w
            
            ## Delete state of minimum weight
            s = minimum_weight_state
            # Declarando elemento de loop (*)
            if self.adjacency_matrix[s][s] is None:
                loop = RegularExp("", False)
            else:
                loop = self.adjacency_matrix[s][s].star()
            # Delete currently deleting from iterables
            iterbale_states.remove(s)

            # Lista de todas las entras y salidas validas
            in_transitions = [i for i in iterbale_states if self.adjacency_matrix[i][s] is not None]
            out_transitions = [o for o in iterbale_states if self.adjacency_matrix[s][o] is not None]

            # Combinacion de todas las entradas validas con todas las salidas valdias
            for i in in_transitions:
                for o in out_transitions:
                    if self.adjacency_matrix[i][o] is None:
                        self.adjacency_matrix[i][o] = self.adjacency_matrix[i][s] ^ loop ^  self.adjacency_matrix[s][o] 
                    else:
                        self.adjacency_matrix[i][o] = self.adjacency_matrix[i][o] +  (self.adjacency_matrix[i][s] ^ loop ^ self.adjacency_matrix[s][o])
             # Contador de operaciones
            self.operations += len(in_transitions) * len(out_transitions)

            # Delete from lists
            active_states.remove(s)

            ### DEBUG:
            if self.debug:
                print("W of delete: {}".format(minimum_weight_value))

        return self.adjacency_matrix[n-2][n-1]

    # PREGUNTA 3:
    def count_cycles_(self, iterbale_states):
        # O(n^2): Adycacency list
        ady_list = {a:[] for a in iterbale_states}
        for i in iterbale_states:
            for o in iterbale_states:
                if (self.adjacency_matrix[i][o] is not None):
                    ady_list[i].append(o)

        # O(n)*O(n) = O(n^2): Counting por estado
        count_dict = {}       
        for node in iterbale_states:
            # O(v+e) = O(v+2v) = O(v) = O(n): DFS counting cycles
            loops = {i:None for i in ady_list}
            loops[node] = True
            count, _ = self.count_cycle_dfs(ady_list, loops, node, node, 0)
            # Save
            count_dict[node] = count
        return count_dict

    def count_cycle_dfs(self, ady_list, loops, node, objective, count):
        # Temporarily set current node as dead end (Unless it is origin)
        if (objective != node):
            loops[node] = False
            current_loops = False
        # Loop
        for s in ady_list[node]:
            if loops[s] is None: 
                # Needs to be explored
                count, temp = self.count_cycle_dfs(ady_list, loops, s, objective, count)
                if (temp):
                    current_loops = True
            elif loops[s] is True: 
                # Next node loops
                count += 1
                current_loops = True
            else: #loops[s] is False: 
                # Next node is dead end
                pass
        # Set current node to appropiate loop status
        if (objective != node):
            loops[node] = current_loops
        # Return count
        return count, loops[node]

    def count_cycles_jhonson(self, iterbale_states):
        # O(n^2): Adycacency list
        ady_list = {a:[] for a in iterbale_states}
        for i in iterbale_states:
            for o in iterbale_states:
                if (self.adjacency_matrix[i][o] is not None):
                    ady_list[i].append(o)
        #print("\n\n\nADY LIST:", ady_list)
        # O((v+e) * c): JHONSON ALL CYCLES
        cycles_count = {a:0 for a in iterbale_states}
        for start in iterbale_states:
            # Inicializar stack con inicio en start
            stack = []
            blocked_set = {}
            blocked_map = {}

            # Rec jhonson
            self.count_cycles_jhonson_rec(start, ady_list, stack, blocked_set, blocked_map, cycles_count)
            # Al terminar de iterar con este valor en start. Eliminarlo del grafo
            ady_list.pop(start)

        ### DEBUG:
        if self.debug:
            print("Dict de cycle counts: {}".format(cycles_count))
        return cycles_count

    def count_cycles_jhonson_rec(self, current, adj_list, stack, blocked_set, blocked_map, cycles_count):
        if not adj_list.get(current):
            return        
        # Actualizar data structures
        stack.append(current)
        blocked_set[current] = True
        start = stack[0]
        cycle = False
        # Exploracion recursiva
        for node in adj_list[current]:
            #print("START:{} - current:{} -> node:{}".format(start, current, node))
            #print("BLOCKED SET:", blocked_set)
            #print("BLOCKED MAP:", blocked_map)
            if node == start:
                # Is cycle
                #print( "CYCLE:", stack)
                for i in stack:
                    cycles_count[i] += 1
                cycle = True 
            elif blocked_set.get(node) is not True:
                # Needs to be explore
                if self.count_cycles_jhonson_rec(node, adj_list, stack, blocked_set, blocked_map, cycles_count):
                    cycle = True
        # End
        if cycle:
            self.unblock_rec(current, blocked_set, blocked_map)
        else:
            for node in adj_list[current]:
                if node != current: # Edge case: Self cycles
                    if blocked_map.get(node):
                        blocked_map[node].append(current)
                    else:
                        blocked_map[node] = [current,]
        stack.pop()
        return cycle

    def unblock_rec(self, current, blocked_set, blocked_map):
        blocked_set[current] = False
        if blocked_map.get(current):
            while blocked_map[current] != []:
                node = blocked_map[current].pop()
                self.unblock_rec(node, blocked_set, blocked_map)


            



    def count_cycles_fix(self, iterbale_states):
        # O(n^2): Adycacency list
        ady_list = {a:[] for a in iterbale_states}
        for i in iterbale_states:
            for o in iterbale_states:
                if (self.adjacency_matrix[i][o] is not None):
                    ady_list[i].append(o)

        # O(n)*O(n) = O(n^2): Counting por estado
        count_dict = {}       
        for node in iterbale_states:
            # O(v+e) = O(v+2v) = O(v) = O(n): DFS counting cycles
            loops = {i:None for i in ady_list}
            loops[node] = 1
            count = self.count_cycle_dfs_fix(ady_list, loops, node, node)
            # Save
            count_dict[node] = count
        return count_dict

    def count_cycle_dfs_fix(self, ady_list, loops, node, objective):
        # Temporarily set current node as dead end (Unless it is origin)
        if (objective != node):
            loops[node] = 0
        current_loops = 0
        
        # Loop
        for s in ady_list[node]:
            if loops[s] is None: 
                # Needs to be explored
                child_loops = self.count_cycle_dfs_fix(ady_list, loops, s, objective)
                current_loops += child_loops
            elif loops[s] > 0: 
                # Next node has N loops
                current_loops += loops[s]
            else: #loops[s] == 0: 
                # Next node is dead end or would be a currently visiting node
                pass
        # Set current node to appropiate loop status
        loops[node] = current_loops
        # Return count
        return loops[node]

    def brute_force_count_cycles(self, iterbale_states):
        # O(n^2): Adycacency list
        ady_list = {a:[] for a in iterbale_states}
        for i in iterbale_states:
            for o in iterbale_states:
                if (self.adjacency_matrix[i][o] is not None):
                    ady_list[i].append(o)

        # Counting por estado
        count_dict = {}       
        for node in iterbale_states:
            # Brute force. Generate all not looping paths from node
            path = []
            count = self.brute_force_count_cycles_rec(ady_list, node, node, path)
            # Save
            count_dict[node] = count
        return count_dict

    def brute_force_count_cycles_rec(self, ady_list, node, objective, path):
        # Loop
        count = 0
        for s in ady_list[node]:
            if s in path:
                pass # Already visited. Hence not a cycle for objective
            elif (s == objective):
                # End
                count += 1
            else:
                # Generate path
                path_extend = path + [s,]
                count += self.brute_force_count_cycles_rec(ady_list, s, objective, path_extend) # Visit recursievly
        # Return 
        return count



    def get_regular_expression_NCE(self):
        # List of active states and iterable states
        n = len(self.adjacency_matrix)
        active_states = [i for i in range(n-2)]
        iterbale_states = [i for i in range(n)]

        # Count cycles and get deletion order O(n^2)
        cycles_count_dict = self.count_cycles_jhonson(active_states)
        cycles_count_list = sorted(cycles_count_dict, key=cycles_count_dict.get)

        # Delete
        for s in cycles_count_list:
            # s = estado a remover

            # Declarando elemento de loop (*)
            if self.adjacency_matrix[s][s] is None:
                loop = RegularExp("", False)
            else:
                loop = self.adjacency_matrix[s][s].star()

            # Delete currently deleting from iterables
            iterbale_states.remove(s)

            # Lista de todas las entras y salidas validas
            in_transitions = [i for i in iterbale_states if self.adjacency_matrix[i][s] is not None]
            out_transitions = [o for o in iterbale_states if self.adjacency_matrix[s][o] is not None]

            # Combinacion de todas las entradas validas con todas las salidas valdias
            for i in in_transitions:
                for o in out_transitions:
                    if self.adjacency_matrix[i][o] is None:
                        self.adjacency_matrix[i][o] = self.adjacency_matrix[i][s] ^ loop ^  self.adjacency_matrix[s][o] 
                    else:
                        self.adjacency_matrix[i][o] = self.adjacency_matrix[i][o] +  (self.adjacency_matrix[i][s] ^ loop ^ self.adjacency_matrix[s][o])
            # Contador de operaciones
            self.operations += len(in_transitions) * len(out_transitions)

        return self.adjacency_matrix[n-2][n-1]


    def get_regular_expression_NCD(self):
        # List of active states and iterable states
        n = len(self.adjacency_matrix)
        active_states = [i for i in range(n-2)]
        iterbale_states = [i for i in range(n)]

        # Delete
        for r in range(len(active_states)):
            # Count cycles and get deletion order O(n^2)
            cycles_count_dict = self.count_cycles_jhonson(active_states)
            s = min(cycles_count_dict, key=cycles_count_dict.get)
            # s = estado a remover

            # Declarando elemento de loop (*)
            if self.adjacency_matrix[s][s] is None:
                loop = RegularExp("", False)
            else:
                loop = self.adjacency_matrix[s][s].star()

            # Delete currently deleting from iterables
            iterbale_states.remove(s)

            # Lista de todas las entras y salidas validas
            in_transitions = [i for i in iterbale_states if self.adjacency_matrix[i][s] is not None]
            out_transitions = [o for o in iterbale_states if self.adjacency_matrix[s][o] is not None]

            # Combinacion de todas las entradas validas con todas las salidas valdias
            for i in in_transitions:
                for o in out_transitions:
                    if self.adjacency_matrix[i][o] is None:
                        self.adjacency_matrix[i][o] = self.adjacency_matrix[i][s] ^ loop ^  self.adjacency_matrix[s][o] 
                    else:
                        self.adjacency_matrix[i][o] = self.adjacency_matrix[i][o] +  (self.adjacency_matrix[i][s] ^ loop ^ self.adjacency_matrix[s][o])
            
            # Contador de operaciones
            self.operations += len(in_transitions) * len(out_transitions)

            # Delete currently deleting from active
            active_states.remove(s)

        return self.adjacency_matrix[n-2][n-1]
