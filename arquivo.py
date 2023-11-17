import json
import os
import time
from win10toast import ToastNotifier
import schedule
from datetime import datetime,timedelta


pacientes = []
enfermeiros = []

EnfermeiroLogado = False

def login():
    with open('enfermeiros.json', 'r', encoding='utf-8') as arquivo:
        enfermeiros = json.load(arquivo)

    
    idenfermeiroEncontrado = False
    senhaCorreta = False

    id: str = input("Digite seu ID: ")

    for enfermeiro in enfermeiros:
        idEnfermeiro = enfermeiro['id']
        if idEnfermeiro == id:
            idenfermeiroEncontrado = True
            senha: str = input("Digite sua senha: ")
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

    cpf = str(input("Insira o CPF: "))
    pacienteCadastrado = False

    for paciente in pacientes:
        if paciente['cpf'] == cpf:
            pacienteCadastrado = True
            print(f"O paciente de cpf {paciente['cpf']} já esta cadastrado!")
            break
    if not pacienteCadastrado:
        nome = str(input("Insira o nome do paciente: "))
        idade = str(input("Insira a idade do paciente: "))

        cadastro={
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
    toaster = ToastNotifier()
    toaster.show_toast("Hora de tomar o remédio!", mensagem, duration=10 )

def agendarNotificacao(paciente):
    for medicamento in paciente.get('medicamentos', []):
        horarios = medicamento.get('horario(s)', [])
        for horario in horarios:
            schedule.every().day.at(horario).do(notificacaoPaciente,f'Hora de tomar {medicamento["medicamento"]}!')


def inserirMedicamento():
    cpf = input("Digite o CPF do paciente: ")

    with open('pacientes.json', 'r', encoding='utf-8') as arquivo:
        pacientes = json.load(arquivo)

    pacienteEncontrado = False

    for paciente in pacientes:
        if paciente['cpf'] == cpf:
            pacienteEncontrado = True
            medicamento = str(input("Insira o nome do medicamento: "))

            
            if 'medicamentos' not in paciente:
                paciente['medicamentos'] = []

           
            if any(item.get('medicamento') == medicamento for item in paciente.get('medicamentos', [])):
                print(f'O paciente já está utilizando este medicamento no momento')
            else:
                dosagem = str(input("Insira a dosagem por dia: "))
                dias = int(input("Insira o total de dias: "))

                horarios = []
                total_horarios = int(input("Total de Horários que o Paciente terá que tomar por dia: "))

                for i in range(total_horarios):
                    horario = str(input("Insira o(s) horário(s): "))
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

def mainLoop():
    while True:
        schedule.run_pending()
        time.sleep(1)

        user_input = input("Para encerrar o programa, digite 'exit' ou 'sair': ")
        if user_input.lower() in ['exit', 'sair']:
            print("Programa encerrado.")
            break


def mostrarDados():
    with open('pacientes.json', 'r', encoding='utf-8') as arquivo:
        pacientes = json.load(arquivo)

    if not pacientes:
        print("Não há pacientes cadastrados.")
        return

    for paciente in pacientes:
        print("\nDados do Paciente:")
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
    print('3 - Mostrar dados dos Pacientes')
    print('4 - Excluir Paciente')
    print('5 - Finalizar o Programa')
    try:
        opcao = int(input('Insira uma opção: '))
        if (opcao < 1) or (opcao > 5):
            raise TypeError
        return opcao
    except ValueError:
        print("Esta opção não consta no menu! Insira uma opção válida. ")



        


while EnfermeiroLogado == False:
    print("Olá! Pra inserir as informações do paciente, é preciso que esteja logado em nosso sistema!")
    loginEnfermeiro = login()
    if loginEnfermeiro == True:
        EnfermeiroLogado = True

    
if EnfermeiroLogado == True:
   while True:
        opcao = menuOpcoes()
        if opcao == 1:
            cadastro()
        elif opcao == 2:
            inserirMedicamento()
        elif opcao == 3:
            mostrarDados()
        elif opcao == 4:
            excluirPaciente()
        elif opcao == 5:
            mainLoop()
   
            





