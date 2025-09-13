Simulador de Sistema de Arquivos - Sistemas Operacionais II

Integrantes da Dupla: João Paulo Gatto de Oliveira - 202553  /  Augusto Rosa - 200849

Descrição do Projeto
Esse projeto foi desenvolvido como parte da disciplina Sistemas Operacionais II, com o objetivo de simular os principais métodos de alocação de arquivos em sistemas de arquivos.
A ideia é o simulador permitir que os usuários compreendam, de forma prática, como os sistemas operacionais gerenciam o espaço em disco e organizam arquivos.
Todo o funcionamento ocorre via terminal, proporcionando interação direta com menus e comandos digitados.

O programa oferece a criação de um disco virtual, no qual o usuário pode:
Criar arquivos;
Estender arquivos existentes;
Deletar arquivos;
Ler arquivos, visualizando a ordem de acesso aos blocos;
Exibir o diretório de arquivos;
Exibir o estado atual do disco (blocos livres e ocupados).

Além disso, ele demonstra na prática as diferenças entre os métodos de alocação, permitindo observar questões como fragmentação, tempo de acesso simulado e falhas de alocação.

Métodos de Alocação Implementados
O simulador implementa três métodos clássicos de alocação de arquivos:

Alocação Contígua: Os arquivos ocupam blocos sequenciais no disco.
Caso não haja um espaço contíguo suficiente, a alocação falha.

Alocação Encadeada: Cada arquivo é armazenado em blocos espalhados, com cada bloco apontando para o próximo.
Não exige espaço contínuo.

Alocação Indexada: Cada arquivo possui um bloco de índice que lista os blocos ocupados.
Permite acesso direto a qualquer parte do arquivo.

Linguagem e Tipo de Interface

Linguagem de Programação: Python
Versão recomendada: Python 3.10 ou superior
Interface do Usuário: Terminal

Instruções de Compilação e Execução

Verifique se o Python está instalado
Para verificar, execute no terminal:
python --version
É necessário ter Python 3.10 ou superior.

Baixe ou clone este repositório
git clone //repositorio

Acesse a pasta do projeto
cd TrabalhoSO2

Execute o programa
python TrabalhoSO.py

Siga as instruções no terminal para configurar:
O tamanho do disco (em blocos).
O método de alocação desejado.
E realizar as operações disponíveis no menu.

Dependências
Este projeto não requer instalação de bibliotecas externas, utilizando apenas módulos nativos do Python.

Decisões de Projeto e Arquitetura
O sistema foi projetado com foco na organização modular e na clareza do código. Abaixo estão os principais componentes e suas funções:

Estrutura Principal
Classe Arquivo
Representa um arquivo no sistema, armazenando informações como:
Nome do arquivo
Tamanho (em blocos)
Método de alocação utilizado
Lista de blocos ocupados
Bloco de índice (se aplicável para alocação indexada)

Classe Disco
Representa o disco virtual, contendo:
Lista de blocos (None = livre, nome do arquivo = ocupado)
Métodos para retornar blocos livres e ocupados.

Classe SistemaArquivos
Responsável por gerenciar os arquivos e blocos, implementando as funcionalidades principais:
Criar arquivos (criar_arquivo)
Estender arquivos (estender_arquivo)
Deletar arquivos (deletar_arquivo)
Ler arquivos (ler_arquivo)
Exibir diretório (exibir_diretorio)
Exibir estado do disco (exibir_disco)
Função menu()
Exibe as opções de interação no terminal.

Bloco principal (if __name__ == "__main__":)
Inicia o programa, solicita as configurações iniciais e gerencia o fluxo de execução.

Estrutura de Pastas do Projeto
TrabalhoSO2/
│
├── TrabalhoSO.py   # Código principal do simulador
├── README.md                  # Documentação do projeto

Funcionalidades do Simulador
Função	Descrição
Criar arquivo	Cria um novo arquivo, alocando blocos conforme o método escolhido.
Estender arquivo	Aumenta o tamanho de um arquivo já existente, se houver espaço disponível.
Deletar arquivo	Remove o arquivo e libera seus blocos no disco.
Ler arquivo	Mostra a sequência de acesso aos blocos do arquivo.
Exibir diretório	Lista todos os arquivos com detalhes de tamanho e blocos ocupados.
Exibir estado do disco	Mostra visualmente quais blocos estão livres ou ocupados.
Sair	Encerra o simulador.

