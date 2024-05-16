from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer

def criar_e_treinar_chatbot():
    # Criação do chatbot
    study_assistant = ChatBot(
        'Assistente de Estudos',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        database_uri='sqlite:///database.sqlite3',
        logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch',
                'default_response': 'Desculpe, eu não entendi. Você pode reformular a pergunta?',
                'maximum_similarity_threshold': 0.90
            }
        ]
    )

    # Treinamento com o corpus padrão em português
    corpus_trainer = ChatterBotCorpusTrainer(study_assistant)
    corpus_trainer.train("chatterbot.corpus.portuguese")

    # Treinamento com dados específicos
    list_trainer = ListTrainer(study_assistant)

    # Treinamento sobre Matemática
    list_trainer.train([
        "O que é uma função matemática?",
        "Uma função matemática é uma relação entre um conjunto de entradas e um conjunto de possíveis saídas onde cada entrada está relacionada a exatamente uma saída.",

        "Qual é a fórmula da área de um círculo?",
        "A fórmula da área de um círculo é A = πr^2, onde 'A' é a área e 'r' é o raio."
    ])

    # Treinamento sobre História
    list_trainer.train([
        "Quem foi Dom Pedro I?",
        "Dom Pedro I foi o fundador e primeiro imperador do Brasil.",

        "O que foi a Revolução Francesa?",
        "A Revolução Francesa foi um período de mudanças sociais e políticas radicais na França que durou de 1789 a 1799."
    ])

    # Treinamento sobre Geografia
    list_trainer.train([
        "Qual é o maior deserto do mundo?",
        "O maior deserto do mundo é o Deserto do Saara, localizado no norte da África.",

        "O que é a linha do Equador?",
        "A linha do Equador é uma linha imaginária ao redor do meio da Terra, equidistante dos pólos norte e sul."
    ])

    print("Treinamento concluído!")
    return study_assistant

def escolher_disciplina():
    disciplinas = {
        "1": "Matemática",
        "2": "História",
        "3": "Geografia"
    }

    print("Escolha uma disciplina (ou digite 'sair' para encerrar):")
    for key, value in disciplinas.items():
        print(f"{key} - {value}")

    escolha = input("Digite o número da disciplina: ")

    if escolha.lower() == "sair":
        return "sair"

    return disciplinas.get(escolha, "Disciplina não encontrada")

def interagir_com_chatbot(chatbot):
    while True:
        disciplina = escolher_disciplina()
        if disciplina == "sair":
            print("Até mais! Bons estudos!")
            break

        if disciplina == "Disciplina não encontrada":
            print(disciplina)
            continue

        print(f"Você escolheu {disciplina}. Faça sua pergunta (ou digite 'sair' para encerrar).")

        while True:
            try:
                user_input = input("Você: ")
                if user_input.lower() == "sair":
                    print("Até mais! Bons estudos!")
                    return
                response = chatbot.get_response(user_input)
                print(f"Assistente de Estudos ({disciplina}): ", response)
            except (KeyboardInterrupt, EOFError, SystemExit):
                print("Até mais! Bons estudos!")
                return

def testar_precisao(chatbot):
    # Definir perguntas e respostas esperadas
    testes = {
        "O que é uma função matemática?": "Uma função matemática é uma relação entre um conjunto de entradas e um conjunto de possíveis saídas onde cada entrada está relacionada a exatamente uma saída.",
        "Qual é a fórmula da área de um círculo?": "A fórmula da área de um círculo é A = πr^2, onde 'A' é a área e 'r' é o raio.",
        "Quem foi Dom Pedro I?": "Dom Pedro I foi o fundador e primeiro imperador do Brasil.",
        "O que foi a Revolução Francesa?": "A Revolução Francesa foi um período de mudanças sociais e políticas radicais na França que durou de 1789 a 1799.",
        "Qual é o maior deserto do mundo?": "O maior deserto do mundo é o Deserto do Saara, localizado no norte da África.",
        "O que é a linha do Equador?": "A linha do Equador é uma linha imaginária ao redor do meio da Terra, equidistante dos pólos norte e sul."
    }

    acertos = 0
    total_testes = len(testes)

    for pergunta, resposta_esperada in testes.items():
        resposta_do_chatbot = chatbot.get_response(pergunta).text
        print(f"Pergunta: {pergunta}")
        print(f"Resposta esperada: {resposta_esperada}")
        print(f"Resposta do chatbot: {resposta_do_chatbot}")
        print()

        if resposta_do_chatbot.lower() == resposta_esperada.lower():
            acertos += 1

    precisao = (acertos / total_testes) * 100
    print(f"Precisão do chatbot: {precisao:.2f}%")

if __name__ == "__main__":
    chatbot = criar_e_treinar_chatbot()
    interagir_com_chatbot(chatbot)
    testar_precisao(chatbot)
