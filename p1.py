import math
import random
import matplotlib.pyplot as plt

# configurações
lado = 4
quantidade = 100

# plano cartesiano fixo
largura = 30
altura_plano = 30

# limite de tentativas por triângulo
max_tentativas = 100

triangulos = []

def distancia_ponto_segmento(P, A, B):
    # vetor AB
    ABx = B[0] - A[0]
    ABy = B[1] - A[1]

    # vetor AP
    APx = P[0] - A[0]
    APy = P[1] - A[1]

    # projeção
    t = (APx*ABx + APy*ABy) / (ABx*ABx + ABy*ABy)

    t = max(0, min(1, t))

    # ponto mais próximo
    Px = A[0] + t * ABx
    Py = A[1] + t * ABy

    dx = P[0] - Px
    dy = P[1] - Py

    return math.sqrt(dx*dx + dy*dy)

def distancia_segmentos(a1, a2, b1, b2):
    d1 = distancia_ponto_segmento(a1, b1, b2)
    d2 = distancia_ponto_segmento(a2, b1, b2)
    d3 = distancia_ponto_segmento(b1, a1, a2)
    d4 = distancia_ponto_segmento(b2, a1, a2)

    return min(d1, d2, d3, d4)

# --------------------------
# FUNÇÕES GEOMÉTRICAS
# --------------------------

def orientacao(p, q, r):
    return (q[1] - p[1])*(r[0] - q[0]) - (q[0] - p[0])*(r[1] - q[1])

def intersecta(p1, q1, p2, q2):
    o1 = orientacao(p1, q1, p2)
    o2 = orientacao(p1, q1, q2)
    o3 = orientacao(p2, q2, p1)
    o4 = orientacao(p2, q2, q1)

    return (o1 * o2 < 0) and (o3 * o4 < 0)

def arestas(triangulo):
    A, B, C = triangulo
    return [(A,B), (B,C), (C,A)]

dist_min = 0.5  # margem mínima (ajuste se quiser)

def colide(t1, t2):
    for a1 in arestas(t1):
        for a2 in arestas(t2):

            # 1. cruzamento
            if intersecta(a1[0], a1[1], a2[0], a2[1]):
                return True

            # 2. proximidade (evita encostar)
            if distancia_segmentos(a1[0], a1[1], a2[0], a2[1]) < dist_min:
                return True

    return False

# --------------------------
# GERADOR DE TRIÂNGULOS
# --------------------------

for _ in range(quantidade):

    tentativas = 0
    criado = False

    while tentativas < max_tentativas and not criado:
        tentativas += 1

        # garante que o triângulo fique dentro do plano
        x = random.randint(0, largura - lado)
        y = random.randint(0, altura_plano - int((math.sqrt(3)/2)*lado))

        altura = (math.sqrt(3)/2) * lado

        A = (x, y)
        B = (x + lado, y)
        C = (x + lado/2, y + altura)

        novo = (A,B,C)

        # verificar colisão
        colisao = False
        for t in triangulos:
            if colide(novo, t):
                colisao = True
                break

        if not colisao:
            triangulos.append(novo)
            criado = True

# --------------------------
# PLOT
# --------------------------

for (A,B,C) in triangulos:
    xs = [A[0], B[0], C[0], A[0]]
    ys = [A[1], B[1], C[1], A[1]]

    plt.plot(xs, ys)
    # plt.scatter(xs[:-1], ys[:-1])

plt.title("Triângulos sem colisão")
plt.xlim(0, largura)
plt.ylim(0, altura_plano)
plt.grid()
plt.axis("equal")

plt.show()