import random
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point

# --------------------------
# CRIA TRIÂNGULO
# --------------------------

def criar_triangulo_isosceles(x_base, y_base, tamanho):
    a = (x_base, y_base)
    b = (x_base + tamanho, y_base)
    c = (x_base + tamanho / 2, y_base + tamanho)
    return Polygon([a, b, c])


# --------------------------
# DENTRO DO MAPA
# --------------------------

def triangulo_dentro_do_mapa(triangulo, largura, altura):
    coords = list(triangulo.exterior.coords)
    for x, y in coords:
        if x < 0 or x > largura or y < 0 or y > altura:
            return False
    return True


# --------------------------
# GEOMETRIA SIMPLES
# --------------------------

def orientacao(ponto_a, ponto_b, ponto_c):
    return (ponto_b[1] - ponto_a[1]) * (ponto_c[0] - ponto_b[0]) - (ponto_b[0] - ponto_a[0]) * (ponto_c[1] - ponto_b[1])


def segmentos_intersectam(inicio_1, fim_1, inicio_2, fim_2):
    orientacao_1 = orientacao(inicio_1, fim_1, inicio_2)
    orientacao_2 = orientacao(inicio_1, fim_1, fim_2)
    orientacao_3 = orientacao(inicio_2, fim_2, inicio_1)
    orientacao_4 = orientacao(inicio_2, fim_2, fim_1)

    return (orientacao_1 * orientacao_2 < 0) and (orientacao_3 * orientacao_4 < 0)


def arestas(triangulo):
    coordenadas = list(triangulo.exterior.coords)[:-1]
    ponto_a, ponto_b, ponto_c = coordenadas
    return [ (ponto_a, ponto_b), (ponto_b, ponto_c), (ponto_c, ponto_a) ]


def triangulos_colidem(triangulo_1, triangulo_2):
    # 1. cruzamento de arestas
    for aresta_1 in arestas(triangulo_1):
        for aresta_2 in arestas(triangulo_2):
            if segmentos_intersectam( aresta_1[0], aresta_1[1], aresta_2[0], aresta_2[1] ):
                return True

    # 2. encostar ou estar dentro
    ponto_t1 = Point(list(triangulo_1.exterior.coords)[0])
    ponto_t2 = Point(list(triangulo_2.exterior.coords)[0])

    if triangulo_1.contains(ponto_t2) or triangulo_1.touches(ponto_t2):
        return True

    if triangulo_2.contains(ponto_t1) or triangulo_2.touches(ponto_t1):
        return True

    return False

# --------------------------
# VALIDAÇÃO
# --------------------------

def triangulo_valido(novo_triangulo, obstaculos, inicio, fim):
    ponto_inicio = Point(inicio)
    ponto_fim = Point(fim)

    # não pode cobrir início ou fim
    if novo_triangulo.contains(ponto_inicio) or novo_triangulo.touches(ponto_inicio):
        return False

    if novo_triangulo.contains(ponto_fim) or novo_triangulo.touches(ponto_fim):
        return False

    # não pode colidir com outros
    for obstaculo in obstaculos:
        if triangulos_colidem(novo_triangulo, obstaculo):
            return False

    return True


# --------------------------
# GERAR OBSTÁCULOS
# --------------------------

def gerar_obstaculos(quantidade, tamanho, largura, altura, inicio, fim, max_tentativas=5000):
    obstaculos = []
    tentativas = 0

    while len(obstaculos) < quantidade and tentativas < max_tentativas:
        tentativas += 1

        x_base = random.uniform(0, largura - tamanho)
        y_base = random.uniform(0, altura - tamanho)

        novo_triangulo = criar_triangulo_isosceles(x_base, y_base, tamanho)

        if not triangulo_dentro_do_mapa(novo_triangulo, largura, altura):
            continue

        if triangulo_valido(novo_triangulo, obstaculos, inicio, fim):
            obstaculos.append(novo_triangulo)

    return obstaculos


# --------------------------
# DESENHO
# --------------------------

def desenhar_mapa(largura, altura, inicio, fim, obstaculos):
    fig, ax = plt.subplots(figsize=(8, 6))

    # obstáculos
    for triangulo in obstaculos:
        x, y = triangulo.exterior.xy
        ax.fill(x, y, alpha=0.5)
        ax.plot(x, y)

    # pontos
    ax.scatter(inicio[0], inicio[1], s=100, label="Inicio")
    ax.scatter(fim[0], fim[1], s=100, label="Fim")

   # ax.text(inicio[0], inicio[1], " I(0,0)", fontsize=10)
   # ax.text(fim[0], fim[1], f" F{fim}", fontsize=10)

    ax.set_xlim(0, largura)
    ax.set_ylim(0, altura)
    ax.set_xlabel("Eixo X")
    ax.set_ylabel("Eixo Y")
    ax.set_title("Mapa com Obstaculos Triangulares")
    ax.grid(True)
    ax.legend()

    plt.show()


# --------------------------
# MAIN
# --------------------------

def main():
    print("=== Geracao de mapa ===")

    inicio = (0, 0)

    x_final = float(input("Digite o X do ponto final: "))
    y_final = float(input("Digite o Y do ponto final: "))

    if x_final <= 0 or y_final <= 0:
        print("Erro: valores devem ser positivos.")
        return

    fim = (x_final, y_final)

    largura = x_final
    altura = y_final

    quantidade_obstaculos = int(input("Quantidade de obstaculos: "))
    tamanho_triangulo = float(input("Tamanho dos triangulos: "))

    obstaculos = gerar_obstaculos( quantidade_obstaculos, tamanho_triangulo, largura, altura, inicio, fim )

    desenhar_mapa(largura, altura, inicio, fim, obstaculos)


if __name__ == "__main__":
    main()