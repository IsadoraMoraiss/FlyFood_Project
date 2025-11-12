import math
import random
import time
import os


# Lê o arquivo TSPLIB (.tsp)
def ler_tsplib(arquivo):
    with open(arquivo, 'r') as f:
        linhas = f.readlines()

    coords = []
    start = False
    for linha in linhas:
        if "NODE_COORD_SECTION" in linha:
            start = True
            continue
        if "EOF" in linha:
            break
        if start:
            partes = linha.strip().split()
            if len(partes) >= 3:
                x, y = float(partes[1]), float(partes[2])
                coords.append((x, y))
    return coords



# Calcula a distância euclidiana entre duas cidades
def distancia_euclidiana(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)


# Cria a população inicial com rotas aleatórias
def criar_populacao(n_cidades, tamanho_pop):
    populacao = []
    for _ in range(tamanho_pop):
        individuo = list(range(n_cidades))
        random.shuffle(individuo)
        populacao.append(individuo)
    return populacao



# Calcula a distância total de uma rota
def calcular_distancia_total(rota, distancias):
    return sum(distancias[rota[i]][rota[(i+1)%len(rota)]] for i in range(len(rota)))



# Avalia a população 
def avaliar_populacao(populacao, distancias):
    return [(ind, calcular_distancia_total(ind, distancias)) for ind in populacao]


def selecao(pontuacoes, k=5):
    selecionados = random.sample(pontuacoes, k)
    selecionados.sort(key=lambda x: x[1])
    return selecionados[0][0]




def cruzamento(pai1, pai2):# Cruzamento (Ordered Crossover - OX)
    a, b = sorted(random.sample(range(len(pai1)), 2))
    filho = [None]*len(pai1)
    filho[a:b] = pai1[a:b]
    ptr = b
    for cidade in pai2:
        if cidade not in filho:
            if ptr >= len(pai1):
                ptr = 0
            filho[ptr] = cidade
            ptr += 1
    return filho


# Mutação (troca de cidades)
def mutacao(individuo, taxa=0.02):
    for i in range(len(individuo)):
        if random.random() < taxa:
            j = random.randint(0, len(individuo)-1)
            individuo[i], individuo[j] = individuo[j], individuo[i]
    return individuo




def algoritmo_genetico(coords, tamanho_pop=100, geracoes=300):
    n = len(coords)
    distancias = [[distancia_euclidiana(coords[i], coords[j]) for j in range(n)] for i in range(n)]

    populacao = criar_populacao(n, tamanho_pop)

    for _ in range(geracoes):
        pontuacoes = avaliar_populacao(populacao, distancias)
        nova_pop = []
        for _ in range(tamanho_pop):
            pai1 = selecao(pontuacoes)
            pai2 = selecao(pontuacoes)
            filho = cruzamento(pai1, pai2)
            mutacao(filho)
            nova_pop.append(filho)
        populacao = nova_pop

    melhor = min(populacao, key=lambda ind: calcular_distancia_total(ind, distancias))
    return melhor, calcular_distancia_total(melhor, distancias)


def main():
    arquivo = "brazil58.tsp"
    if not os.path.exists(arquivo):
        raise FileNotFoundError(f"Arquivo '{arquivo}' não encontrado!")

    print("➡️ Executando algoritmo genético com o arquivo 'brazil58.tsp'...")
    coords = ler_tsplib(arquivo)

    inicio = time.time()
    rota, distancia = algoritmo_genetico(coords, tamanho_pop=150, geracoes=400)
    fim = time.time()

    print("\nMelhor rota encontrada:", rota)
    print(f"Distância total: {distancia:.2f}")
    print(f"Tempo de execução: {fim - inicio:.2f}s")


if __name__ == "__main__":
    main()
