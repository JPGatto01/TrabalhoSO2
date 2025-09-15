import math

# Classe que representa um arquivo no sistema
class Arquivo:
    def __init__(self, nome, tamanho, metodo, blocos, bloco_indice=None, frag_interna=0):
        # Inicializa os atributos do arquivo: nome, tamanho, método de alocação, blocos ocupados e bloco índice (se indexada)
        self.nome, self.tamanho, self.metodo = nome, tamanho, metodo
        self.blocos, self.bloco_indice = blocos, bloco_indice
        self.frag_interna = frag_interna  # Fragmentação interna em KB

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
    def __init__(self, tamanho, metodo, bloco_tam=4):
        self.disco = Disco(tamanho)  # Cria o disco com o tamanho informado
        self.metodo = metodo         # Método de alocação escolhido
        self.diretorio = {}  
        self.bloco_tam = bloco_tam   # Diretório: dicionário de arquivos criados

# Cria um novo arquivo no sistema
    def criar_arquivo(self, nome, tamanho):
        # Verifica se o arquivo já existe ou tamanho inválido
        if nome in self.diretorio or tamanho <= 0:
            print("Arquivo já existe ou tamanho inválido."); return
        m = self.metodo

        blocos_necessarios = math.ceil(tamanho / self.bloco_tam)
        frag_interna = blocos_necessarios * self.bloco_tam - tamanho

        # Seleciona o método de alocação
        if m == "Alocação Contígua": blocos = self._contigua(blocos_necessarios)
        elif m == "Alocação Encadeada": blocos = self._encadeada(blocos_necessarios)
        elif m == "Alocação Indexada": blocos = self._indexada(blocos_necessarios)
        # Se não conseguiu alocar, informa falha
        if not blocos: print("Falha na alocação."); return
        # Para indexada, separa bloco índice e blocos de dados
        if m == "Alocação Indexada":
            idx, dados = blocos
            self.disco.blocos[idx] = nome + "_indice"  # Marca bloco índice
            for b in dados: self.disco.blocos[b] = nome  # Marca blocos de dados
            arq = Arquivo(nome, tamanho, m, dados, idx, frag_interna)  # Cria arquivo
        else:
            for b in blocos: self.disco.blocos[b] = nome  # Marca blocos ocupados
            arq = Arquivo(nome, tamanho, m, blocos, frag_interna=frag_interna)       # Cria arquivo
        self.diretorio[nome] = arq  # Adiciona ao diretório
        print(f"Arquivo '{nome}' criado ({m}): blocos {arq.blocos}, frag interna: {frag_interna} KB")

    # Estende um arquivo existente, aumentando seu tamanho
    def estender_arquivo(self, nome, extra_kb):
        arq = self.diretorio.get(nome)
        if not arq or extra_kb <= 0: 
            print("Arquivo não existe ou tamanho inválido."); 
            return

        # Calcula blocos necessários e fragmentação interna nova
        blocos_necessarios = math.ceil(extra_kb / self.bloco_tam)
        frag_interna = blocos_necessarios * self.bloco_tam - extra_kb

        m = arq.metodo
        if m == "Alocação Contígua":
            ult = arq.blocos[-1]
            novos = [ult+i for i in range(1, blocos_necessarios+1) 
                     if ult+i < self.disco.tamanho and self.disco.blocos[ult+i] is None]
            if len(novos) != blocos_necessarios: 
                print("Falha: não há espaço contíguo."); 
                return
        else:
            livres = self.disco.livres()
            if len(livres) < blocos_necessarios: 
                print("Falha: não há blocos livres."); 
                return
            novos = livres[:blocos_necessarios]

        for b in novos: self.disco.blocos[b] = nome
        arq.blocos += novos
        arq.tamanho += extra_kb
        arq.frag_interna = frag_interna  # Atualiza fragmentação interna
        print(f"Arquivo '{nome}' estendido ({m}): novos blocos {novos}, frag interna: {frag_interna} KB")

    # Lê um arquivo, mostrando os blocos acessados e tempo de acesso simulado
    def ler_arquivo(self, nome):
        arq = self.diretorio.get(nome)
        if not arq: print("Arquivo não existe."); return
        m = arq.metodo
        print(f"Lendo '{nome}':")
        if m == "Alocação Contígua": print("Blocos:", arq.blocos, "| Acesso: rápido")
        elif m == "Alocação Encadeada": 
            cadeia = " -> ".join(str(b) for b in arq.blocos) + " -> FIM"
            print("Encadeamento:", cadeia, "| Acesso: lento")
        elif m == "Alocação Indexada": print(f"Índice: {arq.bloco_indice} | Blocos: {arq.blocos} | Acesso: intermediário")

    # Exibe o diretório de arquivos no terminal
    def exibir_diretorio(self):
        print("\n--- Diretório ---")
        for a in self.diretorio.values():
            if a.metodo == "Alocação Indexada":
                print(f"{a.nome} | {a.tamanho}KB | índice {a.bloco_indice} | {a.blocos} | frag interna: {a.frag_interna} KB")
            else:
                ini = a.blocos[0] if a.blocos else "-"
                print(f"{a.nome} | {a.tamanho}KB | {ini} | {a.blocos} | frag interna: {a.frag_interna} KB")
    
    # Exibe o estado atual do disco (blocos livres e ocupados)
    def exibir_disco(self):
        print("\n--- Disco ---")
        print(" ".join(f"[{i}:{b if b else 'LIVRE'}]" for i, b in enumerate(self.disco.blocos) ))
        print(f"Livres: {len(self.disco.livres())} | Ocupados: {len(self.disco.ocupados())}")

     # Alocação contígua: busca espaço sequencial livre
    def _contigua(self, t):
        for i in range(self.disco.tamanho - t + 1):
            if all(self.disco.blocos[j] is None for j in range(i, i + t)):
                return list(range(i, i + t))
        return None

    # Alocação encadeada: pega qualquer bloco livre
    def _encadeada(self, t):
        livres = self.disco.livres()
        return livres[:t] if len(livres) >= t else None

    # Alocação indexada: um bloco para índice, o resto para dados
    def _indexada(self, t):
        livres = self.disco.livres()
        return (livres[0], livres[1:t+1]) if len(livres) >= t+1 else None
    
# Função para exibir o menu de opções
def menu():
    print("\n--- Simulador SO2 ---")
    print("1- Criar 2- Estender 3- Deletar 4- Ler 5- Exibir Diretório 6- Exibir Disco 0- Sair")

# Ponto de entrada do programa
if __name__ == "__main__":
    tam = int(input("Tamanho do disco: "))
    m = input("Método (1- Alocação Contígua 2- Alocação Encadeada 3- Alocação Indexada): ")
    metodo = {"1": "Alocação Contígua", "2": "Alocação Encadeada", "3": "Alocação Indexada"}.get(m, "Alocação Contígua") # Traduz opção
    so2 = SistemaArquivos(tam, metodo) # Cria sistema de arquivos
    while True:
        if(m != "1" and m != "2" and m != "3"):
            print("Método inválido. ")
            break
        menu()
        print("Método escolhido:", metodo)
        op = input("Opção: ")  # Solicita opção do usuário
        if op == "1":
            nome = input("Nome: "); t = int(input("Tamanho do arquivo (KB): "))
            so2.criar_arquivo(nome, t)
        elif op == "2":
            nome = input("Nome: "); t = int(input("Extra (KB): "))
            so2.estender_arquivo(nome, t)
        elif op == "3":
            so2.deletar_arquivo(input("Nome: "))
        elif op == "4":
            so2.ler_arquivo(input("Nome: "))
        elif op == "5":
            so2.exibir_diretorio()
        elif op == "6":
            so2.exibir_disco()
        elif op == "0":
            break
