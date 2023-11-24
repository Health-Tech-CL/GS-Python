# Importações necessárias para o funcionamento do sistema
import json
import os
import time
from plyer import notification
import schedule
import threading
import random
import time
from paho.mqtt import client as mqtt_client

broker = '46.17.108.113'
port = 1883
topic = "/TEF/hosp230/cmd"
client_id = f'publish-{random.randint(0, 1000)}'

# Leia o README antes de rodar o código, pois há informações importantes!!!!!!



# Aqui são as listas que criamos para deixar as informações no banco de dados organizadas
pacientes = []
enfermeiros = []
notificacoes_agendadas = []


EnfermeiroLogado = False



# Função pra enfermeira completar o Login pra ter acesso ao menu de opções
def login():
    with open('enfermeiros.json', 'r', encoding='utf-8') as arquivo:
        enfermeiros = json.load(arquivo)

    idenfermeiroEncontrado = False
    senhaCorreta = False

    id = input("Digite seu ID: ")
    time.sleep(1)
    for enfermeiro in enfermeiros:
        idEnfermeiro = enfermeiro['id']
        if idEnfermeiro == id:
            idenfermeiroEncontrado = True
            senha = input("Digite sua senha: ")
            time.sleep(1)
            if senha == enfermeiro['senha']:
                print(f'Bem-Vindo(a), {enfermeiro["nome"]}!')
                time.sleep(2)
                senhaCorreta = True
                return True
            else:
                print("Senha Incorreta!")
                time.sleep(1)
                return False
    if not idenfermeiroEncontrado:
        print("ID Incorreto!")
        time.sleep(1)
        return False

# Aqui é a função de cadastrar o paciente, onde coloca seu cpf, nome e idade
def cadastro():
    global pacientes

    if os.path.exists('pacientes.json') and os.path.getsize('pacientes.json') > 0:
        with open('pacientes.json', 'r', encoding='utf-8') as arquivo:
            pacientes = json.load(arquivo)
    else:
        pacientes = []

    cpf = input("Insira o CPF: ")
    time.sleep(1)
    pacienteCadastrado = False

    for paciente in pacientes:
        if paciente['cpf'] == cpf:
            pacienteCadastrado = True
            print(f"O paciente de cpf {paciente['cpf']} já está cadastrado!")
            time.sleep(1)
            break
    if not pacienteCadastrado:
        nome = input("Insira o nome do paciente: ")
        time.sleep(1)
        idade = input("Insira a idade do paciente: ")
        time.sleep(1)

        cadastro = {
            "cpf": cpf,
            "nome": nome,
            "idade": idade,
        }

        pacientes.append(cadastro)

        with open("pacientes.json", 'w', encoding='utf-8') as JSON:
            json.dump(pacientes, JSON, indent=4, ensure_ascii=False)
        print("Paciente Cadastrado com Sucesso!")
        time.sleep(2)
    return cadastro



# Função que programa o corpo da notificação
def notificacaoPaciente(mensagem):
    notification.notify(
        title="Hora de tomar o remédio!",
        message=mensagem,
        timeout=10
    )
        
        


# Aqui fazemos o agendamento da notificação assim que o enfermeiro(a) adiciona um medicamento pro paciente
def agendarNotificacao(paciente):
    mensagemAgendada = False
    for medicamento in paciente.get('medicamentos', []):
        horarios = medicamento.get('horario(s)', [])
        for horario in horarios:
            print(f'Agendando notificação para {horario}')
            schedule.every().day.at(horario).do(notificacaoPaciente, f'Hora de tomar {medicamento["medicamento"]}, {paciente["nome"]}!')
            mensagemAgendada = True

# Função pra garantir que a notificação continue rodando em um laço de repetição
def notificacoes_thread():
    while True:
        schedule.run_pending()
        time.sleep(1)


# Aqui é onde o enfermeiro(a) adiciona o medicamento pro paciente desejado
def inserirMedicamento(client):
    global paciente_atual
    cpf = input("Digite o CPF do paciente: ")
    time.sleep(1)

    with open('pacientes.json', 'r', encoding='utf-8') as arquivo:
        pacientes = json.load(arquivo)

    pacienteEncontrado = False

    for paciente in pacientes:
        if paciente['cpf'] == cpf:
            pacienteEncontrado = True
            medicamento = input("Insira o nome do medicamento: ")
            time.sleep(1)
            if 'medicamentos' not in paciente:
                paciente['medicamentos'] = []

            if any(item.get('medicamento') == medicamento for item in paciente.get('medicamentos', [])):
                print(f'O paciente já está utilizando este medicamento no momento')
                time.sleep(1)
            else:
                dosagem = input("Insira a dosagem: ")
                time.sleep(1)
                dias = int(input("Insira o total de dias: "))
                time.sleep(1)

                horarios = []
                total_horarios = int(input("Total de Horários que o Paciente terá que tomar por dia: "))
                time.sleep(1)

                for i in range(total_horarios):
                    horario = input("Insira o(s) horário(s): ")
                    time.sleep(1)
                    horarios.append(horario)

                novo_medicamento = {
                    'medicamento': medicamento,
                    'dosagem': dosagem,
                    'quantos dias': dias,
                    'horario(s)': horarios
                }

                paciente['medicamentos'].append(novo_medicamento)

                agendarNotificacao(paciente)      # Assim que o novo medicamento é adicionado, o agendamento automaticamente liga

                paciente_atual = paciente

                print(f'Medicamento inserido com sucesso para o paciente com CPF {cpf}')
                time.sleep(2)

                msg = f"Hora de tomar o remédio {paciente_atual['nome']}!"
                #msg = f"On"
                result = client.publish(topic, msg)
                status = result.rc
                if status == 0:
                    print(f"Send `{msg}` to topic `{topic}` via MQTT")
                else:
                    print(f"Failed to send message to topic {topic} via MQTT")

            

    if not pacienteEncontrado:
        print(f"Paciente com o CPF {cpf} não encontrado no registro")
        time.sleep(1)

    with open('pacientes.json', 'w', encoding='utf-8') as arquivo:
        json.dump(pacientes, arquivo, indent=4, ensure_ascii=False)




# Aqui é pra quando o enfermeiro deseja ver os pacientes cadastrados
def mostrarDados():
    with open('pacientes.json', 'r', encoding='utf-8') as arquivo:
        pacientes = json.load(arquivo)

    if not pacientes:
        print("Não há pacientes cadastrados.")
        time.sleep(1)
        return

    for paciente in pacientes:
        print("\n Dados do Paciente:")
        print(f"CPF: {paciente['cpf']}")
        time.sleep(1)
        print(f"Nome: {paciente.get('nome', 'N/A')}")
        time.sleep(1)
        print(f"Idade: {paciente.get('idade', 'N/A')}")
        time.sleep(1)

        medicamentos = paciente.get('medicamentos', [])
        if medicamentos:
            print("\nMedicamentos:")
            time.sleep(1)
            for med in medicamentos:
                print(f"  Medicamento: {med.get('medicamento', 'N/A')}")
                time.sleep(1)
                print(f"  Dosagem: {med.get('dosagem', 'N/A')}")
                time.sleep(1)
                print(f"  Quantos dias: {med.get('quantos dias', 'N/A')}")
                time.sleep(1)
                horarios = ', '.join(med.get('horario(s)', []))
                print(f"  Horário(s): {horarios}")
                time.sleep(1)
                print("\n---")
                time.sleep(1)

    print("\nFim da lista de pacientes.\n")
    time.sleep(2)


# Aqui o enfermeiro(a) consegue editar os dados do cadastro inicial caso tenham sido digitados errado
def editarDados():
    cpf = input("Insira o cpf do paciente que deseja editar os dados: ")
    time.sleep(1)

    with open('pacientes.json', 'r', encoding='utf-8') as arquivo:
        pacientes = json.load(arquivo)

    pacienteEncontrado = False

    for paciente in pacientes:
        if paciente['cpf'] == cpf:
            pacienteEncontrado = True

            print(f"Editando as Informações do Paciente com CPF {cpf}")
            time.sleep(1)
            print("1 - Editar Nome")
            print("2 - Editar Idade")

            opcao = int(input("Insira a opção desejada: "))
            time.sleep(1)

            if opcao == 1:
                novo_nome = input("Insira o novo nome: ")
                time.sleep(1)
                paciente['nome'] = novo_nome
                print("Nome alterado com sucesso!")
                time.sleep(2)
            
            elif opcao == 2:
                nova_idade = input("Insira a idade nova: ")
                time.sleep(1)
                paciente['idade'] = nova_idade
                print("Idade alterada com sucesso!")
                time.sleep(2)
            
            else:
                print("Opção Inválida")
                time.sleep(1)

            with open('pacientes.json', 'w', encoding='utf-8') as arquivo_saida:
                json.dump(pacientes, arquivo_saida, indent=4, ensure_ascii=False)
                
            break


# Essa função exclui um medicamento específico 
def excluirMedicamento():
    cpf = input("Insira o CPF do paciente que deseja excluir o Medicamento: ")
    time.sleep(1)

    with open('pacientes.json', 'r', encoding='utf-8') as arquivo:
        pacientes = json.load(arquivo)
    
    pacienteEncontrado = False

    for paciente in pacientes:
        if paciente['cpf'] == cpf:
            pacienteEncontrado = True
            medicamentos = paciente.get('medicamentos', [])

            if not medicamentos:
                print(f'O paciente com cpf {cpf} não possui medicamentos registrados')
                time.sleep(1)
                return
            
            print("Medicamentos do Paciente: ")
            time.sleep(1)
            for i, med in enumerate(medicamentos, start=1):
                print(f'{i}. {med.get("medicamento")}')

            medicamento_nome = input("Insira o nome do remédio que deseja excluir: ")
            formatacaoNome = medicamento_nome.capitalize()
            time.sleep(1)
            medicamento_encontrado = False

            for med in medicamentos:
                if med.get('medicamento') == formatacaoNome:
                    medicamento_encontrado = True
                    medicamentos.remove(med)

                    for job, mensagem in notificacoes_agendadas:
                        if mensagem == f'Hora de tomar {medicamento_nome}!':
                            job.unschedule()
                            notificacoes_agendadas.remove((job, mensagem))
                            break

                    time.sleep(2)
                    print(f'Medicamento {medicamento_nome} removido com sucesso para o paciente com CPF {cpf}')
                    time.sleep(2)
                    break

            if not medicamento_encontrado:
                print(f"Medicamento {medicamento_nome} não encontrado para o paciente com CPF {cpf}")
                time.sleep(1)

            break

    if not pacienteEncontrado:
        print(f"Paciente com o CPF {cpf} não encontrado no registro")
        time.sleep(1)

    with open('pacientes.json', 'w', encoding='utf-8') as arquivo:
        json.dump(pacientes, arquivo, indent=4, ensure_ascii=False)



# Aqui você exclui um paciente específico do banco de dados
def excluirPaciente():
    cpf = input("Digite o CPF do paciente que deseja excluir: ")
    time.sleep(1)

    with open('pacientes.json', 'r', encoding='utf-8') as arquivo:
        pacientes = json.load(arquivo)

    pacienteEncontrado = False

    for paciente in pacientes:
        if paciente['cpf'] == cpf:
            pacienteEncontrado = True
            pacientes.remove(paciente)
            time.sleep(2)
            print(f'Paciente com CPF {cpf} excluído com sucesso.')
            time.sleep(1)
            break

    if not pacienteEncontrado:
        print(f"Paciente com o CPF {cpf} não encontrado no registro.")
        time.sleep(1)

    with open('pacientes.json', 'w', encoding='utf-8') as arquivo:
        json.dump(pacientes, arquivo, indent=4, ensure_ascii=False)

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client):
    msg_count = 1
    while True:
        time.sleep(1)
        msg = f"On"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1
        if msg_count > 5:
            break

def run(client):
    client.loop_start()
    publish(client)
    client.loop_stop()



# Aqui é o menu de opções
def menuOpcoes():
    print('O que deseja fazer?')
    print('1 - Cadastrar Paciente')
    print('2 - Inserir Medicamento')
    print('3 - Excluir Medicamento')
    print('4 - Mostrar dados dos Pacientes')
    print('5-  Editar Dados dos Pacientes')
    print('6 - Excluir Paciente')
    print('7 - Finalizar o Programa')
    try:
        opcao = int(input('Insira uma opção: '))
        time.sleep(1)
        if (opcao < 1) or (opcao > 7):
            raise TypeError
        return opcao
    except ValueError:
        print("Esta opção não consta no menu! Insira uma opção válida. ")
        time.sleep(1)


# Aqui é o laço de repetição pra garantir que, se o enfermeiro nao estiver logado, o sistema não irá iniciar
while EnfermeiroLogado == False:
    print("Olá! Para inserir as informações do paciente, é preciso que esteja logado em nosso sistema!")
    time.sleep(1)
    loginEnfermeiro = login()
    if loginEnfermeiro == True:
        EnfermeiroLogado = True


# Já aqui é quando o enfermeiro está logado e tem acesso a todas as funções do sistema, incluindo o menu de opções
if EnfermeiroLogado == True:
    # Iniciando a thread para processar as notificações
    notificacoes_thread = threading.Thread(target=notificacoes_thread)
    notificacoes_thread.start()
    
    client = connect_mqtt()

    while True:
        opcao = menuOpcoes()
        if opcao == 1:
            time.sleep(1)
            cadastro()
        elif opcao == 2:
            time.sleep(1)
            inserirMedicamento(client)
        elif opcao == 3:
            time.sleep(1)
            excluirMedicamento()
        elif opcao == 4:
            time.sleep(1)
            mostrarDados()
        elif opcao == 5:
            time.sleep(1)
            editarDados()
        elif opcao == 6:
           time.sleep(1)
           excluirPaciente()
        elif opcao == 7:
            time.sleep(1)
            print("Finalizando o programa")
            break


    # Para aguardar até que a thread de notificações esteja concluída antes de encerrar o programa
    notificacoes_thread.join()



