import random
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict, Optional
import time 
import os


def manhattan(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def gerar_rotulos(n: int) -> List[str]:
    rotulos = []
    for i in range(n):
        r = ''
        temp = i
        while True:
            r = chr(65 + temp % 26) + r
            temp = temp // 26 - 1
            if temp < 0:
                break
        rotulos.append(r)
    return rotulos


def gerar_matriz_aleatoria(linhas: int, colunas: int, num_pontos: int) -> Tuple[List[List[str]], Tuple[int, int], Dict[str, Tuple[int, int]]]:
    matriz = [['0' for _ in range(colunas)] for _ in range(linhas)]

    todas_posicoes = [(r, c) for r in range(linhas) for c in range(colunas)]

    posicao_inicio = random.choice(todas_posicoes)
    matriz[posicao_inicio[0]][posicao_inicio[1]] = 'R'
    todas_posicoes.remove(posicao_inicio)

    rotulos_entregas = gerar_rotulos(num_pontos)
    pontos_entregas = {}

    for rotulo in rotulos_entregas:
        pos = random.choice(todas_posicoes)
        todas_posicoes.remove(pos)
        matriz[pos[0]][pos[1]] = rotulo
        pontos_entregas[rotulo] = pos

    return matriz, posicao_inicio, pontos_entregas


def salvar_matriz(caminho="historico_matrizes_AG.txt"):
    print("Insira a matriz desejada: ")

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

    with open(caminho, "a", encoding="utf-8") as f:
        f.write("\n---\n")
        f.write("\n".join(conteudo))

    return "\n".join(conteudo)

def salvar_historico_ag(matriz_texto: str, rota, distancia_total, tempo_execucao,
                        caminho="historico_matrizes_AG.txt"):
    """
    Salva a matriz, rota ótima, distância e tempo no arquivo de histórico.
    """
    
    with open(caminho, "a", encoding="utf-8") as f:
        f.write("\n---\n")
        f.write(matriz_texto + "\n")
        f.write("Rota ótima: " + " - ".join(rota) + "\n")
        f.write(f"Distância total: {distancia_total}\n")
        f.write(f"Tempo de execução: {tempo_execucao:.6f} segundos\n")



def ler_ultima_matriz_arquivo(caminho="historico_matrizes_AG.txt") -> str:
    if not os.path.exists(caminho):
        raise FileNotFoundError("Nenhuma matriz salva ainda!")

    with open(caminho, "r", encoding="utf-8") as f:
        conteudo = f.read().strip()

    blocos = [b.strip() for b in conteudo.split("---") if b.strip()]
    return blocos[-1]



def matriz_para_texto(matriz: List[List[str]]) -> str:
    return f"{len(matriz)} {len(matriz[0])}\n" + "\n".join(" ".join(linha) for linha in matriz)


def ler_matriz_texto(entrada_texto: str) -> Tuple[List[List[str]], Tuple[int, int], Dict[str, Tuple[int, int]]]:
    linhas = entrada_texto.strip().split("\n")
    l, c = map(int, linhas[0].split())

    matriz = [linha.split() for linha in linhas[1:]]

    pontos_entregas = {}
    posicao_inicio = None

    for i in range(l):
        for j in range(c):
            valor = matriz[i][j]
            if valor == 'R':
                posicao_inicio = (i, j)
            elif valor != '0':
                pontos_entregas[valor] = (i, j)

    if posicao_inicio is None:
        raise ValueError("Ponto 'R' não encontrado.")

    return matriz, posicao_inicio, pontos_entregas


def avaliacao(individuo: List[str], inicio: Tuple[int, int], pontos: Dict[str, Tuple[int, int]]) -> float:
    custo_total = 0
    atual = inicio

    for p in individuo:
        custo_total += manhattan(atual, pontos[p])
        atual = pontos[p]

    custo_total += manhattan(atual, inicio)
    return -custo_total



def selecao(populacao: List[List[str]], pontuacoes: List[float]) -> List[List[str]]:
    selecionados = []
    for _ in range(len(populacao)):
        concorrentes = random.sample(list(zip(populacao, pontuacoes)), 2)
        vencedor = max(concorrentes, key=lambda x: x[1])[0]
        selecionados.append(vencedor.copy())
    return selecionados



def crossover_order(pai1: List[str], pai2: List[str]) -> List[str]:
    tamanho = len(pai1)
    a, b = sorted(random.sample(range(tamanho), 2))

    conjunto_fixo = set(pai1[a:b+1])
    filho = [None] * tamanho
    filho[a:b+1] = pai1[a:b+1]

    restante = [p for p in pai2 if p not in conjunto_fixo]
    idx = 0

    for i in range(tamanho):
        if filho[i] is None:
            filho[i] = restante[idx]
            idx += 1

    return filho



def crossover_pmx(pai1: List[str], pai2: List[str]) -> List[str]:
    tamanho = len(pai1)
    a, b = sorted(random.sample(range(tamanho), 2))
    filho = [None] * tamanho
    filho[a:b+1] = pai1[a:b+1]

    mapeamento = {pai1[i]: pai2[i] for i in range(a, b+1)}

    for i in list(range(0, a)) + list(range(b+1, tamanho)):
        candidato = pai2[i]
        while candidato in filho:
            candidato = mapeamento.get(candidato, candidato)
        filho[i] = candidato

    return filho


def mutar(individuo: List[str], taxa_mutacao: float) -> None:
    if random.random() < taxa_mutacao:
        i, j = random.sample(range(len(individuo)), 2)
        individuo[i], individuo[j] = individuo[j], individuo[i]



def executar_ag(matriz_txt: str, tamanho_populacao: int, numero_geracoes: int, elitismo: bool, taxa_mutacao: float, metodo_crossover: str):
    matriz, inicio, pontos_entregas = ler_matriz_texto(matriz_txt)

    rotulos = list(pontos_entregas.keys())
    populacao = [random.sample(rotulos, len(rotulos)) for _ in range(tamanho_populacao)]
    melhores_distancias = []

    for _ in range(numero_geracoes):
        pontuacoes = [avaliacao(ind, inicio, pontos_entregas) for ind in populacao]
        nova_geracao = []

        if elitismo:
            melhor_rota = max(zip(pontuacoes, populacao), key=lambda x: x[0])[1]
            nova_geracao.append(melhor_rota.copy())

        selecionados = selecao(populacao, pontuacoes)

        for _ in range(tamanho_populacao - len(nova_geracao)):
            pai1, pai2 = random.sample(selecionados, 2)

            if metodo_crossover == 'pmx':
                filho = crossover_pmx(pai1, pai2)
            else:
                filho = crossover_order(pai1, pai2)

            mutar(filho, taxa_mutacao)
            nova_geracao.append(filho)

        populacao = nova_geracao
        melhor_pontuacao = max(pontuacoes)
        melhores_distancias.append(-melhor_pontuacao)

    melhor_rota = max(populacao, key=lambda ind: avaliacao(ind, inicio, pontos_entregas))
    return melhor_rota, inicio, pontos_entregas, matriz, melhores_distancias



def plotar_rota_ag(rota: List[str], inicio: Tuple[int, int], pontos: Dict[str, Tuple[int, int]], matriz: List[List[str]]):
    plt.figure(figsize=(8, 8))
    plt.title("Rota Encontrada")

    for r in range(len(matriz)):
        for c in range(len(matriz[0])):
            plt.scatter(c, -r, color='lightgray')
            valor = matriz[r][c]
            if valor != '0':
                plt.text(c, -r, valor, fontsize=8, ha='center', va='center')

    caminho = [inicio] + [pontos[p] for p in rota] + [inicio]

    for i in range(len(caminho) - 1):
        p0 = caminho[i]
        p1 = caminho[i + 1]

        x0, y0 = p0[1], -p0[0]
        x1, y1 = p1[1], -p1[0]

        inter_x, inter_y = x1, y0
        plt.plot([x0, inter_x], [y0, inter_y], 'b-')
        plt.plot([inter_x, x1], [inter_y, y1], 'b-')

        dist = manhattan(p0, p1)
        plt.text((x0+x1)/2, (y0+y1)/2, f"{dist}", fontsize=8)

    plt.scatter(inicio[1], -inicio[0], c='red')
    plt.grid(True)
    plt.axis('equal')
    plt.show()




if __name__ == "__main__":
    caminho_arquivo = "historico_matrizes_AG.txt"

    print("\033[1;34m----- Flyfood Project-----\033[m")
    print("1 - Digitar nova matriz e salvar")
    print("2 - Usar última matriz salva")
    escolha = input("\nEscolha: ").strip()

    if escolha == "1":
        matriz_exemplo = salvar_matriz(caminho_arquivo)

    elif escolha == "2":
        try:
            matriz_exemplo = ler_ultima_matriz_arquivo(caminho_arquivo)
            print("\nMatriz carregada:")
            print(matriz_exemplo)
        except Exception as e:
            print("Erro:", e)
            exit()

    else:
        print("Opção inválida.")
        exit()

    # CONFIGURAÇÕES DO AG
    tamanho_populacao_cfg = 150
    numero_geracoes_cfg = 400
    elitismo_cfg = True
    taxa_mutacao_cfg = 0.2
    metodo_crossover_cfg = 'order'

    inicio_tempo = time.time()

    melhor, inicio, pontos_entregas, matriz, distancias = executar_ag(
        matriz_exemplo,
        tamanho_populacao_cfg,
        numero_geracoes_cfg,
        elitismo_cfg,
        taxa_mutacao_cfg,
        metodo_crossover_cfg
    )

    fim_tempo = time.time()
    tempo = fim_tempo - inicio_tempo

    dist_total = -avaliacao(melhor,inicio,pontos_entregas)

    salvar_historico_ag(
        matriz_texto=matriz_para_texto(matriz),
        rota=melhor,
        distancia_total=dist_total,
        tempo_execucao=tempo,
        caminho=caminho_arquivo
    )

    print("\nMelhor rota encontrada:", "-".join(melhor))
    print(f"Tempo de execução: {tempo:.4f} segundos")

    plotar_rota_ag(melhor, inicio, pontos_entregas, matriz)