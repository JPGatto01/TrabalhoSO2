Simulador de Sistema de Arquivos - Sistemas Operacionais II
-----------------------------------------------------------
-----------------------------------------------------------
Integrantes da Dupla: João Paulo Gatto de Oliveira - 202553  /  Augusto Rosa - 200849
-------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------
Descrição do Projeto
---------------------
Esse projeto foi desenvolvido como parte da disciplina Sistemas Operacionais II, com o objetivo de simular os principais métodos de alocação de arquivos em sistemas de arquivos.
A ideia é o simulador permitir que os usuários compreendam, de forma prática, como os sistemas operacionais gerenciam o espaço em disco e organizam arquivos.
Todo o funcionamento ocorre via terminal, proporcionando interação direta com menus e comandos digitados.
-------------------------------------------------------------------------
O programa oferece a criação de um disco virtual, no qual o usuário pode criar arquivos, estender arquivos existentes, deletar arquivos, ler arquivos, visualizando a ordem
de acesso aos blocos, exibir o diretório de arquivos e exibir o estado atual do disco (blocos livres e ocupados.
---------------------------------------------------------
---------------------------------------------------------
Além disso, ele demonstra na prática as diferenças entre os métodos de alocação, permitindo observar questões como fragmentação, tempo de acesso simulado e falhas de alocação.
---------------------------------------------------------
---------------------------------------------------------
Métodos de Alocação Implementados
---------------------------------
O simulador implementa três métodos clássicos de alocação de arquivos:
---------------------------------
Alocação Contígua: Os arquivos ocupam blocos sequenciais no disco.
Caso não haja um espaço contíguo suficiente, a alocação falha.
---------------------------------
Alocação Encadeada: Cada arquivo é armazenado em blocos espalhados, com cada bloco apontando para o próximo.
Não exige espaço contínuo.
---------------------------------
Alocação Indexada: Cada arquivo possui um bloco de índice que lista os blocos ocupados.
Permite acesso direto a qualquer parte do arquivo.
---------------------------------
---------------------------------
Linguagem e Tipo de Interface
---------------------------------
Linguagem de Programação: Python
---------------------------------
Versão utilizada: 3.13.7
---------------------------------
Interface do Usuário: Terminal
---------------------------------
Instruções de Compilação e Execução
---------------------------------
Também pode ser rodado no terminal do Visual Studio Code
---------------------------------
Verifique se o Python está instalado: 
---------------------------------
Para verificar, execute no terminal:
---------------------------------
python --version
---------------------------------
Baixe ou clone este repositório 
git clone https://github.com/JPGatto01/TrabalhoSO2
---------------------------------
Acesse a pasta do projeto:  
cd TrabalhoSO2
---------------------------------
Execute o programa: 
python TrabalhoSO.py
---------------------------------
Siga as instruções no terminal para configurar: 
---------------------------------
O tamanho do disco (em blocos).
---------------------------------
O método de alocação desejado.
---------------------------------
E realizar as operações disponíveis no menu.
---------------------------------
---------------------------------
Dependências: 
---------------------------------
Utilizamos apenas a biblioteca math do python.
---------------------------------
---------------------------------
Decisões de Projeto e Arquitetura: 
---------------------------------
O sistema foi projetado com foco na organização modular e na clareza do código. Abaixo estão os principais componentes e suas funções:
---------------------------------
---------------------------------
Estrutura Principal
---------------------------------
Explicação detalhada das funções do Simulador de Sistema de Arquivos
---------------------------------
---------------------------------
Classe Arquivo
---------------------------------
---------------------------------
Representa um arquivo do sistema.
---------------------------------
__init__(self, nome, tamanho, metodo, blocos, bloco_indice=None, frag_interna=0)
Inicializa um objeto Arquivo com os seguintes passos:
---------------------------------
Armazena o nome do arquivo.
---------------------------------
Guarda o tamanho em KB.
---------------------------------
Define o método de alocação usado.
---------------------------------
Guarda os blocos ocupados no disco.
---------------------------------
Para arquivos indexados, guarda o bloco de índice.
---------------------------------
Calcula a fragmentação interna (espaço não utilizado no último bloco).
---------------------------------
---------------------------------
Classe Disco
---------------------------------
---------------------------------
Representa o disco físico com blocos.
---------------------------------
__init__(self, tamanho)
Cria um disco com tamanho blocos, todos inicialmente livres (None).
---------------------------------
livres(self)
Retorna uma lista com os índices de blocos livres no disco usando uma compreensão de lista.
---------------------------------
ocupados(self)
Retorna uma lista com os índices de blocos ocupados, também usando compreensão de lista.
---------------------------------
---------------------------------
Classe SistemaArquivos
__init__(self, tamanho, metodo, bloco_tam=4)
---------------------------------
---------------------------------
Cria o disco chamando Disco(tamanho).
---------------------------------
Define o método de alocação (metodo).
---------------------------------
Inicializa o diretório como um dicionário vazio.
---------------------------------
Define o tamanho de cada bloco (bloco_tam), padrão 4 KB.
---------------------------------
---------------------------------
criar_arquivo(self, nome, tamanho)
---------------------------------
---------------------------------
Verificação inicial: Confere se o arquivo já existe ou se o tamanho é inválido.
---------------------------------
Calcula blocos necessários:
---------------------------------
blocos_necessarios = math.ceil(tamanho / self.bloco_tam)
frag_interna = blocos_necessarios * self.bloco_tam - tamanho
---------------------------------
Usa math.ceil para arredondar para cima, garantindo que haja blocos suficientes.
---------------------------------
Escolhe o método de alocação:
---------------------------------
Contígua → _contigua(blocos_necessarios)
---------------------------------
Encadeada → _encadeada(blocos_necessarios)
---------------------------------
Indexada → _indexada(blocos_necessarios)
---------------------------------
Aloca os blocos no disco:
---------------------------------
Para indexada, separa bloco de índice e blocos de dados.
---------------------------------
Para os outros métodos, marca os blocos como ocupados com o nome do arquivo.
---------------------------------
Cria o objeto Arquivo e adiciona ao diretório.
---------------------------------
Exibe informações sobre blocos ocupados e fragmentação interna.
---------------------------------
---------------------------------
estender_arquivo(self, nome, extra_kb)
---------------------------------
---------------------------------
Aumenta o tamanho de um arquivo existente.
---------------------------------
Verifica validade: arquivo existe e tamanho extra > 0.
---------------------------------
Calcula blocos adicionais necessários e nova fragmentação interna.
---------------------------------
Aloca blocos extras:
---------------------------------
Contígua → tenta encontrar blocos contínuos após os atuais.
---------------------------------
Encadeada / Indexada → pega qualquer bloco livre.
---------------------------------
Atualiza o arquivo: adiciona novos blocos, aumenta o tamanho e ajusta a fragmentação interna.
---------------------------------
Exibe os blocos adicionados e a nova fragmentação.
---------------------------------
---------------------------------
deletar_arquivo(self, nome)
---------------------------------
---------------------------------
Remove um arquivo do sistema:
---------------------------------
Remove o arquivo do diretório (pop).
---------------------------------
Libera todos os blocos que estavam ocupados pelo arquivo.
---------------------------------
Para indexada, libera também o bloco de índice.
---------------------------------
Mostra mensagem confirmando exclusão.
---------------------------------
---------------------------------
ler_arquivo(self, nome)
---------------------------------
---------------------------------
Simula leitura de arquivo:
---------------------------------
Verifica se o arquivo existe.
---------------------------------
Mostra o método de alocação e os blocos acessados:
---------------------------------
Contígua → blocos sequenciais, acesso rápido.
---------------------------------
Encadeada → mostra o encadeamento, acesso mais lento.
---------------------------------
Indexada → mostra bloco índice e blocos de dados, acesso intermediário.
---------------------------------
---------------------------------
exibir_diretorio(self)
---------------------------------
---------------------------------
Lista todos os arquivos no diretório:
---------------------------------
Para cada arquivo, mostra:
---------------------------------
Nome, tamanho, blocos ocupados.
---------------------------------
Para indexada, também exibe bloco índice.
---------------------------------
Fragmentação interna em KB.
---------------------------------
---------------------------------
exibir_disco(self)
---------------------------------
---------------------------------
Mostra o estado do disco:
---------------------------------
Percorre todos os blocos e imprime o nome do arquivo que está ocupando ou "LIVRE".
---------------------------------
Mostra o total de blocos livres e ocupados.
---------------------------------
---------------------------------
Métodos privados de alocação
---------------------------------
---------------------------------
_contigua(self, t)
---------------------------------
Procura t blocos livres consecutivos:
---------------------------------
Percorre o disco, verifica sequências de t blocos.
---------------------------------
Retorna lista de índices se encontrados, ou None caso contrário.
---------------------------------
---------------------------------
_encadeada(self, t)
---------------------------------
---------------------------------
Procura t blocos livres em qualquer posição:
---------------------------------
Retorna os primeiros t blocos livres, ou None se não houver.
---------------------------------
---------------------------------
_indexada(self, t)
---------------------------------
---------------------------------
Aloca 1 bloco para índice e t blocos para dados:
---------------------------------
Retorna (bloco_indice, blocos_dados).
---------------------------------
Retorna None se não houver blocos suficientes.
---------------------------------
---------------------------------
Função auxiliar: menu()
---------------------------------
---------------------------------
Mostra opções disponíveis no console:
---------------------------------
Criar, estender, deletar, ler arquivos, exibir diretório, exibir disco ou sair.
---------------------------------
---------------------------------
Estrutura de Pastas do Projeto
---------------------------------
TrabalhoSO2/
│
├── TrabalhoSO.py   # Código principal do simulador
├── README.md       # Documentação do projeto
---------------------------------
---------------------------------
Funcionalidades do Simulador
---------------------------------
Criar arquivo:	cria um novo arquivo, alocando blocos conforme o método escolhido.
---------------------------------
Estender arquivo:	aumenta o tamanho de um arquivo já existente, se houver espaço disponível.
---------------------------------
Deletar arquivo:	remove o arquivo e libera seus blocos no disco.
---------------------------------
Ler arquivo:	mostra a sequência de acesso aos blocos do arquivo.
---------------------------------
Exibir diretório:	lista todos os arquivos com detalhes de tamanho e blocos ocupados.
---------------------------------
Exibir disco:	mostra visualmente quais blocos estão livres ou ocupados.
---------------------------------
Sair:	encerra o simulador.
---------------------------------
Teste com entrada e saída esperada (1 para cada método de alocação)
-------------------------------------------------------------------
-------------------------------------------------------------------
ALOCAÇÃO CONTÍGUA
---------------------------------
Tamanho do disco = 10
---------------------------------
Método = 1
---------------------------------
Opção 1 (Criar)
---------------------------------
Nome: teste
---------------------------------
Tamanho do arquivo (KB): 8
---------------------------------
Resultado esperado: Arquivo 'teste' criado (Alocação Contígua): blocos [0, 1], frag interna: 0 KB
-------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------
ALOCAÇÃO ENCADEADA
---------------------------------
Tamanho do disco = 10
---------------------------------
Método = 2
---------------------------------
Opção 1 (Criar)
---------------------------------
Nome: teste
---------------------------------
Tamanho do arquivo (KB): 8
---------------------------------
Resultado esperado: Arquivo 'teste' criado (Alocação Encadeada): blocos [0, 1], frag interna: 0 KB
--------------------------------------------------------------------------------------------------
Opção 4 (Ler)
---------------------------------
Nome: teste
---------------------------------
Resultado esperado: Encadeamento: 0 -> 1 -> FIM | Acesso: lento
-------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------
ALOCAÇÃO INDEXADA
---------------------------------
Tamanho do disco = 10
---------------------------------
Método = 3
---------------------------------
Opção 1 (Criar)
---------------------------------
Nome: teste
---------------------------------
Tamanho do arquivo (KB): 8
---------------------------------
Resultado esperado: Arquivo 'teste' criado (Alocação Indexada): blocos [1, 2], frag interna: 0 KB
---------------------------------
Opção 5 (Exibir Diretório)
---------------------------------
Resultado esperado: teste | 8KB | índice 0 | [1, 2] | frag interna: 0 KB            
------------------------------------------------------------------------
------------------------------------------------------------------------
                           
