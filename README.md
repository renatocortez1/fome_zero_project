# Projeto de Aluno da Comunidade DS - Fome Zero!
## 1. Contexto do Problema de Negócio:
  Parabéns! Você acaba de ser contratado como Cientista de Dados da empresa
Fome Zero, e a sua principal tarefa nesse momento é ajudar o CEO Kleiton Guerra
a identificar pontos chaves da empresa, respondendo às perguntas que ele fizer
utilizando dados!

  A empresa Fome Zero é uma marketplace de restaurantes. Ou seja, seu core
business é facilitar o encontro e negociações de clientes e restaurantes. Os
restaurantes fazem o cadastro dentro da plataforma da Fome Zero, que disponibiliza
informações como endereço, tipo de culinária servida, se possui reservas, se faz
entregas e também uma nota de avaliação dos serviços e produtos do restaurante,
dentre outras informações.

### O Desafio

O CEO Guerra também foi recém contratado e precisa entender melhor o negócio
para conseguir tomar as melhores decisões estratégicas e alavancar ainda mais a
Fome Zero, e para isso, ele precisa que seja feita uma análise nos dados da
empresa e que sejam gerados dashboards, a partir dessas análises, para responder
às seguintes perguntas:

### Geral
1. Quantos restaurantes únicos estão registrados?
2. Quantos países únicos estão registrados?
3. Quantas cidades únicas estão registradas?
4. Qual o total de avaliações feitas?
5. Qual o total de tipos de culinária registrados?
   
### País
1. Qual o nome do país que possui mais cidades registradas?
2. Qual o nome do país que possui mais restaurantes registrados?
3. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4 registrados?
4. Qual o nome do país que possui a maior quantidade de tipos de culinária distintos?
5. Qual o nome do país que possui a maior quantidade de avaliações feitas?
6. Qual o nome do país que possui a maior quantidade de restaurantes que fazem entrega?
7. Qual o nome do país que possui a maior quantidade de restaurantes que aceitam reservas?
8. Qual o nome do país que possui, na média, a maior quantidade de avaliações registrada?
9. Qual o nome do país que possui, na média, a maior nota média registrada?
10. Qual o nome do país que possui, na média, a menor nota média registrada?
11. Qual a média de preço de um prato para dois por país?

### Cidade
1. Qual o nome da cidade que possui mais restaurantes registrados?
2. Qual o nome da cidade que possui mais restaurantes com nota média acima de 4?
3. Qual o nome da cidade que possui mais restaurantes com nota média abaixo de 2.5?
4. Qual o nome da cidade que possui o maior valor médio de um prato para dois?
5. Qual o nome da cidade que possui a maior quantidade de tipos de culinária distintas?
6. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem reservas?
7. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem entregas?
8. Qual o nome da cidade que possui a maior quantidade de restaurantes que aceitam pedidos online?

### Restaurantes
1. Qual o nome do restaurante que possui a maior quantidade de avaliações?
2. Qual o nome do restaurante com a maior nota média?
3. Qual o nome do restaurante que possui o maior valor de um prato para duas pessoas?
4. Qual o nome do restaurante de tipo de culinária brasileira que possui a menor média de avaliação?
5. Qual o nome do restaurante de tipo de culinária brasileira, e que é do Brasil, que possui a maior média de avaliação?
6. Os restaurantes que aceitam pedido online são também, na média, os restaurantes que mais possuem avaliações registradas?
7. Os restaurantes que fazem reservas são também, na média, os restaurantes que possuem o maior valor médio de um prato para duas pessoas?
8. Os restaurantes do tipo de culinária japonesa dos Estados Unidos da América possuem um valor médio de prato para duas pessoas maior que as churrascarias americanas (BBQ)?

### Tipos de Culinária
1. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a maior média de avaliação?
2. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a menor média de avaliação?
3. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do restaurante com a maior média de avaliação?
4. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do restaurante com a menor média de avaliação?
5. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do restaurante com a maior média de avaliação?
6. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do restaurante com a menor média de avaliação?
7. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do restaurante com a maior média de avaliação?
8. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do restaurante com a menor média de avaliação?
9. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do restaurante com a maior média de avaliação?
10. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do restaurante com a menor média de avaliação?
11. Qual o tipo de culinária que possui o maior valor médio de um prato para duas pessoas?
12. Qual o tipo de culinária que possui a maior nota média?
13. Qual o tipo de culinária que possui mais restaurantes que aceitam pedidos online e fazem entregas?

## 2. Premissas Assumidas para a Análise:
1. A análise foi realizada após a limpeza de dados do Dataframe fornecido, a qual resultou em 6.927 restaurantes cadastrados na plataforma dentre 163 tipos de culinárias distintos, e dentro de 125 cidades espalhadas por 15 países.
2. O modelo de negócio assumido foi o de Marketplace de Restaurantes.
3. Os restaurantes fazem o cadastro dentro da plataforma da Fome Zero, que disponibiliza
informações como endereço, tipo de culinária servida, se possui reservas, se faz
entregas e também uma nota de avaliação dos serviços e produtos do restaurante,
entre outras informações.

## 3. Estratégia da solução:
O painel estratégico foi desenvolvido utilizando as métricas que refletem os três principais grupos de visões do modelo de negócio da empresa:

1. Visão por Países
2. Visão por Cidades
3. Visão por Tipo de Culinária

Cada visão é representada pelo seguinte conjunto de métricas:

1. Visão por Países:
   
   a. Quantidade de Restaurantes Registrados por País.
   
   b. Quantidade de Cidades Registradas por País.
   
   c. Média de Avaliações dos Restaurantes por País.
   
   d. Média do Preço de Prato para duas pessoas por País.
   
2. Visão por Cidades:
   
   a. Cidades com mais Restaurantes Cadastrados.
   
   b. Cidades com mais avaliações acima de 4 pontos de média.
   
   c. Cidades com mais avaliações abaixo de 2.5 pontos de média.
   
   d. Cidades com mais Restaurantes de diferentes Tipos de Culinária.

3. Visão por Tipo de Culinária:
   
   a. Restaurantes mais bem avaliados dos 5 principais tipos de culinária.
   
   b. Melhores restaurantes entre os tipos de culinária.
   
   c. Melhores Tipos de Culinárias de acordo com as notas de avaliação.
   
   d. Piores Tipos de Culinárias de acordo com as notas de avaliação.

## 4. Top 3 Insights dos dados

1. Apesar da Indonésia ter apenas 80 restaurantes registrados no marketplace, ela possui a principal média de número de avaliações, revelando que os usuários de lá são bem engajados com a avaliação dos restaurantes. De forma contrária, o Brasil possui um relevante número de restaurantes registrados na plataforma (239), mas possui a média de número de avaliações mais baixa entre os países, mostrando um baixo engajamento dos usuários brasileiros da empresa.
   
2.  Dentre os principais tipos de culinária os restaurantes com culinárias Japonesa, Italiana e Americana são os mais bem avaliados pelos usuários da plataforma.

3. Cidades da Inglaterra, Qatar, Estados Unidos, Canadá, Austrália e Brasil são as que mais possuem restaurantes com tipos de culinária únicos, revelando que nesses países existe uma diversidade cultural bastante presente. Pode-se destacar cidades como Londres, Doha, Houston, Montreal, Perth e Brasil.
   
## 5. O produto final do projeto
Painel online, hospedado em um Cloud e disponível para acesso em qualquer dispositivo conectado à internet. O painel pode ser acessado através do link: https://fomezeroproject-renatocortez.streamlit.app

## 6. Conclusão
O objetivo desse projeto é criar um conjunto de gráficos e tabelas que exibam essas métricas da melhor forma possível para o CEO.
Da visão da Empresa, podemos concluir que países como Índia, Estados Unidos, Inglaterra, África do Sul já possuem um número relevante de restaurantes cadastrados revelando um crescimento notável da empresa nessas localidades. 

Outros países como o Brasil e Nova Zelândia possuem um número grande de restaurantes, mas pouca quantidade de registro de média de avaliações, algo que precisa ser trabalhado melhor pela empresa para gerar um maior engajamento dos usuários dessas localidades e permitindo um crescimento sustentável da empresa.

## 7. Próximo passos:
1. Reduzir o número de métricas.
2. Criar novos filtros.
3. Adicionar novas visões de negócio.





