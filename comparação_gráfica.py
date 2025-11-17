import time
import matplotlib.pyplot as plt
from collections import deque


class aguaProblema:
    def __init__(self, J4_capacidade=4, J3_capacidade=3, objetivo=2):
        self.J4_capacidade = J4_capacidade
        self.J3_capacidade = J3_capacidade
        self.objetivo = objetivo

    def iniciarEstado(self):
        return (0, 0)

    def estadoEncontrado(self, estado):
        a, b = estado
        return a == self.objetivo or b == self.objetivo

    def expandir(self, estado):
        a, b = estado
        sucessores = []

        if a < self.J4_capacidade:
            sucessores.append(((self.J4_capacidade, b), "Encher o jarro A"))
        if b < self.J3_capacidade:
            sucessores.append(((a, self.J3_capacidade), "Encher o jarro B"))
        if a > 0:
            sucessores.append(((0, b), "Esvaziar o jarro A"))
        if b > 0:
            sucessores.append(((a, 0), "Esvaziar o jarro B"))
        if a > 0 and b < self.J3_capacidade:
            transfer = min(a, self.J3_capacidade - b)
            sucessores.append(((a - transfer, b + transfer), "Transferir A → B"))
        if b > 0 and a < self.J4_capacidade:
            transfer = min(b, self.J4_capacidade - a)
            sucessores.append(((a + transfer, b - transfer), "Transferir B → A"))

        return sucessores

# BFS

def breadthFirstSearch(problema):
    start = problema.iniciarEstado()
    fronteira = deque([(start, [])])
    explorado = set()
    explorados = 0

    while fronteira:
        estado, caminho = fronteira.popleft()
        explorados += 1

        if estado in explorado:
            continue
        explorado.add(estado)

        if problema.estadoEncontrado(estado):
            return caminho + [("Objetivo atingido", estado)], explorados

        for sucessor, acao in problema.expandir(estado):
            if sucessor not in explorado:
                fronteira.append((sucessor, caminho + [(acao, sucessor)]))

    return [], explorados


# DFS

def depthFirstSearch(problema):
    start = problema.iniciarEstado()
    fronteira = [(start, [])]
    explorado = set()
    explorados = 0

    while fronteira:
        estado, caminho = fronteira.pop()
        explorados += 1

        if estado in explorado:
            continue
        explorado.add(estado)

        if problema.estadoEncontrado(estado):
            return caminho + [("Objetivo atingido", estado)], explorados

        for sucessor, acao in problema.expandir(estado):
            if sucessor not in explorado:
                fronteira.append((sucessor, caminho + [(acao, sucessor)]))

    return [], explorados

# IDS

def depthLimitedSearch(problema, limite):
    start = problema.iniciarEstado()
    fronteira = [(start, [], 0)]
    explorado = set()
    explorados = 0

    while fronteira:
        estado, caminho, profundidade = fronteira.pop()
        explorados += 1

        if estado in explorado:
            continue
        explorado.add(estado)

        if problema.estadoEncontrado(estado):
            return caminho + [("Objetivo atingido", estado)], explorados

        if profundidade < limite:
            for sucessor, acao in problema.expandir(estado):
                if sucessor not in explorado:
                    fronteira.append((sucessor, caminho + [(acao, sucessor)], profundidade + 1))
    return None, explorados

def iterativeDeepeningSearch(problema):
    limite = 0
    total_explorados = 0
    while True:
        resultado, explorados = depthLimitedSearch(problema, limite)
        total_explorados += explorados
        if resultado is not None:
            return resultado, total_explorados
        limite += 1

# -------------------------------
# Comparação e Plotagem
# -------------------------------
if __name__ == "__main__":
    problema = aguaProblema()
    resultados = {}

    # BFS
    t0 = time.time()
    sol_bfs, exp_bfs = breadthFirstSearch(problema)
    t1 = time.time()
    resultados["BFS"] = (len(sol_bfs), exp_bfs, t1 - t0)

    # DFS
    t0 = time.time()
    sol_dfs, exp_dfs = depthFirstSearch(problema)
    t1 = time.time()
    resultados["DFS"] = (len(sol_dfs), exp_dfs, t1 - t0)

    # IDS
    t0 = time.time()
    sol_ids, exp_ids = iterativeDeepeningSearch(problema)
    t1 = time.time()
    resultados["IDS"] = (len(sol_ids), exp_ids, t1 - t0)

    # Mostrar resultados
    print("\n🔹 RESULTADOS COMPARATIVOS\n")
    print("Algoritmo | Passos | Estados Explorados | Tempo (s)")
    print("------------------------------------------------------")
    for nome, (passos, explorados, tempo) in resultados.items():
        print(f"{nome:10s} | {passos:6d} | {explorados:18d} | {tempo:.6f}")

    # Plotagem
    labels = list(resultados.keys())
    tempos = [resultados[k][2] for k in labels]
    explorados = [resultados[k][1] for k in labels]
    passos = [resultados[k][0] for k in labels]

    plt.figure(figsize=(10, 6))
    plt.subplot(1, 2, 1)
    plt.bar(labels, tempos)
    plt.title("Tempo de Execução")
    plt.ylabel("Tempo (s)")

    plt.subplot(1, 2, 2)
    plt.bar(labels, explorados)
    plt.title("Estados Explorados")
    plt.ylabel("Número de Estados")

    plt.suptitle("Comparação de Desempenho — BFS, DFS e IDS")
    plt.show()
