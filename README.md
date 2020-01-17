# ANÁLISE DE DADOS DE ALERTAS

## Como foi realizada a análise:

#### Para a manipulação dos dados foi utilizada a biblioteca Pandas do Python.
- A primeira coisa feita foi importar os dados do arquivo contacts.xlsx para um dataframe:

![Alt text](https://github.com/ibragionp/analise_de_dados_alertas/blob/master/Imagens%20passo%20a%20passo%20c%C3%B3digo/df_sem_alteracoes.png)

- Depois foi feita a separação do telefone em DDI, DDD e número:

![Alt text](https://github.com/ibragionp/analise_de_dados_alertas/blob/master/Imagens%20passo%20a%20passo%20c%C3%B3digo/coluna_telefone_sem_alteracao.png)        ![Alt text](https://github.com/ibragionp/analise_de_dados_alertas/blob/master/Imagens%20passo%20a%20passo%20c%C3%B3digo/colunas_telefone_separado.png)

- As informações de configuração como tipo de alerta (vermelho, amarelo, etc.), dias para receber alertas (dom,sab,etc.) e tipo de recebimento (whatsapp, call, etc.) estavam como marcação de "sim" ou "não". Para tratar isso, foi feita uma lista com essas informações em respectivas colunas de acordo com o contato, para que fosse mais fácil sua separação posteriormente:

Antes
![Alt text](https://github.com/ibragionp/analise_de_dados_alertas/blob/master/Imagens%20passo%20a%20passo%20c%C3%B3digo/colunas_sim_nao.png)

Depois
![Alt text](https://github.com/ibragionp/analise_de_dados_alertas/blob/master/Imagens%20passo%20a%20passo%20c%C3%B3digo/coluna_com_listas.png)

- Com isso, foi feita então a separação dos dados combinando cada item de cada uma das listas e adicionando uma nova linha ao Datraframe com suas respectivas informações complementares:

![Alt text](https://github.com/ibragionp/analise_de_dados_alertas/blob/master/Imagens%20passo%20a%20passo%20c%C3%B3digo/colunas_separadas.png)

- Finalizado esse tratamento, partimos para parte onde foi conveniente criar um ID para cada "tabela" que possuiria no próprio Dataframe principal e depois copiar apenas as colunas que fossem pertinentes a "tabela":

(A ordenação do ID não se fez necessária)

![Alt text](https://github.com/ibragionp/analise_de_dados_alertas/blob/master/Imagens%20passo%20a%20passo%20c%C3%B3digo/df_contato.png)

(Podemos notar como exemplo, "tabela" telefone com a coluna "contato_id" que faz referência a coluna da "tabela" contatos)

![Alt text](https://github.com/ibragionp/analise_de_dados_alertas/blob/master/Imagens%20passo%20a%20passo%20c%C3%B3digo/df_telefone.png)

(Nesse outro exemplo, podemos notar que as linhas marcadas possuem as mesmas informações, porém muda o tipo de envio de alerta um é "sms" e o outro "email")
![Alt text](https://github.com/ibragionp/analise_de_dados_alertas/blob/master/Imagens%20passo%20a%20passo%20c%C3%B3digo/df_envio_alerta.png)

(Já aqui, muda oque seria o nosso "periodo" de envio, mas trata-se do mesmo contato da imagem anterior, porque foi escolhido receber alertas em diversos dias da semana(periodos))
![Altt text](https://github.com/ibragionp/analise_de_dados_alertas/blob/master/Imagens%20passo%20a%20passo%20c%C3%B3digo/df_envio_alerta_ex2.png)

- Para finalizar, após inserir os dados no banco, foi feito um select para descobrir o ID do primeiro email do arquivo excel.xlsx (foi considerado como unique o email). E em seguida, um select para buscar as configurações de alerta de envio:

![Alt text](https://github.com/ibragionp/analise_de_dados_alertas/blob/master/Imagens%20passo%20a%20passo%20c%C3%B3digo/primeiro_email_excel.png)

![Alt text](https://github.com/ibragionp/analise_de_dados_alertas/blob/master/Imagens%20passo%20a%20passo%20c%C3%B3digo/consulta_primeiro_email_alertas.png)

## Como executar o projeto:

#### Informações importantes
- Primeiro é necessário fazer download do projeto e criar o banco de dados. Para criar com as configurações corretas como nome das tabelas, tipos, etc., no repositório existe um arquivo chamado "sql_create_tables_database_alertas.sql", ele já é um .sql que pode ser executado no Query Tool.

- Depois é necessária a instalação das bibliotecas utilizadas, que são (psycopg2, pandas, timeit):
![Alt text](https://github.com/ibragionp/analise_de_dados_alertas/blob/master/Imagens%20como%20rodar%20o%20codigo/bibliotecas_necessarias.png)

- Para execução do código ou alteração futuramente, é necessária a alteração de do diretório onde o projeto está salvo:
![Alt text](https://github.com/ibragionp/analise_de_dados_alertas/blob/master/Imagens%20como%20rodar%20o%20codigo/diretorio_do_projeto.png)

- E por fim, para conexão correta do banco, é necessária a alteração das informações de acordo com o banco que foi criado anteriormente:
![Alt text](https://github.com/ibragionp/analise_de_dados_alertas/blob/master/Imagens%20como%20rodar%20o%20codigo/informacoes_do_banco_de_dados_da_maquina_pessoal.png)

*Lembrando que as variáveis que necessitam de alteração em seu valor, estão no ínicio do código .py*
