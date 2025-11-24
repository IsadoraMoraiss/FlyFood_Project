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

# adicionando geração de gráfico para as rotas(melhoria p/2VA)
import matplotlib.pyplot as plt

def plotar_rota(rota, inicio, pontos, matriz, titulo="Rota"):
    plt.figure(figsize=(8, 8))
    plt.title(titulo)

    # desenha a grade e pontos
    for r in range(len(matriz)):
        for c in range(len(matriz[0])):
            plt.scatter(c, -r, color='lightgray')
            valor = matriz[r][c]
            if valor != '0':
                plt.text(c, -r, valor, fontsize=8, ha='center', va='center')

    # pontos de entrega
    xs = [pontos[p][1] for p in pontos if p != 'R']
    ys = [-pontos[p][0] for p in pontos if p != 'R']
    plt.scatter(xs, ys, c='orange', s=60, label='Entregas')

    # monta caminho R -> rota -> R
    caminho = [inicio] + [pontos[p] for p in rota] + [inicio]

    for i in range(len(caminho) - 1):
        p0 = caminho[i]
        p1 = caminho[i + 1]
        x0, y0 = p0[1], -p0[0]
        x1, y1 = p1[1], -p1[0]

        inter_x, inter_y = x1, y0

        plt.plot([x0, inter_x], [y0, inter_y], 'b-', linewidth=1.5)
        plt.plot([inter_x, x1], [inter_y, y1], 'b-', linewidth=1.5)

        dist = abs(p0[0] - p1[0]) + abs(p0[1] - p1[1])
        xm = (x0 + inter_x + x1) / 3
        ym = (y0 + inter_y + y1) / 3
        plt.text(xm, ym, f"{dist}", color='purple')

    plt.scatter(inicio[1], -inicio[0], c='red', s=100, label='Início (R)')

    plt.legend()
    plt.grid(True)
    plt.axis('equal')
    plt.show()
    plt.close()

def main():
    Matrizes = "historico_matrizes.txt"

    print("Bem-vindo ao FlyFood! Otimizador de Rotas por Drone")
    print("1 - Adicionar nova matriz")
    print("2 - Usar última matriz salva")

    escolha = input("- ").strip()

    if escolha == "1":
        salvar_matriz(Matrizes)

    try:
        matriz = ler_matriz(Matrizes)
    except Exception as e:
        print("Erro ao ler matriz:", e)
        print("Crie uma matriz primeiro (opção 1).")
        return

    inicio_t = time.time()
    rota, distancia, inicio, pontos, matriz_lida = calcular_rota_otima(matriz)
    fim_t = time.time()
    tempo_exec = fim_t - inicio_t

    # rota é sempre lista (pode ser vazia)
    if rota:
        print("\nRota ótima:", " → ".join(rota))
        print("Distância:", distancia)
        print(f"Tempo: {tempo_exec:.6f} s")
    else:
        # se rota vazia mas existe início, mostramos mensagem e ainda plotamos
        if inicio is None:
            print("\nPonto inicial 'R' não encontrado na matriz.")
            return
        else:
            print("\nNão há destinos (apenas 'R' na matriz) ou melhor rota vazia. Mostrando mapa com ponto R.")

    # salva no arquivo sempre (matriz já salva antes), aqui apenas anota resultado
    with open(Matrizes, "a", encoding="utf-8") as f:
        f.write("\n")
        if rota:
            f.write("Rota ótima: " + " → ".join(rota) + "\n")
            f.write(f"Distância mínima: {distancia}\n")
        else:
            f.write("Rota ótima: (nenhuma)\n")
            f.write("Distância mínima: 0\n")
        f.write(f"Tempo execução: {tempo_exec:.6f} s\n")

    # plota (mesmo se rota vazia, o plot mostrará R)
    plotar_rota(rota, inicio, pontos, matriz_lida,
                titulo=f"Rota ótima ({distancia} dronom.)")

if __name__ == "__main__":
    main()



