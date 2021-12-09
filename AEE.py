class Automata:
    def __init__(self, _n_estados, _e_inicio, _n_estados_finales, _e_finales):
        self.mat_transicion = [[] for i in range(_n_estados)]


l1 = input().split()
n_estados = int(l1[0])
e_inicio = int(l1[1])
n_estados_finales = int(l1[2])
e_finales = [int(l1[i]) for i in range(3, n_estados_finales+3)]

for i in range(2*n_estados_finales):
    trans = input().split()
    e_actual = int(trans[0])
    entrada = int(trans[1])
    e_siguiente = int(trans[2])