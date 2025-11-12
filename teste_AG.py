import random
import time


def salvar_matriz(arquivo):
    """Permite o usuário digitar uma matriz e salva no histórico."""
    print("Insira a matriz (linhas e colunas, depois a matriz):")
    primeira_linha = input().strip()
    while not primeira_linha:
        primeira_linha = input().strip()
    linhas, colunas = map(int, primeira_linha.split())

    conteudo = [primeira_linha]
    for _ in range(linhas):
        linha = input().strip()
        while not linha:
            linha = input().strip()
        conteudo.append(linha)

    with open(arquivo, "a", encoding="utf-8") as f:
        f.write("\n---\n")
        f.write("\n".join(conteudo))
    return arquivo


def ler_matriz(arquivo):
    """Lê a última matriz salva."""
    with open(arquivo, "r", encoding="utf-8") as f:
        conteudo = f.read().strip()

    blocos = [b.strip() for b in conteudo.split('---') if b.strip()]
    ultima = blocos[-1]

    linhas = [linha.strip() for linha in ultima.splitlines() if linha.strip()]
    linhas_e_colunas = linhas[0].split()
    n_linhas = int(linhas_e_colunas[0])
    matriz = [linha.split() for linha in linhas[1:n_linhas + 1]]

    return matriz


def encontrar_pontos(matriz):
    """Encontra as posições (x,y) de cada ponto na matriz."""
    pontos = {}
    for i, linha in enumerate(matriz):
        for j, valor in enumerate(linha):
            if valor != '0':
                pontos[valor] = (i, j)
    return pontos


def calcular_distancia(p1, p2):
    """Distância de Manhattan."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def matriz_para_distancias(matriz):
    """Transforma a matriz de pontos em uma matriz de distâncias."""
    pontos = encontrar_pontos(matriz)
    rotulos = list(pontos.keys())
    n = len(rotulos)
    dist = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                dist[i][j] = calcular_distancia(pontos[rotulos[i]], pontos[rotulos[j]])
    return dist, rotulos



def calcular_custo(rotação, distancias):
    """Calcula o custo total de uma rota."""
    custo = 0
    for i in range(len(rotação) - 1):
        custo += distancias[rotação[i]][rotação[i + 1]]
    custo += distancias[rotação[-1]][rotação[0]]  # retorna ao início
    return custo


def criar_populacao(tamanho_pop, num_cidades):
    """Gera população inicial com rotas aleatórias."""
    populacao = []
    for _ in range(tamanho_pop):
        rota = list(range(num_cidades))
        random.shuffle(rota)
        populacao.append(rota)
    return populacao


def selecionar_pais(populacao, distancias):
    """Seleciona pais pelo método de torneio."""
    competidores = random.sample(populacao, 4)
    competidores.sort(key=lambda r: calcular_custo(r, distancias))
    return competidores[0], competidores[1]


def cruzamento(pai1, pai2):
    """Cruzamento de ordem (OX)."""
    inicio, fim = sorted(random.sample(range(len(pai1)), 2))
    filho = [None] * len(pai1)
    filho[inicio:fim] = pai1[inicio:fim]

    pos = fim
    for cidade in pai2:
        if cidade not in filho:
            if pos >= len(filho):
                pos = 0
            filho[pos] = cidade
            pos += 1
    return filho


def mutacao(rota, taxa_mutacao=0.1):
    """Troca aleatória de duas cidades."""
    for i in range(len(rota)):
        if random.random() < taxa_mutacao:
            j = random.randint(0, len(rota) - 1)
            rota[i], rota[j] = rota[j], rota[i]
    return rota


def algoritmo_genetico_tsp(distancias, rotulos, tamanho_pop=100, geracoes=500, taxa_mutacao=0.1):
    """Executa o algoritmo genético para resolver o TSP."""
    populacao = criar_populacao(tamanho_pop, len(distancias))
    melhor_rota = min(populacao, key=lambda r: calcular_custo(r, distancias))
    melhor_custo = calcular_custo(melhor_rota, distancias)

    for _ in range(geracoes):
        nova_pop = []
        for _ in range(tamanho_pop // 2):
            pai1, pai2 = selecionar_pais(populacao, distancias)
            filho1 = cruzamento(pai1, pai2)
            filho2 = cruzamento(pai2, pai1)
            nova_pop.append(mutacao(filho1, taxa_mutacao))
            nova_pop.append(mutacao(filho2, taxa_mutacao))
        populacao = nova_pop

        melhor_atual = min(populacao, key=lambda r: calcular_custo(r, distancias))
        custo_atual = calcular_custo(melhor_atual, distancias)
        if custo_atual < melhor_custo:
            melhor_rota, melhor_custo = melhor_atual, custo_atual

    rota_nomeada = [rotulos[i] for i in melhor_rota]
    return rota_nomeada, melhor_custo



def main():
    arquivo = "historico_matrizes_AG.txt"
    print("Algoritmo Genético - Otimização de Rotas (TSP)")
    print("1 - Inserir nova matriz")
    print("2 - Usar última matriz salva")
    escolha = input("- ").strip()

    if escolha == "1":
        salvar_matriz(arquivo)

    try:
        matriz = ler_matriz(arquivo)
    except FileNotFoundError:
        print("Nenhuma matriz encontrada. Crie uma nova primeiro.")
        return

    distancias, rotulos = matriz_para_distancias(matriz)
    print(f"\n📍 Pontos detectados: {len(rotulos)}")

    inicio = time.time()
    rota, custo = algoritmo_genetico_tsp(distancias, rotulos)
    fim = time.time()

    tempo_exec = fim - inicio

    print("\nResultados:")
    print("Rota encontrada:", " → ".join(rota))
    print(f"Custo total(Dronômetros): {custo}")
    print(f"Tempo de execução: {tempo_exec:.6f} segundos")

    with open(arquivo, "a", encoding="utf-8") as f:
        f.write("\n\nResultado da execução:\n")
        f.write(f"Rota encontrada: {' → '.join(rota)}\n")
        f.write(f"Custo total: {custo}\n")
        f.write(f"Tempo de execução: {tempo_exec:.6f} segundos\n")


if __name__ == "__main__":
    main()
