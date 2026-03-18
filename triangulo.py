import random
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point

"""
primeiro como tratar os triangulos

1. Função para criar os triangulos

2. Função para colocar trinagulo dentro do plano cartesiano
    - tem que verificar se está dentro

3. Gerar triangulos aleatorio sem colisão

"""

def gerar_triangulo (x_base, y_base, tamanho):
    a = (x_base, y_base)
    b = (x_base + tamanho, y_base)
    c = (x_base + tamanho / 2, y_base + tamanho)
    return Polygon([a, b, c])



def main():
    print ("Teste para gerar triangulo")

    tam_triangulo = float (input("Digite tamanho do triangulo: "))
    if tam_triangulo <= 0:
        print("ERRO: O tamanho do triangulo deve ser maio que zero.")
        return

    triangulo = gerar_triangulo(0, 0, tam_triangulo)

    x,y = triangulo.exterior.xy

    plt.plot(x , y) # plot são as linha
    plt.fill(x , y, alpha=0.3) # fill preencher , alpha é o nível de transparencia
    
    plt.title("Triangulo") #titulo do desenho
    plt.axis('equal') #mantem a proporção x==y

    plt.show()

if __name__ == "__main__" :
    main()