import random

def calcular_doomsday_21st_century(ano_completo):
    # Pega apenas os dois últimos dígitos do ano
    ano = ano_completo % 100
    
    # --- A Regra do Par e Ímpar ---
    # 1. Se for ímpar, soma 11
    if ano % 2 != 0:
        ano += 11
        
    # 2. Divide por 2
    ano = ano // 2
    
    # 3. Se for ímpar, soma 11 novamente
    if ano % 2 != 0:
        ano += 11
        
    # 4. Módulo 7
    resto = ano % 7
    
    # 5. Subtrai de 7 e ajusta para a âncora do século XXI (Terça-feira = 2 na contagem antiga)
    # Na contagem antiga: 0=Dom, 1=Seg, 2=Ter...
    doomsday_antigo = (7 - resto + 2) % 7
    
    # --- Conversão para a nova escala (1=Domingo, 2=Segunda ... 7=Sábado) ---
    # Se der 0 (Domingo), vira 1. Se der 1 (Segunda), vira 2... Se der 6 (Sábado), vira 7.
    if doomsday_antigo == 0:
        doomsday_novo = 1
    else:
        doomsday_novo = doomsday_antigo + 1
        
    return doomsday_novo

def jogar_quiz():
    # Nova escala conforme solicitado: Domingo = 1 até Sábado = 7
    dias_semana = {
        1: "Domingo",
        2: "Segunda-feira",
        3: "Terça-feira",
        4: "Quarta-feira",
        5: "Quinta-feira",
        6: "Sexta-feira",
        7: "Sábado"
    }
    
    print("=" * 55)
    print("🧠 QUIZ DOOMSDAY: ESCALA 1 A 7 (SÉCULO XXI) 🧠")
    print("=" * 55)
    print("Descubra o Dia do Juízo Final (Doomsday) do ano exibido.")
    print("Digite o número correspondente ao dia da semana:")
    for num, dia in dias_semana.items():
        print(f" [{num}] {dia}")
    print("-" * 55)
    
    pontos = 0
    jogar = True
    
    while jogar:
        # Sorteia um ano de 2000 até 2099
        ano_sorteado = random.randint(2000, 2099)
        resposta_correta_num = calcular_doomsday_21st_century(ano_sorteado)
        
        print(f"\nQual é o Doomsday do ano: ➡️  {ano_sorteado}  ⬅️?")
        
        while True:
            entrada = input("Sua resposta (1-7) ou 'sair': ").strip().lower()
            if entrada == 'sair':
                jogar = False
                break
            
            if entrada.isdigit() and int(entrada) in range(1, 8):
                resposta_usuario = int(entrada)
                break
            else:
                print("Por favor, digite um número válido entre 1 e 7.")
                
        if not jogar:
            break
            
        if resposta_usuario == resposta_correta_num:
            print(f"🥳 CORRETO! O Doomsday de {ano_sorteado} é {dias_semana[resposta_correta_num]}.")
            pontos += 1
        else:
            print(f"❌ ERROU! O correto era {dias_semana[resposta_correta_num]} (Número {resposta_correta_num}).")
            
            # Dica rápida de treino
            ultimos_digitos = ano_sorteado % 100
            if ultimos_digitos % 2 != 0:
                print(f"   [Treino {ultimos_digitos}]: Ímpar -> +11 = {ultimos_digitos+11} -> metade = {(ultimos_digitos+11)//2}...")
            else:
                print(f"   [Treino {ultimos_digitos}]: Par -> metade = {ultimos_digitos//2}...")

    print("-" * 55)
    print(f"Jogo terminado! Você fez {pontos} ponto(s).")

if __name__ == "__main__":
    jogar_quiz()
