class Automata:
    def __init__(self, _n_estados, _e_inicio, _n_estados_finales, _e_finales):
        self.transiciones = {}
        for i in range(_n_estados):
            self.transiciones[i] = {0:None, 1:None}

    def mas_transicion(self, _e_actual, _entrada, _e_siguiente):
        self.transiciones[_e_actual][_entrada]=_e_siguiente

    



l1 = input().split()
n_estados = int(l1[0])
e_inicio = int(l1[1])
n_estados_finales = int(l1[2])
e_finales = [int(l1[i]) for i in range(3, n_estados_finales+3)]

a = Automata(n_estados, e_inicio, n_estados_finales, e_finales)

for i in range(2*n_estados):
    trans = input().split()
    e_actual = int(trans[0])
    entrada = int(trans[1])
    e_siguiente = int(trans[2])
    a.mas_transicion(e_actual, entrada, e_siguiente)

print(a.transiciones)