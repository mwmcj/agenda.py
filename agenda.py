# -*- coding: utf-8 -*-
import sys

TODO_FILE = 'todo.txt'
ARCHIVE_FILE = 'done.txt'

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"
YELLOW = "\033[0;33m"

ADICIONAR = 'a'
REMOVER = 'r'
FAZER = 'f'
PRIORIZAR = 'p'
LISTAR = 'l'

# Imprime texto com cores. Por exemplo, para imprimir "Oi mundo!" em vermelho, basta usar
#
# printCores('Oi mundo!', RED)
# printCores('Texto amarelo e negrito', YELLOW + BOLD)

def printCores(texto, cor) :
  print(cor + texto + RESET)
  

# Adiciona um compromisso aa agenda. Um compromisso tem no minimo
# uma descrição. Adicionalmente, pode ter, em caráter opcional, uma
# data (formato DDMMAAAA), um horário (formato HHMM), uma prioridade de A a Z, 
# um contexto onde a atividade será realizada (precedido pelo caractere
# '@') e um projeto do qual faz parte (precedido pelo caractere '+'). Esses
# itens opcionais são os elementos da tupla "extras", o segundo parâmetro da
# função.
#
# extras ~ (data, hora, prioridade, contexto, projeto)
#
# Qualquer elemento da tupla que contenha um string vazio ('') não
# deve ser levado em cpython agenda.py l
#onsideração. 
def adicionar(descricao, extras):

  # não é possível adicionar uma atividade que não possui descrição. 
  if descricao  == '' :
    return False
  novaAtividade=''
  if extras[0]:
    novaAtividade+=extras[0]+' '
  if extras[1]:
    novaAtividade+=extras[1]+' '
  if extras[2]:
    novaAtividade+=extras[2]+' '
  novaAtividade+=descricao
  if extras[3]:
    novaAtividade+=' '+extras[3]
  if extras[4]:
    novaAtividade+=' '+extras[4]
  ################ COMPLETAR
  

  # Escreve no TODO_FILE. 
  try: 
    fp = open(TODO_FILE, 'a')
    fp.write(novaAtividade + "\n")
    fp.close()
  except IOError as err:
    print("Não foi possível escrever para o arquivo " + TODO_FILE)
    print(err)
    return False
  print('adicionado com sucesso')
  return True


# Valida a prioridade.
def prioridadeValida(pri):
  if len(pri)!=3:
    return False
  else:
    if pri[0]=='(' and ((pri[1]<='z' and pri[1]>='a') or (pri[1]<='Z' and pri[1]>='A')) and pri[2]==')':
      return True
    return False
    


# Valida a hora. Consideramos que o dia tem 24 horas, como no Brasil, ao invés
# de dois blocos de 12 (AM e PM), como nos EUA.
def horaValida(horaMin) :
  if len(horaMin) != 4 or not soDigitos(horaMin):
    return False
  else:
    if (int(horaMin[0]+horaMin[1])>23 or int(horaMin[0]+horaMin[1])<0) or (int(horaMin[2]+horaMin[3])>59 or int(horaMin[2]+horaMin[3])<0):
      return False
    return True

# Valida datas. Verificar inclusive se não estamos tentando
# colocar 31 dias em fevereiro. Não precisamos nos certificar, porém,
# de que um ano é bissexto. 
def dataValida(data) :
  if len(data)!=8 or not soDigitos(data):
    return False
  else:
    valido=True
#PELO AMOR DE DEUS VÁ SABER O QUE É UM ANO VÁLIDO
    if valido and (int(data[2]+data[3])>12 or int(data[2]+data[3])<1):
      valido=False
    elif valido and ((int(data[0]+data[1])<0) and (int(data[0]+data[1])>30 and (int(data[2]+data[3])==4 or int(data[2]+data[3])==6 or int(data[2]+data[3])==9 or int(data[2]+data[3])==11)) or (int(data[0]+data[1])>31 and (int(data[2]+data[3])==3 or int(data[2]+data[3])==5 or int(data[2]+data[3])==7 or int(data[2]+data[3])==8 or int(data[2]+data[3])==10 or int(data[2]+data[3])==12)) or (int(data[0]+data[1])>29 and (int(data[2]+data[3])==2))):
      valido=False
  return valido

# Valida que o string do projeto está no formato correto. 
def projetoValido(proj):
  if len(proj)<2:
    return False
  else:
    if proj[0]=='+':
      return True
    return False

# Valida que o string do contexto está no formato correto. 
def contextoValido(cont):
  if len(cont)<2:
    return False
  else:
    if cont[0]=='@':
      return True
    return False

# Valida que a data ou a hora contém apenas dígitos, desprezando espaços
# extras no início e no fim.
def soDigitos(numero) :
  if type(numero) != str :
    return False
  for x in numero :
    if x < '0' or x > '9' :
      return False
  return True


# Dadas as linhas de texto obtidas a partir do arquivo texto todo.txt, devolve
# uma lista de tuplas contendo os pedaços de cada linha, conforme o seguinte
# formato:
#
# (descrição, prioridade, (data, hora, contexto, projeto))
#
# É importante lembrar que linhas do arquivo todo.txt devem estar organizadas de acordo com o
# seguinte formato:
#
# DDMMAAAA HHMM (P) DESC @CONTEXT +PROJ
#
# Todos os itens menos DESC são opcionais. Se qualquer um deles estiver fora do formato, por exemplo,
# data que não tem todos os componentes ou prioridade com mais de um caractere (além dos parênteses),
# tudo que vier depois será considerado parte da descrição.  
def organizar(linhas):
  itens = []

  for l in linhas:
    data = '' 
    hora = ''
    pri = ''
    desc = ''
    contexto = ''
    projeto = ''
  
    l = l.strip() # remove espaços em branco e quebras de linha do começo e do fim
    tokens = l.split() # quebra o string em palavras
    if dataValida(tokens[0]) and len(tokens)>1:
      data=tokens.pop(0)
    if horaValida(tokens[0]) and len(tokens)>1:
      hora=tokens.pop(0)
    if prioridadeValida(tokens[0]) and len(tokens)>1:
      pri=tokens.pop(0)
      pri=pri.upper()
    if projetoValido(tokens[len(tokens)-1]) and len(tokens)>1:
      projeto=tokens.pop(len(tokens)-1)
    if contextoValido(tokens[len(tokens)-1]) and len(tokens)>1:
      contexto=tokens.pop(len(tokens)-1)
    for palavra in tokens:
      desc+=(palavra+' ')
    

    # Processa os tokens um a um, verificando se são as partes da atividade.
    # Por exemplo, se o primeiro token é uma data válida, deve ser guardado
    # na variável data e posteriormente removido a lista de tokens. Feito isso,
    # é só repetir o processo verificando se o primeiro token é uma hora. Depois,
    # faz-se o mesmo para prioridade. Neste ponto, verifica-se os últimos tokens
    # para saber se são contexto e/ou projeto. Quando isso terminar, o que sobrar
    # corresponde à descrição. É só transformar a lista de tokens em um string e
    # construir a tupla com as informações disponíveis. 

    ################ COMPLETAR

    itens.append((desc, (data, hora, pri, contexto, projeto)))

  return itens


# Datas e horas são armazenadas nos formatos DDMMAAAA e HHMM, mas são exibidas
# como se espera (com os separadores apropridados). 
#
# Uma extensão possível é listar com base em diversos critérios: (i) atividades com certa prioridade;
# (ii) atividades a ser realizadas em certo contexto; (iii) atividades associadas com
# determinado projeto; (vi) atividades de determinado dia (data específica, hoje ou amanhã). Isso não
# é uma das tarefas básicas do projeto, porém. 
def listar():
  arquivo=open(TODO_FILE,'r')
  linhas=arquivo.readlines()
  arquivo.close()
  itens=organizar(linhas)
  itens=auxOrdenarPorAno(itens)
  itens=ordenarPorPrioridade(itens)
  ordem='1'
  for x in itens:
    atividade=ordem+' '+reOrganizarFormatado(x[0],x[1])
    if x[1][2]=='(A)':
      atividade=BOLD+RED+atividade+RESET
    elif x[1][2]=='(B)':
      atividade=BLUE+atividade+RESET
    elif x[1][2]=='(C)':
      atividade=CYAN+atividade+RESET
    elif x[1][2]=='(D)':
      atividade=GREEN+atividade+RESET
    print(atividade)
    ordem=str(1+int(ordem))
  ################ COMPLETAR
  return 
def formatarData(data):
  data=data[0:2]+'/'+data[2:4]+'/'+data[4:]
  return data
def formatarHora(hora):
  hora=hora[0:2]+'h'+hora[2:]+'m'
  return hora
  
def reOrganizarFormatado(descricao, extras):
  atividade=''
  if extras[0]:
    atividade+=formatarData(extras[0])+' '
  if extras[1]:
    atividade+=formatarHora(extras[1])+' '
  if extras[2]:
    atividade+=extras[2]+' '
  atividade+=descricao
  if extras[3]:
    atividade+=' '+extras[3]
  if extras[4]:
    atividade+=' '+extras[4]
  return atividade
def reOrganizar(descricao, extras):
  atividade=''
  if extras[0]:
    atividade+=extras[0]+' '
  if extras[1]:
    atividade+=extras[1]+' '
  if extras[2]:
    atividade+=extras[2]+' '
  atividade+=descricao
  if extras[3]:
    atividade+=' '+extras[3]
  if extras[4]:
    atividade+=' '+extras[4]
  return atividade
def ordenarPorDataHora(itens):
  return auxOrdenarPorAno(itens)

def auxOrdenarPorAno(itens):
  if not itens:
    return []
  
  else:
    if [x for x in itens if not x[1][0]]:
      return auxOrdenarPorAno([x for x in itens if x[1][0]])+auxOrdenarPorHora([x for x in itens if not x[1][0]])
    else:
        pivo=itens.pop()
        return auxOrdenarPorAno([x for x in itens if x[1][0][4:8]<pivo[1][0][4:8]])+auxOrdenarPorMes([x for x in itens if x[1][0][4:8]==pivo[1][0][4:8]]+[pivo])+auxOrdenarPorAno([x for x in itens if x[1][0][4:8]>pivo[1][0][4:8]])

def auxOrdenarPorMes(itens):
  if not itens:
    return []
  else:
    pivo=itens.pop()
    return auxOrdenarPorMes([x for x in itens if x[1][0][2:4]<pivo[1][0][2:4]])+auxOrdenarPorDia([x for x in itens if x[1][0][2:4]==pivo[1][0][2:4]]+[pivo])+auxOrdenarPorMes([x for x in itens if x[1][0][2:4]>pivo[1][0][2:4]])

def auxOrdenarPorDia(itens):
  if not itens:
    return []
  else:
    pivo=itens.pop()
    return auxOrdenarPorDia([x for x in itens if x[1][0][0:2]<pivo[1][0][0:2]])+auxOrdenarPorHora([x for x in itens if x[1][0][0:2]==pivo[1][0][0:2]]+[pivo])+auxOrdenarPorDia([x for x in itens if x[1][0][0:2]>pivo[1][0][0:2]])

def auxOrdenarPorHora(itens):
  if not itens:
    return []
  else:
    if [x for x in itens if not x[1][1]]:
      return auxOrdenarPorHora([x for x in itens if x[1][1]])+[x for x in itens if not x[1][1]]
    else:
      pivo=itens.pop()
      return auxOrdenarPorHora([x for x in itens if x[1][1][0:2]<pivo[1][1][0:2]])+auxOrdenarPorMin([x for x in itens if x[1][1][0:2]==pivo[1][1][0:2]]+[pivo])+auxOrdenarPorHora([x for x in itens if x[1][1][0:2]>pivo[1][1][0:2]])

def auxOrdenarPorMin(itens):
  if not itens:
    return []
  else:
    pivo=itens.pop()
    return auxOrdenarPorMin([x for x in itens if x[1][1][2:4]<pivo[1][1][2:4]])+[x for x in itens if x[1][1][2:4]==pivo[1][1][2:4]]+[pivo]+auxOrdenarPorMin([x for x in itens if x[1][1][2:4]>pivo[1][1][2:4]])

def ordenarPorPrioridade(itens):
  if not itens:
    return []
  else:
    if [x for x in itens if not x[1][2]]:
      return ordenarPorPrioridade([x for x in itens if x[1][2]])+[x for x in itens if not x[1][2]]
    else:
      pivo=itens.pop()
      return ordenarPorPrioridade([x for x in itens if x[1][2][1]<pivo[1][2][1]])+[x for x in itens if x[1][2][1]==pivo[1][2][1]]+[pivo]+ordenarPorPrioridade([x for x in itens if x[1][2][1]>pivo[1][2][1]])


def fazer(num):
  num=int(num)
  arquivo=open(TODO_FILE,'r')
  linhas=arquivo.readlines()
  arquivo.close()
  itens=organizar(linhas)
  itens=auxOrdenarPorAno(itens)
  itens=ordenarPorPrioridade(itens)
  if num>len(itens):
    print('não há, esse compromisso, na agenda!')
    return False
  else:
    arquivo=open('done.txt','a')
    feito=reOrganizar(itens[num-1][0],itens[num-1][1])
    arquivo.write(feito)
    arquivo.close()
    remover(str(num))
    print('adicionado ao arquivo done')
    return True

def remover(num):
  num=int(num)
  arquivo=open(TODO_FILE,'r')
  linhas=arquivo.readlines()
  arquivo.close()
  itens=organizar(linhas)
  itens=auxOrdenarPorAno(itens)
  itens=ordenarPorPrioridade(itens)
  if num>len(itens):
    print('não há, esse compromisso, na agenda!')
    return False
#  print(reOrganizar(itens[num-1][0],itens[num-1][1])+'\ntem certeza que quer removêlo?')
#  validação=input('1-sim 2-não')
#  while validação!='1' and validação!='2':
#    validação=input('1-sim 2-não')
#  if validação=='2':
#    return False
  else:
    itens.pop(num-1)
    auxItens=itens[:]
    for x in auxItens:
      itens.pop(0)
      itens.append(reOrganizar(x[0],x[1])+'\n')
    arquivo=open(TODO_FILE,'w')
    arquivo.writelines(itens)
    arquivo.close
    print('arquivo removido com sucesso')
    return True
# prioridade é uma letra entre A a Z, onde A é a mais alta e Z a mais baixa.
# num é o número da atividade cuja prioridade se planeja modificar, conforme
# exibido pelo comando 'l'. 
def priorizar(num, prioridade):
  prioridade=prioridade.upper()
  num=int(num)
  arquivo=open('todo.txt','r')
  linhas=arquivo.readlines()
  arquivo.close()
  itens=organizar(linhas)
  itens=auxOrdenarPorAno(itens)
  itens=ordenarPorPrioridade(itens)
  if num>len(itens):
    print('não há, esse compromisso, na agenda!')
    return False
  itens[num-1]=auxPriorizar(itens[num-1][0],itens[num-1][1],prioridade)
  auxItens=itens[:]
  for x in auxItens:
    itens.pop(0)
    itens.append(reOrganizar(x[0],x[1])+'\n')
  arquivo=open('todo.txt','w')
  arquivo.writelines(itens)
  arquivo.close
  print('prioridade alterada com sucesso')
  return True
def auxPriorizar(desc,extras,prioridade):
  extras=(extras[0],extras[1],('('+prioridade+')'),extras[3],extras[4])
  return (desc,extras)


# Esta função processa os comandos e informações passados através da linha de comando e identifica
# que função do programa deve ser invocada. Por exemplo, se o comando 'adicionar' foi usado,
# isso significa que a função adicionar() deve ser invocada para registrar a nova atividade.
# O bloco principal fica responsável também por tirar espaços em branco no início e fim dos strings
# usando o método strip(). Além disso, realiza a validação de horas, datas, prioridades, contextos e
# projetos. 
def processarComandos(comandos) :
  if comandos[1] == ADICIONAR:
    comandos.pop(0) # remove 'agenda.py'
    comandos.pop(0) # remove 'adicionar'
    itemParaAdicionar = organizar([' '.join(comandos)])[0]
    # itemParaAdicionar = (descricao, (prioridade, data, hora, contexto, projeto))
    adicionar(itemParaAdicionar[0], itemParaAdicionar[1]) # novos itens não têm prioridade
  elif comandos[1] == LISTAR:
    return listar()   
    ################ COMPLETAR

  elif comandos[1] == REMOVER:
    if not soDigitos(comandos[2]):
      print("Comando inválido.")
      return False
    else:
      return remover(comandos[2]) 

    ################ COMPLETAR    

  elif comandos[1] == FAZER:
    if not soDigitos(comandos[2]):
      print("Comando inválido.")
      return False
    else:
      return fazer(comandos[2])

    ################ COMPLETAR

  elif comandos[1] == PRIORIZAR:
    if not soDigitos(comandos[2]) or not prioridadeValida('('+comandos[3]+')'):
      print("Comando inválido.")
      return False
    else:
      return priorizar(comandos[2],comandos[3])
  
  else :
    print("Comando inválido.")
    
  
# sys.argv é uma lista de strings onde o primeiro elemento é o nome do programa
# invocado a partir da linha de comando e os elementos restantes são tudo que
# foi fornecido em sequência. Por exemplo, se o programa foi invocado como
#
# python3 agenda.py a Mudar de nome.
#
# sys.argv terá como conteúdo
#
# ['agenda.py', 'a', 'Mudar', 'de', 'nome']
processarComandos(sys.argv)
