import time
import itertools

def salvar_matriz(Matrizes): #Lê uma matriz digitada pelo usuário e adiciona ao arquivo de histórico.
    print("Insira a matriz desejada: ")
    primeira_linha = input().strip()  # Lê a primeira linha (linhas e colunas)
    while not primeira_linha:
        primeira_linha = input().strip()
    linhas, colunas = map(int, primeira_linha.split())

    conteudo = [primeira_linha]


    for _ in range(linhas):
        linha = input().strip()
        while not linha:
            linha = input().strip()
        conteudo.append(linha)

    # Adiciona delimitador antes da nova matriz
    with open(Matrizes, "a", encoding="utf-8") as f:
        f.write("\n---\n")
        f.write("\n".join(conteudo))

    return Matrizes


def ler_matriz(Matrizes): #Lê apenas a última matriz salva no arquivo.
    with open(Matrizes, "r", encoding="utf-8") as f:
        conteudo = f.read().strip()

    blocos = [b.strip() for b in conteudo.split('---') if b.strip()]
    ultima = blocos[-1]  # pega a última matriz

    linhas = [linha.strip() for linha in ultima.splitlines() if linha.strip()]
    linhas_e_colunas = linhas[0].split()
    n_linhas = int(linhas_e_colunas[0])
    matriz = [linha.split() for linha in linhas[1:n_linhas + 1]]

    return matriz


def encontrar_pontos(matriz):
    pontos = {}
    for i, linha in enumerate(matriz):
        for j, valor in enumerate(linha):
            if valor != '0':
                pontos[valor] = (i, j)
    return pontos


def calcular_distancia(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def calcular_rota_otima(matriz):
    pontos = encontrar_pontos(matriz)

    if 'R' not in pontos:
        return "ponto inicial 'R' não encontrado.", 0

    ponto_inicial = pontos['R']
    destinos = [p for p in pontos.keys() if p != 'R']

    permutacoes = itertools.permutations(destinos)

    distancia_minima = float('inf')
    melhor_rota = None

    for rota in permutacoes:
        custo_total = 0
        ponto_atual = ponto_inicial

        for ponto in rota:
            custo_total += calcular_distancia(ponto_atual, pontos[ponto])
            ponto_atual = pontos[ponto]

        custo_total += calcular_distancia(ponto_atual, ponto_inicial)

        if custo_total < distancia_minima:
            distancia_minima = custo_total
            melhor_rota = rota

    if melhor_rota:
        return melhor_rota, distancia_minima
    else:
        return [], 0


def main():
    Matrizes = "historico_matrizes.txt"
    print("Bem-vindo ao FlyFood! Um Otimizador de rotas de Entregas por Drone")
    print("Deseja adicionar uma nova matriz ou usar a última salva?")
    print("1 - Adicionar nova matriz")
    print("2 - Usar última matriz salva")

    escolha = input("- ").strip()

    if escolha == "1":
        salvar_matriz(Matrizes)

    try:
        matriz = ler_matriz(Matrizes)
    except:
        print("Nenhum arquivo encontrado. Crie uma matriz primeiro.")
        return

    inicio = time.time()
    rota, distancia = calcular_rota_otima(matriz)
    fim = time.time()

    if rota:
        print("\nrota ótima:", ' '.join(rota))
        print("Distância Dronômetros:", distancia)
    else:
        print("\nNenhuma rota encontrada.")
    print(f"Tempo de execução: {fim - inicio:.6f} segundos")


if __name__ == "__main__":
    main()

