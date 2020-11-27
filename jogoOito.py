from random import uniform

objetivo = [[1,2,3],[8,0,4],[7,6,5]]
solucao = []

class Tabuleiro:
    def __init__(self, preencher=True, pai=None, matriz=objetivo, movimentoOriginario=None):
        self.tabuleiro = matriz
        self.pai = pai
        self.jaVisitado = False
        self.movimentoOriginario = movimentoOriginario
        if preencher:
            self.preencher()

    def preencher(self):
        for i in range(10000):
            valor = int(uniform(0, 3))
            posicaoZero = self.identificarPosicaoElemento(0, self.tabuleiro)
            if valor == 0 and posicaoZero[1] != 2:
                #mover o 0 para a direita
                self.tabuleiro = self.movimentar("D")
            elif valor == 1 and posicaoZero[1] != 0:
                #mover o 0 para a esquerda
                self.tabuleiro = self.movimentar("E")
            elif valor == 2 and posicaoZero[0] != 0:
                #mover o 0 para cima
                self.tabuleiro = self.movimentar("C")
            elif valor == 3 and posicaoZero[0] != 2:
                #mover o 0 para baixo
                self.tabuleiro = self.movimentar("B")

    def identificarPosicaoElemento(self, elemento, matriz):
        for i in range(3):
            for j in range(3):
                if matriz[i][j] == elemento:
                    return (i,j)

    def mostrarTabuleiro(self):
        if self.movimentoOriginario == None:
            print("Tabuleiro Inicial")
        else:
            print("Movimento: " + self.movimentoOriginario)
        for linha in self.tabuleiro:
            print(linha)
    
    #sempre que fizer uma movimentacao, o retorno sera a nova matriz
    def movimentar(self, movimento):
        novaMatriz = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                novaMatriz[i][j] = self.tabuleiro[i][j]
        posicaoZero = self.identificarPosicaoElemento(0, self.tabuleiro)
        if movimento == "D":
            valorAntigo = self.tabuleiro[posicaoZero[0]][posicaoZero[1] +1]
            novaMatriz[posicaoZero[0]][posicaoZero[1] +1] = 0
            novaMatriz[posicaoZero[0]][posicaoZero[1]] = valorAntigo
        elif movimento == "E":
            valorAntigo = self.tabuleiro[posicaoZero[0]][posicaoZero[1] -1]
            novaMatriz[posicaoZero[0]][posicaoZero[1] -1] = 0
            novaMatriz[posicaoZero[0]][posicaoZero[1]] = valorAntigo
        elif movimento == "C":
            valorAntigo = self.tabuleiro[posicaoZero[0] -1][posicaoZero[1]]
            novaMatriz[posicaoZero[0] -1][posicaoZero[1]] = 0
            novaMatriz[posicaoZero[0]][posicaoZero[1]] = valorAntigo
        elif movimento == "B":
            valorAntigo = self.tabuleiro[posicaoZero[0] +1][posicaoZero[1]]
            novaMatriz[posicaoZero[0] +1][posicaoZero[1]] = 0
            novaMatriz[posicaoZero[0]][posicaoZero[1]] = valorAntigo
        return novaMatriz

    #metodo que retorna o peso de um tabuleiro completo
    def pesoTabuleiro(self):
        pesoTotal = 0
        for i in range(9):
            pesoTotal += self.pesoPosicao(i)
        return pesoTotal

    #metodo responsavel por calcular a distancia Manhattan entre a posicao atual do elemento e a posicao objetivo de tal elemento
    def pesoPosicao(self, elemento):
        posicaoAtual = self.identificarPosicaoElemento(elemento,self.tabuleiro)
        posicaoObjetivo = self.identificarPosicaoElemento(elemento, objetivo)
        x = posicaoAtual[0] - posicaoObjetivo[0]
        y = posicaoAtual[1] - posicaoObjetivo[1]
        if x < 0:
            x = x*(-1)
        if y < 0:
            y = y*(-1)
        return x+y

    def compararMatrizes(self, matriz):
        for i in range(3):
            for j in range(3):
                if self.tabuleiro[i][j] != matriz[i][j]:
                    return False
        return True


class BuscaInformada:
    def __init__(self, tabuleiro=Tabuleiro()):
        self.matriz = tabuleiro
        self.matrizesExistentes = []
        self.solucionar()
    
    def solucionar(self):
        self.matrizesExistentes.append(self.matriz)
        while self.matriz.compararMatrizes(objetivo) == False:
            movimentosPossiveis = self.analiseMovimentos()
            while len(movimentosPossiveis) != 0:
                movimento = movimentosPossiveis.pop(0)
                tabuleiro = Tabuleiro(False, self.matriz, self.matriz.movimentar(movimento), movimento)
                if self.analiseExistencia(tabuleiro.tabuleiro) == False:
                    self.matrizesExistentes.append(tabuleiro)
            self.matriz.jaVisitado = True

            posicaoMenorPeso = 0
            while self.matrizesExistentes[posicaoMenorPeso].jaVisitado:
                posicaoMenorPeso += 1
            for i in range(len(self.matrizesExistentes)):
                if self.matrizesExistentes[i].jaVisitado == False:
                    if self.matrizesExistentes[i].pesoTabuleiro() < self.matrizesExistentes[posicaoMenorPeso].pesoTabuleiro():
                        posicaoMenorPeso = i
            self.matriz = self.matrizesExistentes[posicaoMenorPeso]
        self.mostrarSolucao()

    def mostrarSolucao(self):
        while self.matriz.pai != None:
            solucao.append(self.matriz)
            self.matriz = self.matriz.pai   
        solucao.append(self.matriz)
        for _ in range(len(solucao)):
            tabuleiro = solucao.pop()
            tabuleiro.mostrarTabuleiro()

    def analiseExistencia(self, matriz):
        for i in range(len(self.matrizesExistentes)):
            if self.matrizesExistentes[i].compararMatrizes(matriz):
                return True
        return False

    def analiseMovimentos(self):
        posicaoZero = self.matriz.identificarPosicaoElemento(0, self.matriz.tabuleiro)
        posicoes = []
        temPai = False
        if self.matriz.movimentoOriginario != None:
            movOrig = self.matriz.movimentoOriginario
            temPai = True
        if posicaoZero == (0,0):
            posicoes = ["D","B"]
            if temPai:
                if movOrig == "E":
                    posicoes.remove("D")
                else:
                    posicoes.remove("B")
        elif posicaoZero == (0,2):
            posicoes = ["E","B"]
            if temPai:
                if movOrig == "D":
                    posicoes.remove("E")
                else:
                    posicoes.remove("B")
        elif posicaoZero == (2,0):
            posicoes = ["C","D"]
            if temPai:
                if movOrig == "E":
                    posicoes.remove("D")
                else:
                    posicoes.remove("C")
        elif posicaoZero == (2,2):
            posicoes = ["C","E"]
            if temPai:
                if movOrig == "D":
                    posicoes.remove("E")
                else:
                    posicoes.remove("C")
        elif posicaoZero == (0,1):
            posicoes = ["E","D","B"]
            if temPai:
                if movOrig == "E":
                    posicoes.remove("D")
                elif movOrig == "D":
                    posicoes.remove("E")
                else:
                    posicoes.remove("B")
        elif posicaoZero == (1,0):
            posicoes = ["C","D","B"]
            if temPai:
                if movOrig == "B":
                    posicoes.remove("C")
                elif movOrig == "E":
                    posicoes.remove("D")
                else:
                    posicoes.remove("B")
        elif posicaoZero == (2,1):
            posicoes = ["E","D","C"]
            if temPai:
                if movOrig == "D":
                    posicoes.remove("E")
                elif movOrig == "E":
                    posicoes.remove("D")
                else:
                    posicoes.remove("C")
        elif posicaoZero == (1,2):
            posicoes = ["C","E","B"]
            if temPai:
                if movOrig == "B":
                    posicoes.remove("C")
                elif movOrig == "D":
                    posicoes.remove("E")
                else:
                    posicoes.remove("B")
        elif posicaoZero == (1,1):
            posicoes = ["C","D","B","E"]
            if temPai:
                if movOrig == "C":
                    posicoes.remove("B")
                elif movOrig == "B":
                    posicoes.remove("C")
                elif movOrig == "D":
                    posicoes.remove("E")
                else:
                    posicoes.remove("D")
        return posicoes


if __name__ == "__main__":
    busca = BuscaInformada()