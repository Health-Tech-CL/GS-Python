import json
import os
import time
from plyer import notification
import schedule
import threading

pacientes = []
enfermeiros = []
notificacoes_agendadas = []

EnfermeiroLogado = False

def login():
    with open('enfermeiros.json', 'r', encoding='utf-8') as arquivo:
        enfermeiros = json.load(arquivo)

    idenfermeiroEncontrado = False
    senhaCorreta = False

    id = input("Digite seu ID: ")

    for enfermeiro in enfermeiros:
        idEnfermeiro = enfermeiro['id']
        if idEnfermeiro == id:
            idenfermeiroEncontrado = True
            senha = input("Digite sua senha: ")
            if senha == enfermeiro['senha']:
                print(f'Bem-Vindo(a) {enfermeiro["nome"]}')
                senhaCorreta = True
                return True
            else:
                print("Senha Incorreta!")
                return False
    if not idenfermeiroEncontrado:
        print("ID Incorreto!")
        return False


def cadastro():
    global pacientes

    if os.path.exists('pacientes.json') and os.path.getsize('pacientes.json') > 0:
        with open('pacientes.json', 'r', encoding='utf-8') as arquivo:
            pacientes = json.load(arquivo)
    else:
        pacientes = []

    cpf = input("Insira o CPF: ")
    pacienteCadastrado = False

    for paciente in pacientes:
        if paciente['cpf'] == cpf:
            pacienteCadastrado = True
            print(f"O paciente de cpf {paciente['cpf']} já está cadastrado!")
            break
    if not pacienteCadastrado:
        nome = input("Insira o nome do paciente: ")
        idade = input("Insira a idade do paciente: ")

        cadastro = {
            "cpf": cpf,
            "nome": nome,
            "idade": idade,
        }

        pacientes.append(cadastro)

        with open("pacientes.json", 'w', encoding='utf-8') as JSON:
            json.dump(pacientes, JSON, indent=4, ensure_ascii=False)
        print("Paciente Cadastrado com Sucesso!")
    return cadastro




def notificacaoPaciente(mensagem):
    notification.notify(
        title="Hora de tomar o remédio!",
        message=mensagem,
        timeout=10
    )


def agendarNotificacao(paciente):
    for medicamento in paciente.get('medicamentos', []):
        horarios = medicamento.get('horario(s)', [])
        for horario in horarios:
            print(f'Agendando notificação para {horario}')
            schedule.every().day.at(horario).do(notificacaoPaciente, f'Hora de tomar {medicamento["medicamento"]}!')

def notificacoes_thread():
    while True:
        schedule.run_pending()
        time.sleep(1)



def inserirMedicamento():
    cpf = input("Digite o CPF do paciente: ")

    with open('pacientes.json', 'r', encoding='utf-8') as arquivo:
        pacientes = json.load(arquivo)

    pacienteEncontrado = False

    for paciente in pacientes:
        if paciente['cpf'] == cpf:
            pacienteEncontrado = True
            medicamento = input("Insira o nome do medicamento: ")
            if 'medicamentos' not in paciente:
                paciente['medicamentos'] = []

            if any(item.get('medicamento') == medicamento for item in paciente.get('medicamentos', [])):
                print(f'O paciente já está utilizando este medicamento no momento')
            else:
                dosagem = input("Insira a dosagem por dia: ")
                dias = int(input("Insira o total de dias: "))

                horarios = []
                total_horarios = int(input("Total de Horários que o Paciente terá que tomar por dia: "))

                for i in range(total_horarios):
                    horario = input("Insira o(s) horário(s): ")
                    horarios.append(horario)

                novo_medicamento = {
                    'medicamento': medicamento,
                    'dosagem': dosagem,
                    'quantos dias': dias,
                    'horario(s)': horarios
                }

                paciente['medicamentos'].append(novo_medicamento)

                agendarNotificacao(paciente)

                print(f'Medicamento inserido com sucesso para o paciente com CPF {cpf}')

    if not pacienteEncontrado:
        print(f"Paciente com o CPF {cpf} não encontrado no registro")

    with open('pacientes.json', 'w', encoding='utf-8') as arquivo:
        json.dump(pacientes, arquivo, indent=4, ensure_ascii=False)



def mostrarDados():
    with open('pacientes.json', 'r', encoding='utf-8') as arquivo:
        pacientes = json.load(arquivo)

    if not pacientes:
        print("Não há pacientes cadastrados.")
        return

    for paciente in pacientes:
        print("\n Dados do Paciente:")
        print(f"CPF: {paciente['cpf']}")
        print(f"Nome: {paciente.get('nome', 'N/A')}")
        print(f"Idade: {paciente.get('idade', 'N/A')}")

        medicamentos = paciente.get('medicamentos', [])
        if medicamentos:
            print("\nMedicamentos:")
            for med in medicamentos:
                print(f"  Medicamento: {med.get('medicamento', 'N/A')}")
                print(f"  Dosagem: {med.get('dosagem', 'N/A')}")
                print(f"  Quantos dias: {med.get('quantos dias', 'N/A')}")
                horarios = ', '.join(med.get('horario(s)', []))
                print(f"  Horário(s): {horarios}")
                print("\n---")

    print("\nFim da lista de pacientes.")
    time.sleep(2)

def editarDados():
    cpf = input("Insira o cpf do paciente que deseja editar os dados: ")

    with open('pacientes.json', 'r', encoding='utf-8') as arquivo:
        pacientes = json.load(arquivo)

    pacienteEncontrado = False

    for paciente in pacientes:
        if paciente['cpf'] == cpf:
            pacienteEncontrado = True

            print(f"Editando as Informações do Paciente com CPF {cpf}")
            print("1 - Editar Nome")
            print("2 - Editar Idade")

            opcao = int(input("Insira a opção desejada: "))

            if opcao == 1:
                novo_nome = input("Insira o novo nome: ")
                paciente['nome'] = novo_nome
                print("Nome alterado com sucesso!")
            
            elif opcao == 2:
                nova_idade = input("Insira a idade nova: ")
                paciente['idade'] = nova_idade
                print("Idade alterada com sucesso!")
            
            else:
                print("Opção Inválida")
                
            break


def excluirMedicamento():
    cpf = input("Insira o CPF do paciente que deseja excluir o Medicamento: ")

    with open('pacientes.json', 'r', encoding='utf-8') as arquivo:
        pacientes = json.load(arquivo)
    
    pacienteEncontrado = False

    for paciente in pacientes:
        if paciente['cpf'] == cpf:
            pacienteEncontrado = True
            medicamentos = paciente.get('medicamentos', [])

            if not medicamentos:
                print(f'O paciente com cpf {cpf} não possui medicamentos registrados')
                return
            
            print("Medicamentos do Paciente: ")
            for i, med in enumerate(medicamentos, start=1):
                print(f'{i}. {med.get("medicamento")}')

            medicamento_nome = input("Insira o nome do remédio que deseja excluir: ")
            medicamento_encontrado = False

            for med in medicamentos:
                if med.get('medicamento') == medicamento_nome:
                    medicamento_encontrado = True
                    medicamentos.remove(med)

                    for job, mensagem in notificacoes_agendadas:
                        if mensagem == f'Hora de tomar {medicamento_nome}!':
                            job.unschedule()
                            notificacoes_agendadas.remove((job, mensagem))
                            break

                    time.sleep(2)
                    print(f'Medicamento {medicamento_nome} removido com sucesso para o paciente com CPF {cpf}')
                    break

            if not medicamento_encontrado:
                print(f"Medicamento {medicamento_nome} não encontrado para o paciente com CPF {cpf}")

            break

    if not pacienteEncontrado:
        print(f"Paciente com o CPF {cpf} não encontrado no registro")

    with open('pacientes.json', 'w', encoding='utf-8') as arquivo:
        json.dump(pacientes, arquivo, indent=4, ensure_ascii=False)




def excluirPaciente():
    cpf = input("Digite o CPF do paciente que deseja excluir: ")

    with open('pacientes.json', 'r', encoding='utf-8') as arquivo:
        pacientes = json.load(arquivo)

    pacienteEncontrado = False

    for paciente in pacientes:
        if paciente['cpf'] == cpf:
            pacienteEncontrado = True
            pacientes.remove(paciente)
            time.sleep(2)
            print(f'Paciente com CPF {cpf} excluído com sucesso.')
            break

    if not pacienteEncontrado:
        print(f"Paciente com o CPF {cpf} não encontrado no registro.")

    with open('pacientes.json', 'w', encoding='utf-8') as arquivo:
        json.dump(pacientes, arquivo, indent=4, ensure_ascii=False)


def menuOpcoes():
    print('O que deseja fazer?')
    print('1 - Cadastrar Paciente')
    print('2 - Inserir Medicamento')
    print('3 - Excluir Medicamento')
    print('4 - Mostrar dados dos Pacientes')
    print('5- Editar Dados dos Pacientes')
    print('6 - Excluir Paciente')
    print('7 - Finalizar o Programa')
    try:
        opcao = int(input('Insira uma opção: '))
        if (opcao < 1) or (opcao > 7):
            raise TypeError
        return opcao
    except ValueError:
        print("Esta opção não consta no menu! Insira uma opção válida. ")



while EnfermeiroLogado == False:
    print("Olá! Para inserir as informações do paciente, é preciso que esteja logado em nosso sistema!")
    loginEnfermeiro = login()
    if loginEnfermeiro == True:
        EnfermeiroLogado = True

if EnfermeiroLogado == True:
    # Inicie a thread para processar notificações
    notificacoes_thread = threading.Thread(target=notificacoes_thread)
    notificacoes_thread.start()

    while True:
        opcao = menuOpcoes()
        if opcao == 1:
            cadastro()
        elif opcao == 2:
            inserirMedicamento()
        elif opcao == 3:
            excluirMedicamento()
        elif opcao == 4:
            mostrarDados()
        elif opcao == 5:
            editarDados()
        elif opcao == 6:
           excluirPaciente()
        elif opcao == 7:
            print("Finalizando o programa")
            break


    # Aguarde até que a thread de notificações seja concluída antes de encerrar o programa
    notificacoes_thread.join()


