import json
enfermeiros = []

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
        print('ID Incorreto!')
        return False
        
login()