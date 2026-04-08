import math
import random
from collections import deque
import matplotlib.pyplot as plt


# ==========================================================
# FUNCOES BASICAS DE GEOMETRIA
# ==========================================================

def distancia_entre_pontos(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return math.sqrt(dx * dx + dy * dy)


def orientacao(p, q, r):
    valor = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])

    if valor == 0:
        return 0
    elif valor > 0:
        return 1
    else:
        return 2


def ponto_no_segmento(p, q, r):
    if (
        min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and
        min(p[1], r[1]) <= q[1] <= max(p[1], r[1])
    ):
        return True
    return False


def segmentos_se_intersectam(p1, q1, p2, q2):
    o1 = orientacao(p1, q1, p2)
    o2 = orientacao(p1, q1, q2)
    o3 = orientacao(p2, q2, p1)
    o4 = orientacao(p2, q2, q1)

    if o1 != o2 and o3 != o4:
        return True

    if o1 == 0 and ponto_no_segmento(p1, p2, q1):
        return True

    if o2 == 0 and ponto_no_segmento(p1, q2, q1):
        return True

    if o3 == 0 and ponto_no_segmento(p2, p1, q2):
        return True

    if o4 == 0 and ponto_no_segmento(p2, q1, q2):
        return True

    return False


def area_triangulo(a, b, c):
    return abs(
        a[0] * (b[1] - c[1]) +
        b[0] * (c[1] - a[1]) +
        c[0] * (a[1] - b[1])
    ) / 2.0


def ponto_dentro_ou_borda_triangulo(ponto, triangulo):
    a, b, c = triangulo

    area_total = area_triangulo(a, b, c)
    area1 = area_triangulo(ponto, b, c)
    area2 = area_triangulo(a, ponto, c)
    area3 = area_triangulo(a, b, ponto)

    soma = area1 + area2 + area3

    if abs(soma - area_total) < 1e-9:
        return True

    return False


def ponto_igual(p1, p2, tolerancia=1e-9):
    return abs(p1[0] - p2[0]) < tolerancia and abs(p1[1] - p2[1]) < tolerancia


# ==========================================================
# FUNCOES DO TRIANGULO
# ==========================================================

def criar_triangulo_isosceles(x_base, y_base, tamanho):
    a = (x_base, y_base)
    b = (x_base + tamanho, y_base)
    c = (x_base + tamanho / 2, y_base + tamanho)
    return (a, b, c)


def obter_vertices_triangulo(triangulo):
    a, b, c = triangulo
    return [a, b, c]


def obter_arestas_triangulo(triangulo):
    a, b, c = triangulo
    return [(a, b), (b, c), (c, a)]


def triangulo_dentro_do_mapa(triangulo, largura, altura):
    for x, y in triangulo:
        if x < 0 or x > largura or y < 0 or y > altura:
            return False
    return True


def triangulos_colidem_ou_tocam(t1, t2):
    arestas_t1 = obter_arestas_triangulo(t1)
    arestas_t2 = obter_arestas_triangulo(t2)

    # verifica se alguma aresta de um triangulo intersecta uma aresta do outro
    for a1_inicio, a1_fim in arestas_t1:
        for a2_inicio, a2_fim in arestas_t2:
            if segmentos_se_intersectam(a1_inicio, a1_fim, a2_inicio, a2_fim):
                return True

    # verifica se algum vertice de t1 esta dentro ou na borda de t2
    for ponto in t1:
        if ponto_dentro_ou_borda_triangulo(ponto, t2):
            return True

    # verifica se algum vertice de t2 esta dentro ou na borda de t1
    for ponto in t2:
        if ponto_dentro_ou_borda_triangulo(ponto, t1):
            return True

    return False


# ==========================================================
# GERACAO DOS OBSTACULOS
# ==========================================================

def triangulo_valido(novo_triangulo, obstaculos, inicio, fim):
    if ponto_dentro_ou_borda_triangulo(inicio, novo_triangulo):
        return False

    if ponto_dentro_ou_borda_triangulo(fim, novo_triangulo):
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
        vertices = obter_vertices_triangulo(triangulo)
        for vertice in vertices:
            pontos.append(vertice)

    pontos_unicos = []
    for p in pontos:
        existe = False
        for ponto_salvo in pontos_unicos:
            if ponto_igual(p, ponto_salvo):
                existe = True
                break

        if not existe:
            pontos_unicos.append(p)

    return pontos_unicos


# ==========================================================
# VALIDACAO DE ARESTA
# ==========================================================

def mesmo_segmento(a1, a2, b1, b2):
    return (
        (ponto_igual(a1, b1) and ponto_igual(a2, b2)) or
        (ponto_igual(a1, b2) and ponto_igual(a2, b1))
    )


def intersecao_apenas_nas_extremidades(A, B, U, V):
    pontos_em_comum = 0

    if ponto_igual(A, U) or ponto_igual(A, V):
        pontos_em_comum += 1

    if ponto_igual(B, U) or ponto_igual(B, V):
        pontos_em_comum += 1

    if pontos_em_comum > 0:
        return True

    return False


def segmento_passa_dentro_do_triangulo(A, B, triangulo):
    # verifica se o ponto medio do segmento fica dentro do triangulo
    ponto_medio = ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2)

    if ponto_dentro_ou_borda_triangulo(ponto_medio, triangulo):
        # se o ponto medio estiver exatamente numa aresta, ainda pode ser valido em alguns casos,
        # mas para deixar a regra mais simples e segura, vamos considerar invalido
        return True

    return False


def segmento_valido(A, B, obstaculos):
    if ponto_igual(A, B):
        return False

    for triangulo in obstaculos:
        arestas = obter_arestas_triangulo(triangulo)

        # se for exatamente uma aresta do triangulo, pode
        for U, V in arestas:
            if mesmo_segmento(A, B, U, V):
                return True

        # verifica se cruza alguma aresta do triangulo em lugar proibido
        for U, V in arestas:
            if segmentos_se_intersectam(A, B, U, V):
                if not intersecao_apenas_nas_extremidades(A, B, U, V):
                    return False

        # verifica se o segmento passa por dentro do triangulo
        if segmento_passa_dentro_do_triangulo(A, B, triangulo):
            return False

    return True


# ==========================================================
# GRAFO
# ==========================================================

def gerar_arestas_validas(pontos, obstaculos):
    arestas_validas = []

    # adiciona as arestas dos triangulos
    for triangulo in obstaculos:
        arestas = obter_arestas_triangulo(triangulo)
        for U, V in arestas:
            arestas_validas.append((U, V))

    # testa ligacao entre todos os pontos do mapa
    for i in range(len(pontos)):
        for j in range(i + 1, len(pontos)):
            A = pontos[i]
            B = pontos[j]

            if segmento_valido(A, B, obstaculos):
                ja_existe = False

                for X, Y in arestas_validas:
                    if mesmo_segmento(A, B, X, Y):
                        ja_existe = True
                        break

                if not ja_existe:
                    arestas_validas.append((A, B))

    return arestas_validas


def gerar_grafo_adjacencia(pontos, arestas_validas):
    grafo = {}

    for p in pontos:
        grafo[p] = []

    for A, B in arestas_validas:
        grafo[A].append(B)
        grafo[B].append(A)

    return grafo


# ==========================================================
# BFS
# ==========================================================

def bfs_caminho(grafo, inicio, fim):
    fila = deque()
    fila.append([inicio])

    visitados = set()
    visitados.add(inicio)

    while len(fila) > 0:
        caminho_atual = fila.popleft()
        ponto_atual = caminho_atual[-1]

        if ponto_atual == fim:
            return caminho_atual

        vizinhos = grafo[ponto_atual]

        for vizinho in vizinhos:
            if vizinho not in visitados:
                visitados.add(vizinho)

                novo_caminho = caminho_atual + [vizinho]
                fila.append(novo_caminho)

    return None


def comprimento_caminho(caminho):
    if caminho is None or len(caminho) < 2:
        return 0.0

    total = 0.0

    for i in range(len(caminho) - 1):
        total += distancia_entre_pontos(caminho[i], caminho[i + 1])

    return total


# ==========================================================
# DESENHO
# ==========================================================

def desenhar_mapa(largura, altura, inicio, fim, obstaculos, arestas_validas, caminho=None):
    fig, ax = plt.subplots(figsize=(10, 7))

    # desenha os triangulos
    for triangulo in obstaculos:
        a, b, c = triangulo
        xs = [a[0], b[0], c[0], a[0]]
        ys = [a[1], b[1], c[1], a[1]]

        ax.fill(xs, ys, alpha=0.4)
        ax.plot(xs, ys)

    # desenha as arestas do grafo
    for A, B in arestas_validas:
        ax.plot([A[0], B[0]], [A[1], B[1]], color="blue", alpha=1.0)

    # desenha o caminho encontrado
    if caminho is not None and len(caminho) > 1:
        for i in range(len(caminho) - 1):
            A = caminho[i]
            B = caminho[i + 1]

            ax.plot(
                [A[0], B[0]],
                [A[1], B[1]],
                color="red",
                linewidth=3,
                label="Caminho BFS" if i == 0 else None
            )

    # desenha inicio e fim
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
            else:
                return valor

        except ValueError:
            print("Erro: digite um numero valido.")


def ler_int_positivo_ou_zero(mensagem):
    while True:
        try:
            valor = int(input(mensagem))

            if valor < 0:
                print("Erro: digite um inteiro maior ou igual a zero.")
            else:
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

    obstaculos = gerar_obstaculos(
        quantidade_obstaculos,
        tamanho_triangulo,
        largura,
        altura,
        inicio,
        fim
    )

    if len(obstaculos) < quantidade_obstaculos:
        print("So foi possivel gerar", len(obstaculos), "de", quantidade_obstaculos, "obstaculos.")

    pontos = obter_pontos_do_mapa(obstaculos, inicio, fim)
    arestas_validas = gerar_arestas_validas(pontos, obstaculos)
    grafo = gerar_grafo_adjacencia(pontos, arestas_validas)
    caminho = bfs_caminho(grafo, inicio, fim)

    print("\n=== RESULTADO ===")
    print("Obstaculos gerados:", len(obstaculos))
    print("Pontos do grafo:", len(pontos))
    print("Arestas validas:", len(arestas_validas))

    if caminho is not None:
        print("Caminho encontrado (BFS):")
        for p in caminho:
            print(p)

        print("Comprimento total do caminho:", round(comprimento_caminho(caminho), 2))
    else:
        print("Nenhum caminho encontrado.")

    desenhar_mapa(largura, altura, inicio, fim, obstaculos, arestas_validas, caminho)


if __name__ == "__main__":
    main()