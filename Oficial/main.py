from automata import Automata

def main():
    ## INPUTS
    line = input().split() # Linea de ingreso de valores de primera fila
    n = int(line[0]) # Definir cuantos estados habrán
    start = int(line[1]) # Definir estado inicial
    end_list = [int(line[i+3]) for i in range( int(line[2]) )] # Dar los ids de los estados finales
    transition_list = []
    for i in range(2*n ): # Bucle para las siguientes 2n filas
        line = input().split() # Fila de transicion estilo  "estado" "entrada" "siguiente estado"
        state = int(line[0]) # Extracción del estado
        transition = str(line[1]) # Extracción del caracter ingresado
        next = int(line[2]) # Extraccion del siguiente estado
        transition_list.append( (state, transition, next) ) # Se añade la transicion a la lista de transiciones del automata

    ## PROCESAMIENTO
    if end_list: # Si existen estados finales
        automata = Automata(n, start, end_list, transition_list) # Creamos la clase automata    
        regex = automata.get_regular_expression_AEE() # Obtenemos la regex
    else:
        # COMPLETADO: CASO ESQUINA: Se sabe que el regex es nulo si no hay estados finales
        regex = None

    ## OUTPUT
    print(regex) # Se imprime la expresión regular


main()