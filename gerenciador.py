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

carregar_tarefas()
# --- MENU INTERATIVO ---
while True:
    print("\n1. Adicionar Tarefa")
    print("2. Ver Tarefas")
    print("3. Sair")
    
    opcao = input("\nEscolha uma opção: ")

    if opcao == "1":
        nome = input("Digite o nome da tarefa: ")
        adicionar_tarefa(nome)
        salvar_tarefas()
    elif opcao == "2":
        ver_tarefas()
       
    elif opcao == "3":
        print("Saindo do gerenciador... Até logo!")
        break
    else:
        print("Opção inválida! Tente novamente.")

