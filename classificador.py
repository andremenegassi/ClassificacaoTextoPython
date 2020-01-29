import nltk

#****remova os comentários caso não tenha os pacotes a seguir instalados.***
#nltk.download('punkt') 
#nltk.download('rslp') #funções para tratamento de texto em português.
#nltk.download("stopwords") #importar a relação de stopwords.

from nltk.stem import RSLPStemmer #para radicalizar (achar sua base) as palavras

#inteções para treino e suas respostas respostas.
#Em uma aplicação real, isso deve ser extraído de uma base de dados.
dados_treino = []


intencao0 = {"classe":"saudacao", 
             "intencoes": [
                    "Oi",
                    "Olá",
                    "Tudo bem?"],
             "resposta":"Oi. Que legal, vamos conversar."}

    
intencao1 = {"classe":"cursar", 
             "intencoes": [
                    "Quero aprender a programar",
                    "Gostaria de aprender a programar",
                    "Desejo começar a aprender programação"],
             "resposta":"Vem para a FIPP"}

intencao2 = {"classe":"matricular", 
             "intencoes": [
                    "Quando é o período matrícula?",
                    "O período de matrícula está disponível?",
                    "Gostaria de fazer minha matrícula?"
                    "Já posso fazer minha matrícula?"], 
             "resposta":"O período de matrícula é agora."}


intencao3 = {"classe":"python", 
             "intencoes": [
                    "Python é difícil?",
                    "Python é complicado?",], 
             "resposta":"Python é estranho, mas é fácil."}             
    
dados_treino.append(intencao0)
dados_treino.append(intencao1)
dados_treino.append(intencao2)
dados_treino.append(intencao3)




#Quebrar uma sentenca em um vetor de palavras
def Tokenize(sentenca):
    sentenca = sentenca.lower()
    sentenca = nltk.tokenize.word_tokenize(sentenca)
    return sentenca

#Substitui uma palavra por seu radical (quando houver)
def Stemming(palavras):
    stemmer = RSLPStemmer()
    palavras_base = []
    for palavra in palavras:
        palavras_base.append(stemmer.stem(palavra))

    return palavras_base

#Remove palavras irrelevantes para a classificação textual.
def RemoveStopwords(palavras):
    stopwords = nltk.corpus.stopwords.words('portuguese')
    palavras_limpa = []
    for palavra in palavras:
        if (palavra not in stopwords):
            palavras_limpa.append(palavra)

    return palavras_limpa


#Usando os dados do treinamento, será criado um modelo de classificação textual.
#Ao final, um modelo é retornado contendo a quantidade da ocorrência das palavras agrupadas pelo nome da inteção.
#A quantidade de ocorrência será usada para determinar o "match" da intenção do usuário com as inteções previamente cadastradas.
def Treinar():
  
    #Exemplo do modelo de saída
    ''' 
        {
            "classe1": {
                "palavra1: qtdeOcorrencia,
                "palavra2: qtdeOcorrencia,                
            },
            "classe2": {
                "palavra1: qtdeOcorrencia,
                "palavra2: qtdeOcorrencia,                
            }         
        }
    '''

    modelo = {}
    for dado in dados_treino:
        classe = dado["classe"] 
        intencoes = dado["intencoes"]

        palavras = []

        for intencao in intencoes:
            intencao = Tokenize(intencao)
            intencao = Stemming(intencao)
            intencao = RemoveStopwords(intencao)

            palavras += intencao
            
        
        #obtendo a frequência das palavras
        modelo[classe] = dict(nltk.probability.FreqDist(palavras))

    return modelo

#A partir de uma intenção do usuário, é calculado qual intenção é mais próxima
def Cacular_Pontuacao(usuarioIntencao):


    #Exemplo da classificação de saída
    ''' 
        {
            "classe1": pontuação,                
            "classe2": pontuação,                
        }
    '''


    usuarioIntencao = Tokenize(usuarioIntencao)
    usuarioIntencao = Stemming(usuarioIntencao)
    usuarioIntencao = RemoveStopwords(usuarioIntencao)

    classificacao = {}

    for classe in modelo.keys():
        pontos = 0
        
        #os pontos são formados a partir da soma das ocorrências das palavras contidas no treinamento.
        for palavra in usuarioIntencao:
            if (palavra in modelo[classe]):
                pontos += modelo[classe][palavra] #obtendo a quantidade de ocorrência da palavra na classe da iteração atual

        #somente adicionar a classe ao dicionário se ela pontuou.
        if (pontos > 0):
            classificacao[classe] = pontos

    return(classificacao)


def Responder(usuarioIntencao):
    classificacao = Cacular_Pontuacao(usuarioIntencao)

    if (len(classificacao.keys()) == 0):
        print(":-( Não entendi sua pergunta")
    else:

        #localizando a classe com maior pontuação
        classeMaior = max(classificacao, key=classificacao.get)
 
        #obtendo a resposta associada a classe com maior pontuação
        intencao = [i for i in dados_treino if i["classe"] == classeMaior]
        resposta = intencao[0]["resposta"]
        print(resposta)

 


# o modelo pode ser importado, para não ter que treinar sempre.
modelo = Treinar()
 
usuarioIntencao = ""
while (True):
    usuarioIntencao = input("pergunta: ")
    if (usuarioIntencao.lower() != "sair"):
        Responder(usuarioIntencao)
    else: break