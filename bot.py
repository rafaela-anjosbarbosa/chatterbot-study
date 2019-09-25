# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 11:25:34 2019

@author: Rafaela
"""

import os
from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.conversation import Statement
import wikipedia

bot = ChatBot('Botzin')
nome_pasta='treino'
wikipedia.set_lang("pt")

def treina(nome_pasta):
        trainer = ChatterBotCorpusTrainer(bot)
        trainer.train("chatterbot.corpus.portuguese")       
        trainer = ListTrainer(bot)
        for treino in os.listdir(nome_pasta):
            arquivos = open(nome_pasta+'/'+treino, 'r', encoding="utf-8").readlines()
            trainer.train(arquivos)
treina(nome_pasta)

def aprender():
    text = input()
    if 's' in text.lower():
        print('Escreva a resposta correta para: '+pergunta)
        resposta_correta = Statement(input())
        bot.learn_response(resposta_correta, pergunta)
        arquivo_aprendizado(resposta_correta)
        print('Resposta adicionada ao bot!')
        return True
    elif 'n' in text.lower():
        return False
    else:
        print('Por favor, responda "S" ou "N"')
        return aprender()

def pesquisar():
    text = input()
    if (text.lower()!='nada'):
        try:
            print (wikipedia.summary(text))
        except:
            opcoes = wikipedia.search(text)
            print (bot.name+': Essas são as opções de pesquisa para: '+text)
            for i, item in enumerate(opcoes):
                if i > 0:
                    print (i, item)
            opcao = int(input(bot.name+': Escolha a opção: '))
            assert opcao in range(len(opcoes))
            print (wikipedia.summary(opcoes[opcao]))
        return True
    elif 'nada' in text.lower():
        return False
    else:
        print(bot.name+': Por favor, digite algum termo para ser pesquisado ou responda "NADA"')
        return aprender()
    
def arquivo_aprendizado(resposta_correta):
        trainer = ListTrainer(bot)
        arquivo = open(nome_pasta+'/'+'aprendizados.txt', 'a+', encoding='UTF-8')
        conteudo = arquivo.readlines()
        conteudo.append(str(pergunta)+'\n'+str(resposta_correta)+'\n')
        arquivo.writelines(conteudo)
        arquivo.close()
        arquivo = open(nome_pasta+'/'+'aprendizados.txt', 'r', encoding='UTF-8').readlines()
        trainer.train(arquivo)
          
while True:
    pergunta = input("Usuário: ")
    resposta = bot.get_response(pergunta)
    if (pergunta!='sair'):
        if float(resposta.confidence) >= 0.1:
            print(bot.name+':', resposta)
        elif (pergunta=='pesquisar'):
            print(bot.name+': O que você deseja pesquisar? Digita NADA para voltarmos a conversar.')
            pesquisar()
        else:
            print(bot.name+': Ainda não sei responder esta pergunta. Gostaria de me ensinar? Responda S ou N')
            aprender()
    else:
        print(bot.name+': Até logo!')
        break