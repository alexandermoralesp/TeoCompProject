class RegularExp:
    def __init__(self, regex, requires_parenthesis=False):
        self.regex = regex
        self.requires_parenthesis = requires_parenthesis
    
    def __add__(self, other):
        if self.requires_parenthesis and other.requires_parenthesis:
            template = "({})+({})"
        elif self.requires_parenthesis:
            template = "({})+{}"
        elif other.requires_parenthesis:
            template = "{}+({})"
        else:
            template = "{}+{}"
        return RegularExp(template.format(self.regex, other.regex), True)
    
    def __xor__(self, other):
        if (other.regex == "e"):
            return RegularExp(self.regex, self.requires_parenthesis)
        elif (self.regex == "e"):
            return RegularExp(other.regex, other.requires_parenthesis)

        if self.requires_parenthesis and other.requires_parenthesis:
            template = "({})({})"
        elif self.requires_parenthesis:
            template = "({}){}"
        elif other.requires_parenthesis:
            template = "{}({})"
        else:
            template = "{}{}"
        return RegularExp(template.format(self.regex, other.regex), False)

    def star(self):
        if (self.regex == "e"):
            return RegularExp("", False)
        if len(self.regex) == 1:
            template = "{}*"
        else:
            template = "({})*"
        return RegularExp(template.format(self.regex), False)

    def __str__(self):
        return self.regex

class Automata:
    def __init__(self, n, start_state, end_state_list):
                
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
    
    def get_regular_expression(self):
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

def main():
    line = input().split() # Linea de ingreso de valores de primera fila
    n = int(line[0]) # Definir cuantos estados habrán
    start = int(line[1]) # Definir estado inicial
    end_list = [int(line[i+3]) for i in range( int(line[2]) )] # Dar los ids de los estados finales

    if end_list: # Si existen estados finales

        automata = Automata(n, start, end_list) # Creamos la clase automata 

        for i in range(2*n ): # Bucle para las siguientes 2n filas
            line = input().split() # Fila de transicion estilo  "estado" "entrada" "siguiente estado"
            state = int(line[0]) # Extracción del estado
            transition = str(line[1]) # Extracción del caracter ingresado
            next = int(line[2]) # Extraccion del siguiente estado
            automata.add_transition(state, transition, next) # Se añade la transicion al automata
        
        regex = automata.get_regular_expression()
    else:
        # COMPLETADO: CASO ESQUINA: Cuando le automata no tiene estados finales se aceptan inputs pero se sabe que el regex va a ser nulo
        for i in range(2*n ):
            line = input()
        regex = None

    print(regex) # Se imprime la expresión regular


main()


