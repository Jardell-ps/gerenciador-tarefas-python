import json
import uuid # Para criar IDs únicos e universais
from datetime import datetime # Para lidar com datas
import requests
import os
from dotenv import load_dotenv

load_dotenv() # Isso carrega as variáveis do arquivo .env

# Nossa "base de dados" temporária (lista)
tarefas = []

def adicionar_tarefa(nome_tarefa, prioridade):
    tarefa = {
        "id": str(uuid.uuid4())[:8], # Cria um ID curto único
        "tarefa": nome_tarefa,
        "prioridade": prioridade,
        "concluida": False,
        "criado_em": datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    tarefas.append(tarefa)
    print(f"Tarefa '{nome_tarefa}' criada com ID: {tarefa['id']}")

def ver_tarefas():
    print("\n" + "="*80)
    print(f"{'ID':<10} | {'STATUS':<8} | {'TAREFA':<20} | {'PRIORIDADE'} | {'CRIADO EM':<8}")
    print("-" * 80)
    
    if not tarefas:
        print("Nenhuma tarefa cadastrada.")
    else:
        for tarefa in tarefas:
            # Usamos o .get() para evitar erro se a tarefa for das antigas
            tid = tarefa.get("id", "---")
            status = "✓" if tarefa.get("concluida") else " "
            nome = tarefa.get("tarefa", "Sem nome")
            prioridade = tarefa.get("prioridade", "N/A")
            criado_em = tarefa.get("criado_em", "---")
            
            print(f"{tid:<10} | [{status}]      | {nome:<20} | {prioridade} | {criado_em :<8}")
    
    print("="*80 + "\n")


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

def concluir_tarefa(id_procurado):
    for tarefa in tarefas:
        if tarefa.get("id") == id_procurado:
            tarefa["concluida"] = True
            print(f"✅ Tarefa {id_procurado} marcada como concluída!")
            
            # AQUI ENTRA A INTEGRAÇÃO!
            enviar_para_slack(tarefa['tarefa'], tarefa['prioridade'])
            
            return
    print("❌ Erro: ID não encontrado.")


def deletar_tarefa(id_procurado):
    global tarefas
    # Criamos uma nova lista SEM a tarefa que tem o ID que queremos apagar
    # Isso é muito comum em back-end (Filtragem)
    tamanho_antes = len(tarefas)
    tarefas = [t for t in tarefas if t.get("id") != id_procurado]
    
    if len(tarefas) < tamanho_antes:
        print(f"🗑️ Tarefa {id_procurado} removida com sucesso!")
    else:
        print("❌ Erro: ID não encontrado.")

def enviar_para_slack(nome_tarefa, prioridade):
    # Substitua pela sua URL real do Slack quando tiver uma
    url_webhook = os.getenv("SLACK_WEBHOOK_URL")
    
    # Vamos simplificar a mensagem para teste
    payload = {"text": f"Nova tarefa concluída: {nome_tarefa}"}
    
    headers = {'Content-type': 'application/json'}
    
    try:
        # Adicionamos o 'headers' para o Slack saber que é um JSON oficial
        response = requests.post(url_webhook, json=payload, headers=headers)
        print(f"Status do Slack: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Erro: {e}")

def enviar_relatorio_slack():
    if not tarefas:
        print("⚠️ Não há tarefas para gerar relatório.")
        return

    # Construindo o cabeçalho do relatório
    texto_relatorio = "📊 *RELATÓRIO GERAL DE TAREFAS*\n"
    texto_relatorio += "------------------------------------------\n"

    for t in tarefas:
        status = "✅" if t.get("concluida") else "⏳"
        texto_relatorio += f"{status} *{t['tarefa']}* | Prioridade: {t['prioridade']} | ID: `{t['id']}`\n"

    texto_relatorio += "------------------------------------------\n"
    texto_relatorio += f"Total de tarefas: {len(tarefas)}"

    # Reutilizando a lógica de envio que você já tem
    url_webhook = os.getenv("SLACK_WEBHOOK_URL")
    payload = {"text": texto_relatorio}
    
    try:
        response = requests.post(url_webhook, json=payload)
        if response.status_code == 200:
            print("🚀 Relatório completo enviado para o Slack!")
        else:
            print(f"⚠️ Erro ao enviar relatório: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Erro de conexão: {e}")



carregar_tarefas()
# --- MENU INTERATIVO ---
while True:
    print("\n1. Adicionar Tarefa")
    print("2. Ver Tarefas")
    print("3. Concluir Tarefa")
    print("4. Deletar Tarefa")
    print("5. Sair")
    print("6. Enviar Relatório para o Slack")
    opcao = input("\nEscolha uma opção: ")

    if opcao == "1":
        nome = input("Digite o nome da tarefa: ")
        tipo = input("Digite o tipo da prioridade: ")
        adicionar_tarefa(nome, tipo)
        salvar_tarefas()
    elif opcao == "2":
        ver_tarefas()
       
    elif opcao == "3":
        ver_tarefas()
        # Removido o int(), agora lemos como string
        id_input = input("Digite o ID da tarefa que deseja concluir: ")
        concluir_tarefa(id_input)
        salvar_tarefas()

    elif opcao == "4":
        ver_tarefas()
        if tarefas:
            id_input = input("Digite o ID da tarefa que deseja REMOVER: ")
            deletar_tarefa(id_input)
            salvar_tarefas()

    elif opcao == "5":
        print("Saindo do gerenciador... Até logo!")
        break
    
    elif opcao == "6":
        enviar_relatorio_slack()

    else:
        print("Opção inválida! Tente novamente.")
