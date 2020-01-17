#Biblioteca Pandas para manipulação de dados
import pandas as pd
#Biblioteca timeit para manipulção de hora sistema
import timeit
#Biblioteca Psycopg para conexão do Python com o PostgreSQL
import psycopg2

#Pega a hora que iníciou a execução do script
start = timeit.default_timer()

#Informações para conexão com o banco de dados
nome_banco_de_dados = 'alertas'
nome_usuario = 'postgres'
senha_banco_de_dados = 'jbg258297'

#Diretório onde se encontra nosso arquivo com os dados .xlsx
diretorio_arquivo = 'C:\\Users\\isabe\\Desktop\\Projeto Climatempo\\'
#Nome do nosso arquivo .xlsx
nome_arquivo = 'contacts.xlsx'
#Nome da planilha do arquivo onde se encontra os dados
planilha = 'alertas'

#Definição de variáveis
lista_colunas_alertas = ['sms', 'email', 'call', 'push', 'whatsapp']
lista_colunas_dias = ['dom', 'seg', 'ter', 'qua', 'qui', 'sex', 'sab']
lista_colunas_tipos = ['alerta_verde', 'alerta_amarelo', 'alerta_vermelho']

coluna_lista_alertas = 'lista_alertas'
coluna_lista_tipos = 'lista_tipos'
coluna_lista_dias = 'lista_dias'

coluna_alerta = 'envio_alerta_descricao'
coluna_tipo = 'tipo_descricao'
coluna_dia = 'periodo_dia'

coluna_nome = 'contato_nome'
coluna_telefone = 'telefone_numero'
coluna_localidade = 'localidade_descricao'
coluna_hora_inicial = 'periodo_hora_inicial'
coluna_hora_final = 'periodo_hora_final'
coluna_email = 'email_endereco'

coluna_contato_id = 'contato_id'
coluna_email_id = 'email_id'
coluna_telefone_id = 'telefone_id'
coluna_localidade_id = 'localidade_id'
coluna_tipo_id = 'tipo_id'
coluna_envio_alerta_id = 'envio_alerta_id'
coluna_periodo_id = 'periodo_id'

#Função para abertura do arquivo e colocar em uma estrutura do tipo Dataframe
def abrir_arquivo():
    
    df = pd.read_excel(diretorio_arquivo + nome_arquivo, planilha)
    
    return df

#Função para separar telefone
def separa_ddi_ddd(linha):
    
    linha['telefone_ddi'] = linha[coluna_telefone].strip().split(' ')[0]
    linha['telefone_ddd'] = linha[coluna_telefone].strip().split(' ')[1]
    linha[coluna_telefone] = linha[coluna_telefone].strip().split(' ')[2]
    
    return linha

def cria_lista_valores(linha, lista_colunas):
    
    
    lista_valores = list(linha[lista_colunas])
    lista_valores = list(filter(None, lista_valores))
    
    return lista_valores

#Função para transformar os valores sim e não em lista para utilização posteriormente
def trata_dados(lista_colunas, nome_nova_coluna):
    
    for i in range(len(lista_colunas)):
    
        df.loc[df[lista_colunas[i]].str.lower().str.strip() == 'sim', 
               lista_colunas[i]] = lista_colunas[i]
        
    df.replace("nao", "", inplace=True)
    df[nome_nova_coluna] = df.apply(cria_lista_valores, args=[lista_colunas], 
      axis = 1)
    df.drop(columns=lista_colunas, inplace = True)

    return df

#Função para separar lista e duplicar linha caso necessário com informações pertinentes
def separa_dados():
    
    df_final = pd.DataFrame()
    
    for index, row in df.iterrows():
        
        print(index)
        
        df_slice = pd.DataFrame(columns=df.columns)
        df_slice = pd.concat([df_slice,pd.DataFrame(columns=[coluna_alerta, 
                                                             coluna_tipo, 
                                                             coluna_dia])],\
        sort=False)
    
        for i in range(len(row[coluna_lista_dias])): 
            
            for j in range(len(row[coluna_lista_alertas])):
                
                for k in range(len(row[coluna_lista_tipos])):
                    
                    df_slice = pd.concat([df_slice, pd.DataFrame(row).transpose()], 
                                          sort=False)
                    df_slice.iloc[-1, df_slice.columns.get_loc(coluna_dia)] = \
                    row[coluna_lista_dias][i]
                    df_slice.iloc[-1, df_slice.columns.get_loc(coluna_alerta)] = \
                    row[coluna_lista_alertas][j]
                    df_slice.iloc[-1, df_slice.columns.get_loc(coluna_tipo)] = \
                    row[coluna_lista_tipos][k]
        
        df_final = pd.concat([df_final, df_slice], sort=False)
        #df = pd.DataFrame(columns=df.columns)

    df_final.drop(columns=[coluna_lista_dias, coluna_lista_alertas, 
                           coluna_lista_tipos], inplace=True)
    df_final.reset_index(drop=True, inplace=True)    
    
    return df_final

#Função para gerar id, dependendo da coluna que será usada como base e o nome que
#será atribuido à ela
def gerar_id(coluna, nome_coluna):
    
    new_df = df.assign(id=(df[coluna]).astype('category').cat.codes)
    new_df.rename(columns={'id':nome_coluna}, inplace=True)
    new_df[nome_coluna] = new_df[nome_coluna].apply(lambda x: x+1)

    return new_df

#Abre o arquivo contacts.xlsx
df = abrir_arquivo()

#renomea as colunas para facilitar a sua manipulação posteriormente
df.rename(columns={'nome': coluna_nome, 'email':coluna_email, 
                   'telefone':coluna_telefone, 'hora_inicial': \
                   coluna_hora_inicial, 'hora_final':coluna_hora_final,
                   'regiao':coluna_localidade, 'email.1':'email'}, inplace=True)

#separa o telefone em DDI, DDD e número
df = df.apply(separa_ddi_ddd, axis= 1)
    
#Adiciona informações onde só há sim e não à uma única lista, para posteriormente
#podermos separar
df = trata_dados(lista_colunas_alertas, coluna_lista_alertas)
df = trata_dados(lista_colunas_dias, coluna_lista_dias)
df = trata_dados(lista_colunas_tipos, coluna_lista_tipos)

#Separa a lista
df = separa_dados()

#Gera um id para cada tabela que irá possuir ID, com base no valor da coluna 
#escolhida e cria um Dataframe com dados pertinentes a cada tabela do banco
#removendo também valores duplicados
df = gerar_id(coluna_email,coluna_contato_id)
df_contatos = (df[[coluna_contato_id, coluna_nome]]).drop_duplicates()

df[coluna_email_id] = df[coluna_contato_id]
df_emails = (df[[coluna_contato_id, coluna_email_id, coluna_email]]).drop_duplicates()

df = gerar_id(coluna_telefone, coluna_telefone_id)
df_telefones = (df[[coluna_contato_id, coluna_telefone_id, 'telefone_ddi', 
                    'telefone_ddd', coluna_telefone]]).drop_duplicates()

df = gerar_id(coluna_tipo, coluna_tipo_id)
df_tipos = (df[[coluna_tipo_id, coluna_tipo]]).drop_duplicates()

df = gerar_id(coluna_localidade, coluna_localidade_id)
df_localidades = (df[[coluna_localidade_id, coluna_localidade]]).drop_duplicates()

df = df.assign(periodo_id=(df[coluna_hora_inicial] + '_' + 
                           df[coluna_hora_final] + '_' + df[coluna_dia]).astype('category').cat.codes)
df[coluna_periodo_id] = df[coluna_periodo_id].apply(lambda x: x+1)
df_periodos = (df[[coluna_periodo_id, coluna_hora_inicial,
                 coluna_hora_final, coluna_dia]]).drop_duplicates()

#Formata o tipo das colunas hora inicial e hora final no formato time, para ficar
#igual ao tipo criado no banco de dados
df_periodos[coluna_hora_inicial] = pd.to_datetime(df_periodos[coluna_hora_inicial]\
          ,format='%H:%M').dt.time
df_periodos[coluna_hora_final] = pd.to_datetime(df_periodos[coluna_hora_final],\
          format='%H:%M').dt.time


df[coluna_envio_alerta_id] = pd.Series(range(1,df.shape[0] +1))
df_envios_alertas = (df[[coluna_envio_alerta_id, coluna_contato_id, 
                         coluna_telefone_id, coluna_email_id, 
                         coluna_localidade_id, coluna_tipo_id, 
                         coluna_periodo_id, coluna_alerta]]).drop_duplicates()


#Lista com todos os daframes separados
dfs = [df_contatos, df_telefones, df_emails, df_localidades, df_tipos, df_periodos,
       df_envios_alertas]
#Lista com o nome das tabelas do nosso banco, na mesma sequência que a lista de
#Dataframes
tabelas = ['contatos', 'telefones', 'emails', 'localidades', 'tipos', 'periodos', 
           'envios_alertas']

#Conexão com o Banco de dados PostgreSQL
connection = psycopg2.connect(host='localhost', database=nome_banco_de_dados,
                              user=nome_usuario, password=senha_banco_de_dados)
    
cursor = connection.cursor()
cont = 0
#For que vai passar por cada Dataframe da minha lista
for data in dfs:
    
    #Junto o nome das colunas do meu Dataframe para passar no Insert do banco
    cols = ",".join([str(i) for i in data.columns.to_list()])
    
    #For para passar em cada linha do meu Dataframe e inserir ao Banco
    for i,row in data.iterrows():
        sql = "INSERT INTO " + tabelas[cont] + " (" + cols + ") VALUES (" + "%s,"*(len(row)-1) + "%s)"
        cursor.execute(sql, tuple(row))
        connection.commit()
    cont += 1        

#Encerrando conexão
connection.close()
#Retorno do tempo de execução do script(aplicação)
stop = timeit.default_timer()   
print('Time: ', stop - start)  