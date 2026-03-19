import math
import random
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point, LineString


# ==========================================================
# GEOMETRIA
# ==========================================================
def criar_triangulo_isosceles(x_base, y_base, tamanho):
    a = (x_base, y_base)
    b = (x_base + tamanho, y_base)
    c = (x_base + tamanho / 2, y_base + tamanho)
    return Polygon([a, b, c])


def obter_vertices_triangulo(triangulo):
    return list(triangulo.exterior.coords)[:-1]


def obter_arestas_triangulo(triangulo):
    v = obter_vertices_triangulo(triangulo)
    return [(v[0], v[1]), (v[1], v[2]), (v[2], v[0])]


def triangulo_dentro_do_mapa(triangulo, largura, altura):
    for x, y in triangulo.exterior.coords:
        if x < 0 or x > largura or y < 0 or y > altura:
            return False
    return True


def ponto_em_triangulo_ou_borda(triangulo, ponto):
    p = Point(ponto)
    return triangulo.contains(p) or triangulo.touches(p)


def triangulos_colidem_ou_tocam(t1, t2):
    return t1.intersects(t2)


def distancia(p1, p2):
    return math.dist(p1, p2)


# ==========================================================
# GERAÇÃO DOS OBSTÁCULOS
# ==========================================================
def triangulo_valido(novo_triangulo, obstaculos, inicio, fim):
    if ponto_em_triangulo_ou_borda(novo_triangulo, inicio):
        return False

    if ponto_em_triangulo_ou_borda(novo_triangulo, fim):
        return False

    for obstaculo in obstaculos:
        if triangulos_colidem_ou_tocam(novo_triangulo, obstaculo):
            return False

    return True


def gerar_obstaculos(quantidade, tamanho, largura, altura, inicio, fim, max_tentativas=10000):
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


# ==========================================================
# PONTOS DO GRAFO
# ==========================================================
def obter_pontos_do_mapa(obstaculos, inicio, fim):
    pontos = [inicio, fim]

    for triangulo in obstaculos:
        pontos.extend(obter_vertices_triangulo(triangulo))

    # remove duplicados preservando ordem
    pontos_unicos = []
    for p in pontos:
        if p not in pontos_unicos:
            pontos_unicos.append(p)

    return pontos_unicos


# ==========================================================
# VALIDAÇÃO DE ARESTA
# ==========================================================
def mesmo_segmento(a1, a2, b1, b2):
    return {a1, a2} == {b1, b2}


def ponto_eh_extremidade(point_geom, A, B, tol=1e-9):
    return (
        point_geom.distance(Point(A)) < tol or
        point_geom.distance(Point(B)) < tol
    )


def intersecao_permitida(intersecao, A, B):
    """
    A interseção só é permitida se acontecer exatamente em A e/ou B.
    """
    if intersecao.is_empty:
        return True

    if intersecao.geom_type == "Point":
        return ponto_eh_extremidade(intersecao, A, B)

    if intersecao.geom_type == "MultiPoint":
        return all(ponto_eh_extremidade(g, A, B) for g in intersecao.geoms)

    return False


def segmento_valido(A, B, obstaculos):
    """
    Segmento AB é válido se:
    - não atravessa triângulo
    - não passa dentro de triângulo
    - não toca aresta no meio
    - só pode tocar triângulos em A ou B
    - se AB coincidir com uma aresta do próprio triângulo, é permitido
    """
    if A == B:
        return False

    segmento = LineString([A, B])

    for triangulo in obstaculos:
        arestas = obter_arestas_triangulo(triangulo)

        # Se for exatamente uma aresta do triângulo, pode
        if any(mesmo_segmento(A, B, U, V) for U, V in arestas):
            continue

        # Não pode passar pelo interior
        if segmento.crosses(triangulo) or segmento.within(triangulo):
            return False

        intersecao = segmento.intersection(triangulo)

        if not intersecao_permitida(intersecao, A, B):
            return False

    return True


# ==========================================================
# GRAFO
# ==========================================================
def gerar_arestas_validas(pontos, obstaculos):
    arestas_validas = []

    for i in range(len(pontos)):
        for j in range(i + 1, len(pontos)):
            A = pontos[i]
            B = pontos[j]

            if segmento_valido(A, B, obstaculos):
                arestas_validas.append((A, B))

    return arestas_validas


# ==========================================================
# CAMINHOS
# ==========================================================
def gerar_grafo_adjacencia(pontos, arestas_validas):
    grafo = {p: [] for p in pontos}

    for A, B in arestas_validas:
        grafo[A].append(B)
        grafo[B].append(A)

    return grafo


def encontrar_caminhos(grafo, inicio, fim, limite=5000):
    caminhos = []

    def dfs(atual, caminho):
        if len(caminhos) >= limite:
            return

        if atual == fim:
            caminhos.append(caminho.copy())
            return

        for vizinho in grafo[atual]:
            if vizinho not in caminho:
                caminho.append(vizinho)
                dfs(vizinho, caminho)
                caminho.pop()

    dfs(inicio, [inicio])
    return caminhos


# ==========================================================
# DESENHO
# ==========================================================
def desenhar_mapa(largura, altura, inicio, fim, obstaculos, arestas_validas):
    fig, ax = plt.subplots(figsize=(10, 7))

    # Triângulos coloridos
    for triangulo in obstaculos:
        x, y = triangulo.exterior.xy
        ax.fill(x, y, alpha=0.4)
        ax.plot(x, y)

    # Arestas do grafo em azul
    for A, B in arestas_validas:
        ax.plot([A[0], B[0]], [A[1], B[1]], color="blue", alpha=0.5)

    # Início e fim
    ax.scatter(inicio[0], inicio[1], s=100, label="Início")
    ax.scatter(fim[0], fim[1], s=100, label="Fim")

    ax.set_xlim(0, largura)
    ax.set_ylim(0, altura)
    ax.set_xlabel("Eixo X")
    ax.set_ylabel("Eixo Y")
    ax.set_title("Mapa com Obstáculos Triangulares")
    ax.grid(True)
    ax.legend()

    plt.show()

# ==========================================================
# ENTRADA
# ==========================================================
def ler_float_positivo(mensagem):
    while True:
        try:
            valor = float(input(mensagem))
            if valor <= 0:
                print("Erro: digite um valor positivo.")
                continue
            return valor
        except ValueError:
            print("Erro: digite um número válido.")


def ler_int_positivo_ou_zero(mensagem):
    while True:
        try:
            valor = int(input(mensagem))
            if valor < 0:
                print("Erro: digite um inteiro maior ou igual a zero.")
                continue
            return valor
        except ValueError:
            print("Erro: digite um número inteiro válido.")


# ==========================================================
# MAIN
# ==========================================================
def main():
    print("=== Geração de mapa ===")

    inicio = (0.0, 0.0)

    x_final = ler_float_positivo("Digite o X do ponto final: ")
    y_final = ler_float_positivo("Digite o Y do ponto final: ")

    fim = (x_final, y_final)
    largura = x_final
    altura = y_final

    quantidade_obstaculos = ler_int_positivo_ou_zero("Quantidade de obstáculos: ")
    tamanho_triangulo = ler_float_positivo("Tamanho dos triângulos: ")

    if tamanho_triangulo > largura or tamanho_triangulo > altura:
        print("Erro: o tamanho do triângulo é maior que o mapa.")
        return

    obstaculos = gerar_obstaculos(
        quantidade_obstaculos,
        tamanho_triangulo,
        largura,
        altura,
        inicio,
        fim
    )

    if len(obstaculos) < quantidade_obstaculos:
        print(f"Aviso: só foi possível gerar {len(obstaculos)} de {quantidade_obstaculos} obstáculos.")

    pontos = obter_pontos_do_mapa(obstaculos, inicio, fim)
    arestas_validas = gerar_arestas_validas(pontos, obstaculos)
    grafo = gerar_grafo_adjacencia(pontos, arestas_validas)
    caminhos = encontrar_caminhos(grafo, inicio, fim, limite=5000)

    print("\n=== RESULTADO ===")
    print(f"Obstáculos gerados: {len(obstaculos)}")
    print(f"Pontos do grafo: {len(pontos)}")
    print(f"Arestas válidas: {len(arestas_validas)}")
    print(f"Caminhos encontrados: {len(caminhos)}")

    desenhar_mapa(largura, altura, inicio, fim, obstaculos, arestas_validas)


if __name__ == "__main__":
    main()