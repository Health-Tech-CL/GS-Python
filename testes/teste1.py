import os
import json

def cadastro():
    global pacientes

    if os.path.exists('pacientes.json') and os.path.getsize('pacientes.json') > 0:
        with open('pacientes.json', 'r', encoding='utf-8') as arquivo:
            pacientes = json.load(arquivo)
    else:
        pacientes = []
    
    cpf = float(input("Insira o CPF: "))
    pacienteCadastrado = False

    for paciente in pacientes:
        if paciente['cpf'] == cpf:
            pacienteCadastrado = True
            print(f"O paciente de cpf {paciente['cpf']} já esta cadastrado!")
            break
    if not pacienteCadastrado:
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

cadastro()