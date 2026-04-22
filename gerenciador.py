import json 

# Nossa "base de dados" temporária (lista)
tarefas = []

def adicionar_tarefa(nome_tarefa):
    # Criamos um dicionário para representar a tarefa
    tarefa = {
        "tarefa": nome_tarefa,
        "concluida": False
    }
    # Adicionamos esse dicionário à nossa lista
    tarefas.append(tarefa)
    print(f"Tarefa '{nome_tarefa}' adicionada com sucesso!")


def ver_tarefas():
    print("\n---------- MINHAS TAREFAS ----------")
    if not tarefas:
        print("Sua lista está vazia.")
    else:
        # O enumerate nos dá o índice (número) e o item (tarefa) ao mesmo tempo
        for indice, tarefa in enumerate(tarefas, start=1):
            status = "✓" if tarefa["concluida"] else " "
            nome = tarefa["tarefa"]
            print(f"{indice}. [{status}] {nome}")
    print("------------------------------------\n")


def salvar_tarefas():
    with open("tarefas.json", "w") as arquivo:
        # Pega a nossa lista 'tarefas' e escreve dentro do arquivo .json
        json.dump(tarefas, arquivo, indent=4)
    print("Dados salvos no arquivo tarefas.json!")

def carregar_tarefas():
    global tarefas
    try:
        with open("tarefas.json", "r") as arquivo:
            tarefas = json.load(arquivo)
    except FileNotFoundError:
        # Se o arquivo não existir ainda, começamos com a lista vazia
        tarefas = []

def concluir_tarefa(indice):
    try:
        # Ajustamos o índice porque o usuário vê começando de 1, mas a lista começa de 0
        ajuste_indice = indice - 1
        if 0 <= ajuste_indice < len(tarefas):
            tarefas[ajuste_indice]["concluida"] = True
            print(f"Tarefa {indice} marcada como concluída!")
        else:
            print("Número de tarefa inválido.")
    except ValueError:
        print("Por favor, digite um número válido.")

def deletar_tarefa(indice):
    try:
        ajuste_indice = indice - 1
        if 0 <= ajuste_indice < len(tarefas):
            # O .pop remove o item e podemos guardar o nome para confirmar
            tarefa_removida = tarefas.pop(ajuste_indice)
            print(f"Tarefa '{tarefa_removida['tarefa']}' removida com sucesso!")
        else:
            print("Número de tarefa inválido.")
    except ValueError:
        print("Por favor, digite um número válido.")


carregar_tarefas()
# --- MENU INTERATIVO ---
while True:
    print("\n1. Adicionar Tarefa")
    print("2. Ver Tarefas")
    print("3. Concluir Tarefa")
    print("4. Deletar Tarefa")
    print("5. Sair")
    
    opcao = input("\nEscolha uma opção: ")

    if opcao == "1":
        nome = input("Digite o nome da tarefa: ")
        adicionar_tarefa(nome)
        salvar_tarefas()
    elif opcao == "2":
        ver_tarefas()
       
    # ... (nos seus ifs)
    elif opcao == "3":
        ver_tarefas() # Mostramos a lista para o usuário ver o número
        num = int(input("Digite o número da tarefa que deseja concluir: "))
        concluir_tarefa(num)
        salvar_tarefas() # Salva a alteração no JSON

# ... (nos seus ifs)
    elif opcao == "4":
        ver_tarefas() # Sempre bom mostrar a lista antes de deletar
        if tarefas: # Só pede o número se a lista não estiver vazia
            num = int(input("Digite o número da tarefa que deseja REMOVER: "))
            deletar_tarefa(num)
            salvar_tarefas() # Salva a remoção no JSON

     elif opcao == "5":
        print("Saindo do gerenciador... Até logo!")
        break

    else:
        print("Opção inválida! Tente novamente.")
