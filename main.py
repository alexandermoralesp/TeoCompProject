
class Automata:
    def __init__(self, n, start_state, end_state_list):
                
        # Create Adjacency Matrix
        self.adjacency_matrix = [[None for i in range(n+2)] for j in range(n+2)]
        
        # Initalize normalized state
        # Normalized Start: n
        # Normalized End: n+1
        normalized_start_index = n
        normalized_end_index = n+1

        print(start_state)
        print(normalized_start_index)
        self.adjacency_matrix[normalized_start_index][start_state] = "" # Epsilon
        for state in end_state_list:
            self.adjacency_matrix[state][normalized_end_index] = "" # Epsilon transition
        

    def add_transition(self, state, transition, next): # Método para añadir un estado al automata
        if self.adjacency_matrix[state][next] is None: 
            self.adjacency_matrix[state][next] = str(transition)
        else:
            # Completado: NORMALIZACION de doble transicion
            self.adjacency_matrix[state][next] = str(transition)+"+"+self.adjacency_matrix[state][next]

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
            print("S:"+str(s))
            loop = str("("+self.adjacency_matrix[s][s]+")*") if self.adjacency_matrix[s][s] !=None else ""
            print("LOOP:"+loop)

            in_transitions = [i for i in range(s+1,n) if self.adjacency_matrix[i][s] is not None]
            out_transitions = [o for o in range(s+1,n) if self.adjacency_matrix[s][o] is not None]

            for i in in_transitions:
                for o in out_transitions:
                    print((i,o))
                    if self.adjacency_matrix[i][o] is None:
                        self.adjacency_matrix[i][o] = self.adjacency_matrix[i][s] + loop +  self.adjacency_matrix[s][o] 
                    else:
                        self.adjacency_matrix[i][o] = "(" + self.adjacency_matrix[i][s] + loop + self.adjacency_matrix[s][o] + "+" + self.adjacency_matrix[i][o]+ ")" 
            
        return self.adjacency_matrix[n-2][n-1]

def main():
    line = input().split() # Linea de ingreso de valores de primera fila
    n = int(line[0]) # Definir cuantos estados habrán
    start = int(line[1]) # Definir estado inicial
    end_list = [int(line[i+3]) for i in range( int(line[2]) )] # Dar los ids de los estados finales

    if end_list: # Si existen estados finales

        automata = Automata(n, start, end_list) # Creamos la clase automata 
        automata.display() 

        for i in range(2*n ): # Bucle para las siguientes 2n filas
            line = input().split() # Fila de transicion estilo  "estado" "entrada" "siguiente estado"
            state = int(line[0]) # Extracción del estado
            transition = str(line[1]) # Extracción del caracter ingresado
            next = int(line[2]) # Extraccion del siguiente estado
            automata.add_transition(state, transition, next) # Se añade la transicion al automata
        
        automata.display()
        regex = automata.get_regular_expression()
    else:
        # COMPLETADO: CASO ESQUINA: Cuando le automata no tiene estados finales
        regex = None

    print("REGEX:",regex) # Se imprime la expresión regular


main()


