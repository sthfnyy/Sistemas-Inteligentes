import random
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point


def criar_triangulo_isosceles(x_base, y_base, tamanho):
    """
    Cria um triângulo isósceles com base horizontal.
    
    Base:
        A ---- B
           C
        
    A = (x_base, y_base)
    B = (x_base + tamanho, y_base)
    C = (x_base + tamanho/2, y_base + tamanho)
    """
    a = (x_base, y_base)
    b = (x_base + tamanho, y_base)
    c = (x_base + tamanho / 2, y_base + tamanho)

    return Polygon([a, b, c])


def triangulo_dentro_do_mapa(triangulo, largura, altura):
    """
    Verifica se todos os pontos do triângulo estão dentro do plano cartesiano.
    """
    coords = list(triangulo.exterior.coords)
    for x, y in coords:
        if x < 0 or x > largura or y < 0 or y > altura:
            return False
    return True


def triangulo_valido(novo_triangulo, obstaculos, inicio, fim):
    """
    Verifica se:
    - não colide com outros triângulos
    - não cobre o ponto inicial
    - não cobre o ponto final
    """
    ponto_inicio = Point(inicio)
    ponto_fim = Point(fim)

    if novo_triangulo.contains(ponto_inicio) or novo_triangulo.touches(ponto_inicio):
        return False

    if novo_triangulo.contains(ponto_fim) or novo_triangulo.touches(ponto_fim):
        return False

    for obstaculo in obstaculos:
        if novo_triangulo.intersects(obstaculo):
            return False

    return True


def gerar_obstaculos(quantidade, tamanho, largura, altura, inicio, fim, max_tentativas=5000):
    """
    Gera triângulos aleatórios sem colisão.
    """
    obstaculos = []
    tentativas = 0

    while len(obstaculos) < quantidade and tentativas < max_tentativas:
        tentativas += 1

        # Gera a base do triângulo em posição aleatória
        x_base = random.uniform(0, largura - tamanho)
        y_base = random.uniform(0, altura - tamanho)

        novo_triangulo = criar_triangulo_isosceles(x_base, y_base, tamanho)

        if not triangulo_dentro_do_mapa(novo_triangulo, largura, altura):
            continue

        if triangulo_valido(novo_triangulo, obstaculos, inicio, fim):
            obstaculos.append(novo_triangulo)

    return obstaculos


def desenhar_mapa(largura, altura, inicio, fim, obstaculos):
    fig, ax = plt.subplots(figsize=(8, 6))

    # Desenha obstáculos
    for i, triangulo in enumerate(obstaculos, start=1):
        x, y = triangulo.exterior.xy
        ax.fill(x, y, alpha=0.5)
        ax.plot(x, y)

        # Marca centro aproximado do triângulo
        centro = triangulo.centroid
        ax.text(centro.x, centro.y, f"T{i}", fontsize=9, ha="center")

    # Desenha início e fim
    ax.scatter(inicio[0], inicio[1], s=100, label="Início")
    ax.scatter(fim[0], fim[1], s=100, label="Fim")

    ax.text(inicio[0], inicio[1], " I(0,0)", fontsize=10, verticalalignment="bottom")
    ax.text(fim[0], fim[1], f" F{fim}", fontsize=10, verticalalignment="bottom")

    # Configuração do plano cartesiano
    ax.set_xlim(0, largura)
    ax.set_ylim(0, altura)
    ax.set_xlabel("Eixo X")
    ax.set_ylabel("Eixo Y")
    ax.set_title("Mapa de Grafo com Obstáculos Triangulares")
    ax.grid(True)
    ax.legend()

    plt.show()


def main():
    print("=== Geração de mapa em plano cartesiano ===")

    inicio = (0, 0)

    # Entrada do ponto final
    x_final = float(input("Digite o X do ponto final: "))
    y_final = float(input("Digite o Y do ponto final: "))

    if x_final <= 0 or y_final <= 0:
        print("Erro: o ponto final deve ter valores positivos maiores que zero.")
        return

    fim = (x_final, y_final)

    # O ponto final define o tamanho do mapa
    largura = x_final
    altura = y_final

    # Quantidade de obstaculos
    quantidade_obstaculos = int(input("Digite a quantidade de obstaculos: "))
    if quantidade_obstaculos < 0:
        print("Erro: a quantidade de obstaculos não pode ser negativa.")
        return

    # Tamanho dos triângulos
    tamanho_triangulo = float(input("Digite o tamanho dos triângulos isósceles: "))
    if tamanho_triangulo <= 0:
        print("Erro: o tamanho do triângulo deve ser maior que zero.")
        return

    # Geração dos obstaculos
    obstaculos = gerar_obstaculos(
        quantidade=quantidade_obstaculos,
        tamanho=tamanho_triangulo,
        largura=largura,
        altura=altura,
        inicio=inicio,
        fim=fim
    )

    # Verifica se conseguiu gerar tudo
    if len(obstaculos) < quantidade_obstaculos:
        print("\nAviso:")
        print(
            f"Foi possível gerar apenas {len(obstaculos)} de "
            f"{quantidade_obstaculos} obstaculos sem colisão."
        )
        print("Tente diminuir a quantidade de obstaculos ou o tamanho dos triângulos.")

    # Exibir mapa
    desenhar_mapa(largura, altura, inicio, fim, obstaculos)


if __name__ == "__main__":
    main()