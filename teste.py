

#%%

'Norbit' in df['Pedro'].keys()
df
df['Pedro']['Norbit']

df['sum'] = df.loc[:,['Ana', 'Pedro']].sum(axis=1)

import numpy as np
def quadrado(x):
    return np.power(x[0] - x[1], 2)

df['sqr'] = df.loc[:,['Ana', 'Claudia']].apply(lambda x: np.power(x[0] - x[1], 2), axis=1)
df.loc[:,['Ana', 'Claudia', 'sqr']]

np.sqrt(df['sqr'].sum())

df




#%%

df_opa = df.drop(columns='Leonardo')
df_opa



df_opaaa = df.loc[:,['Leonardo']]
filmes = df_opaaa[df_opaaa['Leonardo'].isnull()].index

print(filmes)

totais = {}
somaSimilaridade = {}
for item in filmes:
    similaridade = euclidia('Leonardo', 'Ana')
    print(df['Ana'][item], similaridade)

    totais.setdefault(item, 0)
    totais[item] += df['Ana'][item] * similaridade
    
    somaSimilaridade.setdefault(item, 0)
    somaSimilaridade[item] += similaridade

rankings = [(total / somaSimilaridade[item], item)
            for item, total in totais.items()]

rankings.sort()
rankings.reverse()

rankings