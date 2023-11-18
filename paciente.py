import json
import time
import threading
import schedule
from plyer import notification


pacientes = []

PacienteLogado = False

cpf_logado = None

def login():
    global pacientes, cpf_logado
    with open('pacientes.json', 'r', encoding='utf-8') as arquivo:
        pacientes = json.load(arquivo)

    cpfEncontrado = False

    cpf = input("Digite o seu CPF para fazer o login: ")
    time.sleep(1)

    for paciente in pacientes:
        cpfPaciente = paciente['cpf']
        if cpfPaciente == cpf:
            cpfEncontrado = True
            token = int(input("Insira seu token: "))
            time.sleep(1)
            print(f'Bem-vindo(a) {paciente["nome"]}')
            cpf_logado = cpf  # Armazenamos o CPF do paciente logado
            return True

    if not cpfEncontrado:
        print("Esse CPF não consta em nosso sistema. Tente novamente.")
        time.sleep(1)
        return False

def visualizarMedicacao():
    global pacientes, cpf_logado
    for paciente in pacientes:
        if paciente.get('cpf') == cpf_logado:  # Usamos o CPF do paciente logado
            print("\n Dados do Paciente: ")

            medicamentos = paciente.get('medicamentos', [])
            if medicamentos:
                print("\nMedicamentos:")
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
            if not medicamentos:
                print("Você não possui medicamentos registrados.")
                time.sleep(2)
                return False



    
def notificacao(mensagem):
    notification.notify(
        title="Hora de tomar o remédio!",
        message=mensagem,
        timeout=10
    )

def notificacoes_thread():
    while True:
        schedule.run_pending()
        time.sleep(1)


def menuOpcoes():
    print('O que deseja fazer?')
    print('1 - Visualizar suas medicações e horários')
    print('2 - Finalizar o Programa')

    try:
        opcao = int(input('Insira uma opção: '))
        if opcao < 1 or opcao > 2:
            raise ValueError
        return opcao
    except ValueError:
        print("Esta opção não consta no menu! Insira uma opção válida. ")
        time.sleep(1)



while PacienteLogado == False:
    print("Olá! Faça o Login para entrar em nosso sistema.")
    time.sleep(2)
    loginPaciente = login()
    if loginPaciente == True:
        PacienteLogado = True

if PacienteLogado == True:
    notificacoes_thread = threading.Thread(target=notificacoes_thread)
    notificacoes_thread.start()

    while True:
        opcao = menuOpcoes()
        if opcao == 1:
            visualizarMedicacao()
        elif opcao == 2:
            print("Finalizando o programa")
            break

    notificacoes_thread.join()