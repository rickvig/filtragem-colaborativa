
#%%
avaliacoes = {
'Ana': 
    {'Freddy x Jason': 2.5, 
    'O Ultimato Bourne': 3.5,
    'Star Trek': 3.0, 
    'Exterminador do Futuro': 3.5, 
    'Norbit': 2.5, 
    'Star Wars': 3.0},
 
'Marcos': 
    {'Freddy x Jason': 3.0, 
    'O Ultimato Bourne': 3.5, 
    'Star Trek': 1.5, 
    'Exterminador do Futuro': 5.0, 
    'Star Wars': 3.0, 
    'Norbit': 3.5}, 

'Pedro': 
    {'Freddy x Jason': 2.5, 
    'O Ultimato Bourne': 3.0,
    'Exterminador do Futuro': 3.5, 
    'Star Wars': 4.0},

'Claudia': 
    {'O Ultimato Bourne': 3.5, 
    'Star Trek': 3.0,
    'Star Wars': 4.5, 
    'Exterminador do Futuro': 4.0, 
    'Norbit': 2.5},

'Adriano': 
    {'Freddy x Jason': 3.0, 
    'O Ultimato Bourne': 4.0, 
    'Star Trek': 2.0, 
    'Exterminador do Futuro': 3.0, 
    'Star Wars': 3.0,
    'Norbit': 2.0}, 

'Janaina': 
    {'Freddy x Jason': 3.0, 
    'O Ultimato Bourne': 4.0,
    'Star Wars': 3.0, 
    'Exterminador do Futuro': 5.0, 
    'Norbit': 3.5},

'Leonardo': 
    {'O Ultimato Bourne':4.5,
    'Norbit':1.0,
    'Exterminador do Futuro':4.0}
}

print(avaliacoes)


#%%
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import Image
import numpy as np

#%%
# Massa de dados

df = pd.DataFrame(avaliacoes)
df


#%%
df['Pedro']['Star Wars']


#%%
dft = df.T
dft = dft.fillna(0)
dft


#%% 
# Gráfico de dispersão

plot = dft.plot(kind='scatter',x='Star Trek', y='Exterminador do Futuro')
plot.ylim(0, 6)
plot.xlim(0, 6)

dft[['Star Trek','Exterminador do Futuro','pessoas']].apply(lambda x: plot.text(*x),axis=1);
dft[['Star Trek','Exterminador do Futuro']]

#%%
Image('dispersao-anotacao.png')

#%%
# Formula da distancia Euclidiana

Image('distancia-euclidiana.png')

#%%
# Calculando a distância Eucliadia

print('''
Ana x Claudia
x = (3, 3)
y = (3.5, 4)

3-3 = 0² -> 0
3.5-4 = 0.5² -> 0.25
0+0.25 = ²√0.25 -> 0.5

Ana x Marcos
x = (3, 1.5)
y = (3.5, 5)
3-1.5 = 1.5² -> 2.25
3.5-5 = 1.5² -> 2.25
2.25+2.25 = ²√4.5 -> 2.12

Ana X Leonardo
x = 3.5, 2.5, 3.5
y = 4.0, 1.0, 4,5
    0.5², 1.5², 1.0²
   0.25 + 2.25 + 1 = ²√3.5 -> 1.87

''')

 
#%%
# Resolvendo escla para 0..1

de = np.sqrt(pow(3-3, 2) + pow(3.5-4, 2))

similaridade = 1 / ( 1 + de )

print("distancia euclidia é {1} e a similaridade de Ana e Claudia para Exterminador do Futuro e Star Trek é {0}%".format(similaridade, de))


#%%
# Funcao para calculo da distância Euclidina

def euclidia(usr1, usr2):

    df['sqr'] = df.loc[:,[usr1, usr2]].apply(
                                        lambda item: 
                                            np.power(item[0] - item[1], 2), 
                                        axis=1)
    
    de = 1 / (1 + np.sqrt(df['sqr'].sum()))
    
    return de

#%%
print(
    euclidia('Ana', 'Claudia'), '\n',
    euclidia('Ana', 'Pedro'), '\n',
    euclidia('Marcos', 'Claudia'), '\n',
    euclidia('Pedro', 'Marcos'), '\n',
    euclidia('Leonardo', 'Ana'))

df = df.drop(columns='sqr')


#%%
# Função de similariaridade por usuário

def getSimilaridade(usr):
    similaridade = [(euclidia(usr, outro), outro)
                    for outro in df.drop(columns=usr).columns]

    similaridade.sort()
    similaridade.reverse()

    return similaridade

#%%
print(
    getSimilaridade('Ana'), '\n\n',
    getSimilaridade('Pedro'), '\n\n',
    getSimilaridade('Marcos'))

df = df.drop(columns='sqr')

#%%
# Gerando recomendações

print('''
Encontrar alguém semelhante para ler as avaliações!

Problemas:
◦ Pessoas que não tenham feito avaliações sobre filmes que pode ser de interesse (pegar somente a pessoa mais semelhante)
◦ Pessoas que tenham gostado de filmes mal avaliados por todos os demais

Solução: atribuir notas usando média ponderada (Peso) -> vamos dar um peso para avaliações

Processo de aquisição das recomendações:
◦ Só vamos gerar recomendações para filmes não assistidos pelo usuário.
◦ Vamos gerar uma nota que provavelmente o usuario daria para esses filmes e ranquea-los
''')

dft

#%%
# Recomendação para Leonardo

getSimilaridade('Leonardo')

# Ver Tabela de calculo de média ponderada --->

#%%
# Gerando Recomendações

def getRecomedacao(usr):
    print(usr)
    
    df_usr = df.loc[:,[usr]]
    filmes = df_usr[df_usr[usr].isnull()].index

    totais = {}
    somaSimilaridade = {}
    for outro in df.drop(columns=usr).columns:
        similaridade = euclidia(usr, outro)

        for item in filmes:
            if np.isnan(df[outro][item]) : continue

            totais.setdefault(item, 0)
            totais[item] += df[outro][item] * similaridade
            
            somaSimilaridade.setdefault(item, 0)
            somaSimilaridade[item] += similaridade

    rankings = [(total / somaSimilaridade[item], item)
                for item, total in totais.items()]

    rankings.sort()
    rankings.reverse()

    return rankings


#%%
# df = df.drop(columns='sqr')
# df = df.drop(columns='sum')
df

#%%
getRecomedacao('Leonardo')


#%%
getRecomedacao('Pedro')

#%%
getRecomedacao('Claudia')

#%%
getRecomedacao('Janaina')