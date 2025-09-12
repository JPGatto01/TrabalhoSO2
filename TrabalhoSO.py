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

# Cria um novo arquivo no sistema
    def criar_arquivo(self, nome, tamanho):
        # Verifica se o arquivo já existe ou tamanho inválido
        if nome in self.diretorio or tamanho <= 0:
            print("Arquivo já existe ou tamanho inválido."); return
        m = self.metodo
        # Seleciona o método de alocação
        if m == "Alocacao Contigua": blocos = self._contigua(tamanho)
        elif m == "Alocacao Encadeada": blocos = self._encadeada(tamanho)
        elif m == "Alocacao Indexada": blocos = self._indexada(tamanho)
        else: print("Método desconhecido."); return
        # Se não conseguiu alocar, informa falha
        if not blocos: print("Falha na alocação."); return
        # Para indexada, separa bloco índice e blocos de dados
        if m == "Alocacao Indexada":
            idx, dados = blocos
            self.disco.blocos[idx] = nome + "_indice"  # Marca bloco índice
            for b in dados: self.disco.blocos[b] = nome  # Marca blocos de dados
            arq = Arquivo(nome, tamanho, m, dados, idx)  # Cria arquivo
        else:
            for b in blocos: self.disco.blocos[b] = nome  # Marca blocos ocupados
            arq = Arquivo(nome, tamanho, m, blocos)       # Cria arquivo
        self.diretorio[nome] = arq  # Adiciona ao diretório
        print(f"Arquivo '{nome}' criado ({m}): {arq.blocos if m!='Alocacao Indexada' else f'índice {idx}, dados {dados}'}")

    # Estende um arquivo existente, aumentando seu tamanho
    def estender_arquivo(self, nome, extra):
        arq = self.diretorio.get(nome)  # Busca arquivo no diretório
        if not arq or extra <= 0: print("Arquivo não existe ou tamanho inválido."); return
        m = arq.metodo
        if m == "Alocacao Contigua":
            # Só pode estender se houver espaço contíguo após o último bloco
            ult = arq.blocos[-1]
            novos = [ult+i for i in range(1, extra+1) if ult+i < self.disco.tamanho and self.disco.blocos[ult+i] is None]
            if len(novos) != extra: print("Falha: não há espaço contíguo."); return
        else:
            # Para encadeada e indexada, pega blocos livres quaisquer
            livres = self.disco.livres()
            if len(livres) < extra: print("Falha: não há blocos livres."); return
            novos = livres[:extra]
        for b in novos: self.disco.blocos[b] = nome  # Marca novos blocos ocupados
        arq.blocos += novos                          # Adiciona aos blocos do arquivo
        arq.tamanho += extra                         # Atualiza tamanho
        print(f"Arquivo '{nome}' estendido ({m}): novos blocos {novos}")

    # Deleta um arquivo, liberando seus blocos
    def deletar_arquivo(self, nome):
        arq = self.diretorio.pop(nome, None)  # Remove do diretório
        if not arq: print("Arquivo não existe."); return
        for b in arq.blocos: self.disco.blocos[b] = None  # Libera blocos ocupados
        if arq.metodo == "Alocacao Indexada" and arq.bloco_indice is not None:
            self.disco.blocos[arq.bloco_indice] = None    # Libera bloco índice
        print(f"Arquivo '{nome}' deletado.")

    # Lê um arquivo, mostrando os blocos acessados e tempo de acesso simulado
    def ler_arquivo(self, nome):
        arq = self.diretorio.get(nome)
        if not arq: print("Arquivo não existe."); return
        m = arq.metodo
        print(f"Lendo '{nome}':")
        if m == "Alocacao Contigua": print("Blocos:", arq.blocos, "| Acesso: rápido")
        elif m == "Alocacao Encadeada": print("Blocos:", arq.blocos, "| Acesso: lento")
        elif m == "Alocacao Indexada": print(f"Índice: {arq.bloco_indice} | Blocos: {arq.blocos} | Acesso: intermediário")

    # Exibe o diretório de arquivos no terminal
    def exibir_diretorio(self):
        print("\n--- Diretório ---")
        for a in self.diretorio.values():
            if a.metodo == "Alocacao Indexada":
                print(f"{a.nome} | {a.tamanho} | índice {a.bloco_indice} | {a.blocos}")
            else:
                ini = a.blocos[0] if a.blocos else "-"
                print(f"{a.nome} | {a.tamanho} | {ini} | {a.blocos}")
    
    # Exibe o estado atual do disco (blocos livres e ocupados)
    def exibir_disco(self):
        print("\n--- Disco ---")
        print(" ".join(f"[{i}:{b if b else 'LIVRE'}]" for i, b in enumerate(self.disco.blocos) ))
        print(f"Livres: {len(self.disco.livres())} | Ocupados: {len(self.disco.ocupados())}")