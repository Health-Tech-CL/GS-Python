import json

def inserirMedicamento():
    cpf = input("Digite o CPF do paciente: ")

    with open('pacientes.json', 'r', encoding='utf-8') as arquivo:
        pacientes = json.load(arquivo)

    pacienteEncontrado = False

    for paciente in pacientes:
        if paciente['cpf'] == cpf:
            medicamento = str(input("Insira o nome do medicamento: "))

            # Verifica se a chave 'medicamentos' existe no dicionário do paciente
            if 'medicamentos' not in paciente:
                paciente['medicamentos'] = []

            pacienteEncontrado = True  # Marca o paciente como encontrado

            # Verifica se o medicamento já está na lista
            if any(item.get('medicamento') == medicamento for item in paciente.get('medicamentos', [])):
                print(f'O paciente já está utilizando este medicamento no momento')
                pacienteEncontrado = False  # Desmarca o paciente se o medicamento já existe
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

                print(f'Medicamento inserido com sucesso para o paciente com CPF {cpf}')
                pacienteEncontrado = True
            break
        else:
            print("CPF não encontrado nos registros")
   

    # Sobrescreve o arquivo com os dados atualizados
    with open('pacientes.json', 'w', encoding='utf-8') as arquivo:
        json.dump(pacientes, arquivo, indent=4, ensure_ascii=False)

# Chama a função para inserir o medicamento
inserirMedicamento()