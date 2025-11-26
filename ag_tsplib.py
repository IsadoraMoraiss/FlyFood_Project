import random
import time
import os


# Lê o arquivo TSPLIB (.tsp)
def ler_tsplib(arquivo):
    with open(arquivo, 'r') as f:
        linhas = f.readlines()
    
    n = None
    start = False
    valores = []

    for linha in linhas:
        linha = linha.strip()

        if linha.startswith("DIMENSION"):
            n = int(linha.split(":")[1])

        if linha.startswith("EDGE_WEIGHT_SECTION"):
            start = True
            continue
        
        if start:
            if linha == "EOF":
                break
            partes = linha.split()
            valores.extend([float(x) for x in partes])
    
    if n is None:
        raise ValueError("DIMENSION não encontrada no arquivo Tsplib")
    
    matriz = [[0.0 for _ in range(n)]for _ in range(n)]
    idx = 0 
    for i in range(n-1):
        for j in range(i+1,n):
            matriz[i][j] = valores[idx]
            matriz[j][i] = valores[idx]
            idx += 1 
    
    return matriz


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
    filho = [None] * len(pai1)
    # copia o segmento do pai1
    filho[a:b] = pai1[a:b]

    #completa com pai2
    ptr = b
    for cidade in pai2:
        if cidade not in filho:
            if ptr >= len(filho):
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




def algoritmo_genetico(distancias, tamanho_pop=100, geracoes=300):
    n = len(distancias)
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
        populacao += nova_pop
        #criar uma nova populacao de sobreviventes
        #transferir o melhor indivduo para ela
        #transferir o restante (tamanho_pop-1) usando o torneio
        #lembrete: apagar o individuo da populacao original apos transferi-lo


    melhor = min(populacao, key=lambda ind: calcular_distancia_total(ind, distancias))
    return melhor, calcular_distancia_total(melhor, distancias)


def main():
    arquivo = "brazil58.tsp"

    if not os.path.exists(arquivo):
        raise FileNotFoundError(f"Arquivo '{arquivo}' não encontrado!")

    print(f"Executando algoritmo genético com o arquivo {arquivo}...")
    distancias = ler_tsplib(arquivo)

    inicio = time.time()
    rota, distancia = algoritmo_genetico(distancias, tamanho_pop=150, geracoes=400)
    fim = time.time()

    print("\nMelhor rota encontrada:", rota)
    print(f"Distância total: {distancia:.2f}")
    print(f"Tempo de execução: {fim - inicio:.2f}s")


if __name__ == "__main__":
    main()
