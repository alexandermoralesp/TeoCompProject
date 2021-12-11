from automata import Automata

def solve(n, start, end_list, transition_list, algo):
    ## PROCESAMIENTO
    if end_list: # Si existen estados finales
        automata = Automata(n, start, end_list, transition_list) # Creamos la clase automata    
        regex = automata.get_regular_expression(algo) # Obtenemos la regex
    else:
        # COMPLETADO: CASO ESQUINA: Se sabe que el regex es nulo si no hay estados finales
        regex = None
    return regex