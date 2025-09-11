TRABALHO SISTEMAS OPERACIONAIS 2 - Simulação, Análise e Apresentação de Conceitos Fundamentais de Sistemas Operacionais

Alunos: João Paulo Gatto de Oliveira - 202553 / Augusto Rosa - 200849

Visão Geral 
A ideia é desenvolver o simulador em Python e tem como objetivo demonstrar os principais métodos de alocação de arquivos em sistemas de arquivos: contígua, encadeada e indexada. Toda a interação será feita pelo terminal, através de menus e comandos digitados pelo usuário.

Estrutura do Sistema Nossa ideia é o sistema funcionar com base em três partes principais:

Configuração inicial: 
O usuário informa o tamanho do disco (em blocos). Escolhe o método de alocação (contígua, encadeada ou indexada). Operações disponíveis: Criar arquivo: informar nome e tamanho. O simulador tenta alocar os blocos seguindo o método escolhido. Estender arquivo: aumentar o tamanho de um arquivo já existente, se houver espaço disponível. Deletar arquivo: liberar os blocos ocupados pelo arquivo. Ler arquivo: mostrar a ordem em que os blocos são acessados (sequencial ou aleatório, dependendo do método). Tabela de Diretório: Exibir no terminal como uma lista com nome, tamanho, bloco inicial (se aplicável) e blocos alocados. Representação dos Métodos

Contígua: 
os arquivos serão alocados em blocos sequenciais. Se não houver espaço contínuo, a operação falha.

Encadeada: 
cada arquivo deverá ser representado como uma lista de blocos ligados por ponteiros. O diretório guarda apenas o primeiro bloco.

Indexada: 
cada arquivo vai possuir um bloco de índice que lista os blocos de dados. No terminal, os blocos do disco serão exibidos como uma sequência numerada, com marcações indicando quais pertencem a cada arquivo.

Métricas e Resultados Ao longo do uso, o sistema poderá exibir:

Fragmentação: quando não é possível alocar arquivos de forma contígua. 
Blocos livres e ocupados: situação atual do disco. 
Tempo de acesso (simulado): mostrando diferenças entre métodos (ex.: contígua mais rápida em acesso sequencial, encadeada mais lenta). 
Falhas de alocação: mensagens quando não há espaço suficiente. 
Tecnologias Utilizadas

Linguagem: Python. Execução: programa em modo texto, rodando no terminal. Estruturas: listas e dicionários para representar os blocos do disco e os arquivos no diretório.
