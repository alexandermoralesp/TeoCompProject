from regularexp import RegularExp

class Automata:
    def __init__(self, n, start_state, end_state_list, transition_list):
                
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
    
    # PREGUNTA 1:
    def get_regular_expression_AEE(self):
        n = len(self.adjacency_matrix)

        for s in range( n ):
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
            
        return self.adjacency_matrix[n-2][n-1]