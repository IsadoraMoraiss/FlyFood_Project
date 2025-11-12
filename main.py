from força_bruta import salvar_matriz, ler_matriz, calcular_distancia, calcular_rota_otima
import time 

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
    tempo_execucao = fim - inicio
    

    if rota:
        print("\nrota ótima:", ' '.join(rota))
        print("Distância Dronômetros:", distancia)
        print(f"Tempo de execução: {tempo_execucao:.6f} segundos")
        # Salva não só as matrizes colocadas como também a melhor rota, distância e tempo que levou para calcular 
        with open(Matrizes, "a", encoding="utf-8") as f:
            f.write(f"\n  \n")
            f.write(f"Rota ótima: {' → '.join(rota)}\n")
            f.write(f"Distância mínima: {distancia}\n")
            f.write(f"Tempo de execução: {tempo_execucao:.6f} segundos\n")
    else:
        print("\nNenhuma rota encontrada.")
    


if __name__ == "__main__":
    main()