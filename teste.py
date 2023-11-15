import json

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
    with open('pacientes.json', 'r', encoding='utf-8') as arquivo:
        pacientes = json.load(arquivo)

    cpf = float(input("Insira o CPF: "))
    pacienteCadastrado = False

    for paciente in pacientes:
        if paciente['cpf'] == cpf:
            pacienteCadastrado == True
            print(f"O paciente de cpf {paciente['cpf']} já esta cadastrado!")
        else:
            nome = str(input("Insira o nome do paciente: "))
            idade = int(input("Insira a idade do paciente: "))

            cadastro={
                "cpf": cpf,
                "nome": nome,
                "idade": idade
            }

            pacientes.append(cadastro)

            with open("pacientes.json", 'w', encoding='utf-8') as JSON:
                json.dump(pacientes, JSON, indent=4, ensure_ascii=False)
            print("Paciente Cadastrado com Sucesso!")
            return cadastro
        
def menuOpcoes():
    print('O que deseja fazer?')
    print('1 - Inserir Paciente')
    print('2 - Inserir Medicamento')
    print('3 - Mostrar dados dos Pacientes')
    print('4 - Excluir Paciente')
    print('5 - Finalizar')
    try:
        opcao = int(input('Insira uma opção: '))
        if (opcao < 1) or (opcao > 5):
            raise TypeError
        return opcao
    except TypeError:
        print("Esta opção não consta no menu! Insira uma opção válida. ")


while EnfermeiroLogado == False:
    print("Olá! Pra inserir as informações do paciente, é preciso que esteja logado em nosso sistema!")
    loginEnfermeiro = login()
    if loginEnfermeiro == True:
        EnfermeiroLogado = True

    
if EnfermeiroLogado == True:
    while True:
        opcao = menuOpcoes()

