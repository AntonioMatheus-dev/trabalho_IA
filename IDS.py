class aguaProblema:
    def __init__(self, J4_capacidade=4, J3_capacidade=3, objetivo=2):
        self.J4_capacidade = J4_capacidade
        self.J3_capacidade = J3_capacidade
        self.objetivo = objetivo
        
    def  iniciarEstado(self):
       
        return (0, 0)
    def estadoEncontrado(self, estado):
        a,b = estado
        return a == self.objetivo or b == self.objetivo
    def expandir(self, estado):
       
        
        a, b = estado
        sucessores = []
        
        
        if a< self.J4_capacidade :
            sucessores.append(((self.J4_capacidade, b), "Encher o jarro A"))
     
     
        if b< self.J3_capacidade:
            sucessores.append(((a, self.J3_capacidade), "Encher o jarro B"))
        
       
        if a > 0:
            sucessores.append(((0, b), "Esvaziar jarro A"))
        
        if b>0:
            sucessores.append(((a, 0),"Esvaziar o jarro B"))
        
        if a>0 and b <self.J3_capacidade:
            transfer = min(a, self.J3_capacidade - b)
            sucessores.append(((a - transfer, b + transfer), "Trasnferindo de A -> B"))
        
        
        if b> 0 and a<self.J4_capacidade: 
            transfer = min(b, self.J4_capacidade - a)
            sucessores.append(((a+transfer, b-transfer),"Trasnferindo de B -> A"))
        
        return sucessores
    
def depthLimitedSearch(problema, limite):
    start = problema.iniciarEstado()
    fronteira = [(start, [], 0)]
    explorado = set()
    
    while fronteira:
        estado, caminho, profundidade = fronteira.pop()
        
        if estado in explorado:
            continue
        explorado.add(estado)
        
        if problema.estadoEncontrado(estado):
            return caminho + [("Objetivo atingido", estado)]
        
        if profundidade < limite:
            for sucessor, acao in problema.expandir(estado):
                if sucessor not in explorado:
                    fronteira.append((sucessor, caminho + [(acao, sucessor)], profundidade + 1))
    return None 

def interativeDeepeningSearch(problema):
    limite = 0
    while True:
        resultado = depthLimitedSearch(problema, limite)
        if resultado is not None:
            return resultado
        limite +=1 

if __name__ == "__main__":
    problema = aguaProblema()
    solucao = interativeDeepeningSearch(problema)

    if solucao:
        print("\nSolução encontrada (Busca com Aprofundamento Iterativo - IDS):\n")
        for i, (acao, estado) in enumerate(solucao):
            print(f"{i+1}. {acao} -> {estado}")
    else:
        print("Nenhuma solução encontrada.")