from random import uniform

objetivo = [[1,2,3],[8,0,4],[7,6,5]]

class Tabuleiro:
    def __init__(self, preencher=True, pai=None, matriz=objetivo, movimentoOriginario=None):
        self.tabuleiro = matriz
        self.pai = pai
        self.jaVisitado = False
        self.movimentoOriginario = movimentoOriginario
        if preencher:
            self.preencher()

    def preencher(self):
        for i in range(50):
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
        for linha in self.tabuleiro:
            print(linha)
    
    #sempre que fizer uma movimentacao, o retorno sera a nova matriz
    def movimentar(self, movimento):
        novaMatriz = self.tabuleiro
        posicaoZero = self.identificarPosicaoElemento(0, self.tabuleiro)
        if movimento == "D":
            #salvar o valor que pertencia ao elemento da direita do zero
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



class BuscaInformada:
    def __init__(self):
        self.matriz = Tabuleiro()
        self.matrizesExistentes = []
    
    def solucionar(self):
        self.matrizesExistentes.append(self.matriz)
        while self.matriz != objetivo:
            posicaoMenorPeso = 0
            movimentosPossiveis = self.analiseMovimentos()
            for i in range(len(movimentosPossiveis)):
                tabuleiro = Tabuleiro(False, self.matriz, self.matriz.movimentar(i), i)
                if self.analiseExistencia(tabuleiro) == False:
                    self.matrizesExistentes.append(tabuleiro)
                self.matriz.jaVisitado = True
            for i in range(len(self.matrizesExistentes)):
                menorPeso = 0
                #PROVAVELMENTE O ERRO ESTA NESSA PARTE
                if self.matrizesExistentes[i].jaVisitado == False:
                    if self.matrizesExistentes[i].pesoTabuleiro() < self.matrizesExistentes[posicaoMenorPeso].pesoTabuleiro():
                        menorPeso = self.matrizesExistentes[i].pesoTabuleiro()
                        posicaoMenorPeso = i
            self.matriz = self.matrizesExistentes[posicaoMenorPeso]
        print("Resolvendo....")
        self.mostrarSolucao()

    def mostrarSolucao(self):
        if self.matriz.pai != None:
            self.pai.mostrarSolucao()
            print(self.matriz.movimentoOriginario)
        self.matriz.mostrarTabuleiro()

    def analiseExistencia(self, matriz):
        for i in range(len(self.matrizesExistentes)):
            if matriz == self.matrizesExistentes[i]:
                return True
        return False

    def analiseMovimentos(self):
        posicaoZero = self.matriz.identificarPosicaoElemento(0, self.matriz.tabuleiro)
        posicoes = []
        if posicaoZero == (0,0):
            posicoes = ["D","B"]
        elif posicaoZero == (0,2):
            posicoes = ["E","B"]
        elif posicaoZero == (2,0):
            posicoes = ["C","D"]
        elif posicaoZero == (2,2):
            posicoes = ["C","E"]
        elif posicaoZero == (0,1):
            posicoes = ["E","D","B"]
        elif posicaoZero == (1,0):
            posicoes = ["C","D","B"]
        elif posicaoZero == (2,1):
            posicoes = ["E","D","C"]
        elif posicaoZero == (1,2):
            posicoes = ["C","E","B"]
        elif posicaoZero == (1,1):
            posicoes = ["C","D","B","E"]
        if self.matriz.movimentoOriginario != None:
            movOrig = self.matriz.movimentoOriginario
            if posicaoZero == (0,0):
                if movOrig == "E":
                    posicoes.remove("D")
                else:
                    posicoes.remove("B")
            elif posicaoZero == (0,2):
                if movOrig == "D":
                    posicoes.remove("E")
                else:
                    posicoes.remove("B")
            elif posicaoZero == (2,0):
                if movOrig == "E":
                    posicoes.remove("D")
                else:
                    posicoes.remove("C")
            elif posicaoZero == (2,2):
                if movOrig == "D":
                    posicoes.remove("E")
                else:
                    posicoes.remove("C")
            elif posicaoZero == (0,1):
                if movOrig == "E":
                    posicoes.remove("D")
                elif movOrig == "D":
                    posicoes.remove("E")
                else:
                    posicoes.remove("B")
            elif posicaoZero == (1,0):
                if movOrig == "B":
                    posicoes.remove("C")
                elif movOrig == "E":
                    posicoes.remove("D")
                else:
                    posicoes.remove("B")
            elif posicaoZero == (2,1):
                if movOrig == "D":
                    posicoes.remove("E")
                elif movOrig == "E":
                    posicoes.remove("D")
                else:
                    posicoes.remove("C")
            elif posicaoZero == (1,2):
                if movOrig == "B":
                    posicoes.remove("C")
                elif movOrig == "D":
                    posicoes.remove("E")
                else:
                    posicoes.remove("B")
            elif posicaoZero == (1,1):
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
    #opcao = input("Como gostaria de resolver o Jogo dos 8? 1-Busca Informada  2-Busca Cega \n")
    #if opcao == 1:
    busca = BuscaInformada()
    busca.solucionar()