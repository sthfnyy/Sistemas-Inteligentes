import math
import random
from collections import deque
from matplotlib import pyplot as plt
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


#def ponto_em_triangulo_ou_borda(triangulo, ponto):
   # p = Point(ponto)
  #  return triangulo.contains(p) or triangulo.touches(p)


def triangulos_colidem_ou_tocam(t1, t2):
    return t1.intersects(t2) #gerar o código matematico e chamar a função 


# ==========================================================
# GERAÇÃO DOS OBSTÁCULOS
# ==========================================================
def triangulo_valido(novo_triangulo, obstaculos, inicio, fim):
    #if ponto_em_triangulo_ou_borda(novo_triangulo, inicio):
    #    return False

  #  if ponto_em_triangulo_ou_borda(novo_triangulo, fim):
   #     return False

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
        pontos.extend(obter_vertices_triangulo(triangulo)) #fez uma varredura pegando todos gerados pertencentes aos triangulos

    ponto_unicos = [] #lista para armazenar os pontos únicos
    for p in pontos:#verificar se o pontos já foi adicionado para evitar duplicatas
        if p not in ponto_unicos: #verificar se o pontos já foi adicionado para evitar duplicatas
            ponto_unicos.append(p)

    return ponto_unicos#retorna a lista de pontos únicos


# ==========================================================
# VALIDAÇÃO DE ARESTA
# ==========================================================
def mesmo_segmento(a1, a2, b1, b2):
    return {a1, a2} == {b1, b2}


def ponto_eh_extremidade(point_geom, A, B, tol=1e-9):
    return point_geom.distance(Point(A)) < tol or point_geom.distance(Point(B)) < tol


def intersecao_permitida(intersecao, A, B):
    if intersecao.is_empty:
        return True

    if intersecao.geom_type == "Point":
        return ponto_eh_extremidade(intersecao, A, B)

    if intersecao.geom_type == "MultiPoint":
        return all(ponto_eh_extremidade(g, A, B) for g in intersecao.geoms)

    return False


def segmento_valido(A, B, obstaculos):
    if A == B:
        return False

    segmento = LineString([A, B])

    for triangulo in obstaculos:
        arestas = obter_arestas_triangulo(triangulo)

    # TODO deixar em uma linguagem mais iniciante: para cada triangulo, pega as arestas do triangulo e compara com o segmento que queremos criar


        # Se for exatamente uma aresta do triângulo, pode
        #verificar
        # if any(mesmo_segmento(A, B, U, V) for U, V in arestas):
        #     continue

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

    for triangulo in obstaculos:
        arestas = obter_arestas_triangulo(triangulo)
        for U, V in arestas:
            arestas_validas.append((U, V))
        #print("Arestas do triangulo:", arestas)
        #arestas_validas.extend(arestas)
    print("arestas_validas:",arestas_validas)

    for i in range(len(pontos)):
        for j in range(i + 1, len(pontos)):
            A = pontos[i]
            B = pontos[j]

            if segmento_valido(A, B, obstaculos):
                arestas_validas.append((A, B))

    print("arestas_validas 2:",arestas_validas)

    return arestas_validas


def gerar_grafo_adjacencia(pontos, arestas_validas):
    grafo = {p: [] for p in pontos}

    for A, B in arestas_validas:
        grafo[A].append(B)
        grafo[B].append(A)

    return grafo


# ==========================================================
# BFS
# ==========================================================
def bfs_caminho(grafo, inicio, fim):
    fila = deque([[inicio]])
    visitados = {inicio}
#TODO deixar em uma linguagem mais iniciante: criar uma fila para armazenar os caminhos a serem explorados e um conjunto para marcar os pontos já visitados
    while fila:
        caminho = fila.popleft()
        atual = caminho[-1]

        if atual == fim:
            return caminho

        for vizinho in grafo[atual]:
            if vizinho not in visitados:
                visitados.add(vizinho)
                fila.append(caminho + [vizinho])

    return None


def comprimento_caminho(caminho):
    if not caminho or len(caminho) < 2:
        return 0.0

    total = 0.0
    for i in range(len(caminho) - 1):
        total += math.dist(caminho[i], caminho[i + 1])
    return total


# ==========================================================
# DESENHO
# ==========================================================
def desenhar_mapa(largura, altura, inicio, fim, obstaculos, arestas_validas, caminho=None):
    fig, ax = plt.subplots(figsize=(10, 7))

    # Triângulos coloridos
    for triangulo in obstaculos:
        x, y = triangulo.exterior.xy
        ax.fill(x, y, alpha=0.4)
        ax.plot(x, y)

    # Arestas do grafo
    for A, B in arestas_validas:
        ax.plot([A[0], B[0]], [A[1], B[1]], color="blue", alpha=1.0)

    # Caminho BFS destacado
    if caminho and len(caminho) > 1:
        for i in range(len(caminho) - 1):
            A = caminho[i]
            B = caminho[i + 1]
            ax.plot(
                [A[0], B[0]], [A[1], B[1]],
                color="red", linewidth=3,
                label="Caminho BFS" if i == 0 else None
            )

    # Início e fim
    ax.scatter(inicio[0], inicio[1], s=100, label="Inicio")
    ax.scatter(fim[0], fim[1], s=100, label="Fim")

    ax.set_xlim(0, largura)
    ax.set_ylim(0, altura)
    ax.set_xlabel("Eixo X")
    ax.set_ylabel("Eixo Y")
    ax.set_title("Mapa com Obstaculos Triangulares e Caminho BFS")
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
            print("Erro: digite um numero valido.")


#TODO bota na main
def ler_int_positivo_ou_zero(mensagem):
    while True:
        try:
            valor = int(input(mensagem))
            if valor < 0:
                print("Erro: digite um inteiro maior ou igual a zero.")
                continue
            return valor
        except ValueError:
            print("Erro: digite um numero inteiro valido.")


# ==========================================================
# MAIN
# ==========================================================
def main():
    print("=== Geracao de mapa ===")

    inicio = (0.0, 0.0)

    x_final = ler_float_positivo("Digite o X do ponto final: ")
    y_final = ler_float_positivo("Digite o Y do ponto final: ")

    fim = (x_final, y_final)
    largura = x_final
    altura = y_final

    quantidade_obstaculos = ler_int_positivo_ou_zero("Quantidade de obstaculos: ")
    tamanho_triangulo = ler_float_positivo("Tamanho dos triangulos: ")

    if tamanho_triangulo > largura or tamanho_triangulo > altura:
        print("Erro: o tamanho do triangulo eh maior que o mapa.")
        return

    obstaculos = gerar_obstaculos(quantidade_obstaculos, tamanho_triangulo, largura, altura, inicio, fim)

    if len(obstaculos) < quantidade_obstaculos:
        print(f"So foi possível gerar {len(obstaculos)} de {quantidade_obstaculos} obstaculos.")

    pontos = obter_pontos_do_mapa(obstaculos, inicio, fim)
    arestas_validas = gerar_arestas_validas(pontos, obstaculos)
    grafo = gerar_grafo_adjacencia(pontos, arestas_validas)
    caminho = bfs_caminho(grafo, inicio, fim)

    print("\n=== RESULTADO ===")
    print(f"Obstaculos gerados: {len(obstaculos)}")
    print(f"Pontos do grafo: {len(pontos)}")
    print(f"Arestas validas: {len(arestas_validas)}")

    if caminho:
        print("Caminho encontrado (BFS):")
        for p in caminho:
            print(p)
        print(f"Comprimento total do caminho: {comprimento_caminho(caminho):.2f}")
    else:
        print("Nenhum caminho encontrado.")

    desenhar_mapa(largura, altura, inicio, fim, obstaculos, arestas_validas, caminho)


if __name__ == "__main__":
    main()