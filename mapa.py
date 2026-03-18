import random
import matplotlib.pyplot as plt
from shapely.geometry import polygon, Point


"""
primeiro como tratar os triangulos

1. Função para criar os triangulos

2. Função para colocar trinagulo dentro do plano cartesiano
    - tem que verificar se está dentro

3. Gerar triangulos aleatorio sem colisão

"""
"""
1. Gerar o mapa:

chamar main

"""

def gerar_mapa(largura, altura, inicio, fim):
    fig, ax = plt.subplots(figsize=(8, 6))

    ax.scatter(inicio[0], inicio[1], s=100, label="Inicio")
    ax.scatter(fim[0], fim[1], s=100, label="Fim")

    ax.text(inicio[0], inicio[1], "I(0,0)", fontsize=10, verticalalignment="bottom")
    ax.text(fim[0], fim[1], f" F{fim}", fontsize=10, verticalalignment="bottom")

    ax.set_xlim(0, largura)
    ax.set_ylim(0, altura)
    ax.set_xlabel("Eixo X")
    ax.set_ylabel("Eixo Y")
    ax.set_title("Mapa de Plano Cartesiano")
    ax.grid(True)
    ax.legend()

    plt.show()    

def main():
    print("==== Plano Cartesiano ====")

    inicio = (0, 0)

    #entrada do ponto final
    x_final = float(input("Digite o X do ponto final: "))
    y_final = float(input("Digite o Y do ponto final: "))

    if x_final <= 0 or y_final <= 0:
        print("ERRO: o ponto final deve ter valores positivos maior que zero. ")
        return 
    
    final = (x_final, y_final)

    largura = x_final
    altura = y_final

    gerar_mapa(largura, altura, inicio, final)

if __name__ == "__main__":
    main()