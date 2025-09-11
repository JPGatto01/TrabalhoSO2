# Classe que representa um arquivo no sistema
class Arquivo:
    def __init__(self, nome, tamanho, metodo, blocos, bloco_indice=None):
        # Inicializa os atributos do arquivo: nome, tamanho, método de alocação, blocos ocupados e bloco índice (se indexada)
        self.nome, self.tamanho, self.metodo = nome, tamanho, metodo
        self.blocos, self.bloco_indice = blocos, bloco_indice

# Classe que representa o disco, composto por blocos
class Disco:
    def __init__(self, tamanho):
        self.tamanho = tamanho  # Tamanho total do disco (quantidade de blocos)
        self.blocos = [None] * tamanho  # Lista de blocos, inicialmente todos livres (None)

    # Retorna lista dos índices dos blocos livres
    def livres(self): return [i for i, b in enumerate(self.blocos) if b is None]
    # Retorna lista dos índices dos blocos ocupados
    def ocupados(self): return [i for i, b in enumerate(self.blocos) if b is not None]

# Classe principal do sistema de arquivos
class SistemaArquivos:
    def __init__(self, tamanho, metodo):
        self.disco = Disco(tamanho)  # Cria o disco com o tamanho informado
        self.metodo = metodo         # Método de alocação escolhido
        self.diretorio = {}          # Diretório: dicionário de arquivos criados
