

def ler_matriz():
    primeira_linha = input().strip()
    while primeira_linha == "":
        primeira_linha = input().strip()
    partes = primeira_linha.split()
    linhas = int(partes[0])
    matriz = []
    for _ in range(linhas):
        linha = input().strip()
        while linha == "":
            linha = input().strip()
        elementos = linha.split()
        matriz.append(elementos)
    return matriz

def encontrar_pontos(matriz):  # Encontra todos os pontos nomeados na matriz
    pontos = {}
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            valor = matriz[i][j]
            if valor != 0:
                pontos[valor] = (i, j)
    return pontos

def calcular_distancia(p1, p2):  # Calcula a distância Manhattan entre dois pontos
    dis_linha = p1[0] - p2[0]
    dis_coluna = p1[1] - p2[1]

    # Calcula valores absolutos sem usar a função abs()
    if dis_linha < 0:
        dis_linha = -dis_linha
    if dis_coluna < 0:
        dis_coluna = -dis_coluna

    return dis_linha + dis_coluna

def gerar_permutacoes(elementos):  # Gera todas as permutações possíveis de uma lista de elementos
    if len(elementos) <= 1:
        return [elementos]

    resultado = []
    for i in range(len(elementos)):
        elemento_atual = elementos[i]
        elementos_restantes = elementos[:i] + elementos[i + 1:]
        for p in gerar_permutacoes(elementos_restantes):
            resultado.append([elemento_atual] + p)

    return resultado

def encontrar_rota_otimizada():
    # Encontra a rota mais curta para as entregas do drone
    matriz = ler_matriz()
    pontos = encontrar_pontos(matriz)

    if 'R' not in pontos:
        return "Ponto R não encontrado"

    ponto_inicial = pontos['R']
    destinos = [p for p in pontos if p != 'R']

    if not destinos:
        return ""

    permutacoes = gerar_permutacoes(destinos)

    rota_otima = None
    distancia_minima = None

    for rota in permutacoes:
        custo = 0 
        ponto_atual = ponto_inicial
        for ponto in rota:
            proximo_ponto = pontos[ponto]
            custo += calcular_distancia(ponto_atual, proximo_ponto)
            ponto_atual = proximo_ponto
            if rota_otima is None or custo < distancia_minima:
                rota_otima = rota
                distancia_minima = custo
        if rota_otima:
            return ' '.join(rota_otima)
    return ""

if __name__ == "__main__":
    resultado = encontrar_rota_otimizada()
    print(resultado)
