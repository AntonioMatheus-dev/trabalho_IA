

class aguaProblema:
    def __init__(self,J4_capacidade=4, J3_capacidade=3, objetivo=2):
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
            sucessores.append(((self.J4_capacidade, b),"Encher jarro A"))   


        if b < self.J3_capacidade:
            sucessores.append(((a,self.J3_capacidade),"Encher jarro B"))   
        

        if a>0:
            sucessores.append(((0,b), "Esvaziar jarro A"))
        
   
        if b > 0:
            sucessores.append(((a,0), "Esvaziar jarro B"))
        
        #Trasnferindo de A para B
        if a>0 and b < self.J3_capacidade:
            transfer = min(a,self.J3_capacidade-b)
            sucessores.append(((a - transfer, b + transfer),"Tranferência de A -> B"))
        
        # Transferir de B para A
        if b > 0 and a < self.J4_capacidade:  
            transfer = min(b, self.J4_capacidade - a)
            sucessores.append(((a + transfer, b - transfer),"Tranferência de B -> A"))
        
        return sucessores
    
    
def depthFirstSearch(problema):
    start = problema.iniciarEstado()
    fronteira = [(start, [])] 
    explorado = set()
    
    while fronteira:
        estado, caminho = fronteira.pop() 
        if estado in explorado:
            continue
        explorado.add(estado)
        
        if problema.estadoEncontrado(estado):
            return caminho + [("Objetivo atingido", estado)]
        

        for sucessor, acao in problema.expandir(estado):
            if sucessor not in explorado:
                fronteira.append((sucessor, caminho + [(acao, sucessor)]))
                
    return []

if __name__ == "__main__":
    problema = aguaProblema()
    solucao = depthFirstSearch(problema)

    if solucao:
        print("\nSolução encontrada (Busca em Profundidade - DFS):\n")
        for i, (acao, estado) in enumerate(solucao):
            print(f"{i+1}. {acao} -> {estado}")
    else:
        print("Nenhuma solução encontrada.")