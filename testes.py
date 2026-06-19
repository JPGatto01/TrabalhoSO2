iimport unittest
import subprocess
import io
from unittest.mock import patch
from TrabalhoSO import Disco, SistemaArquivos

# ---------------------------------------------------------
# 1. TESTES DE UNIDADE: Classe Disco
# ---------------------------------------------------------
class TestDisco(unittest.TestCase):
    def setUp(self):
        self.disco = Disco(5)

    def test_inicializacao_disco(self):
        self.assertEqual(self.disco.tamanho, 5)
        self.assertEqual(self.disco.blocos, [None] * 5)

    def test_livres_e_ocupados(self):
        self.disco.blocos[0] = "arq"
        self.assertEqual(self.disco.ocupados(), [0])
        self.assertEqual(self.disco.livres(), [1, 2, 3, 4])


# ---------------------------------------------------------
# 1.1 TESTES DE UNIDADE: Métodos privados de alocação (_contigua, _encadeada, _indexada)
#     Testados isoladamente, sem passar por criar_arquivo, para verificar
#     apenas a lógica de seleção de blocos (classes de equivalência: sucesso e falha)
# ---------------------------------------------------------
class TestMetodosPrivadosAlocacao(unittest.TestCase):
    def setUp(self):
        # O método de alocação do SO não importa aqui, pois chamamos os métodos privados direto
        self.so = SistemaArquivos(tamanho=5, metodo="Alocação Contígua", bloco_tam=4)

    def test_contigua_sucesso(self):
        self.assertEqual(self.so._contigua(3), [0, 1, 2])

    def test_contigua_falha_sem_espaco_sequencial(self):
        # Disco de 5 blocos (0-4). Bloqueando o bloco 2 (meio do disco),
        # não há mais nenhuma sequência livre de 3 blocos consecutivos:
        # livres são 0,1,3,4 -> nenhuma sequência de tamanho 3 é possível.
        self.so.disco.blocos[2] = "x"
        self.assertIsNone(self.so._contigua(3))

    def test_contigua_falha_disco_pequeno(self):
        # Pede mais blocos do que o disco tem
        self.assertIsNone(self.so._contigua(6))

    def test_encadeada_sucesso(self):
        self.so.disco.blocos[0] = "x"
        self.so.disco.blocos[2] = "y"
        # Livres: 1, 3, 4 -> pega os 2 primeiros livres
        self.assertEqual(self.so._encadeada(2), [1, 3])

    def test_encadeada_falha_sem_blocos_livres(self):
        for i in range(5):
            self.so.disco.blocos[i] = "x"
        self.assertIsNone(self.so._encadeada(1))

    def test_indexada_sucesso(self):
        # 5 blocos livres, pede 2 de dados -> precisa de 1 (índice) + 2 (dados) = 3
        idx, dados = self.so._indexada(2)
        self.assertEqual(idx, 0)
        self.assertEqual(dados, [1, 2])

    def test_indexada_falha_sem_espaco_para_indice_e_dados(self):
        # Só há espaço para os dados, mas não para o bloco de índice extra
        for i in range(4):
            self.so.disco.blocos[i] = "x"
        # 1 bloco livre (índice 4); pede 1 bloco de dados -> precisaria de 1+1=2
        self.assertIsNone(self.so._indexada(1))


# ---------------------------------------------------------
# 2. TESTES DE INTEGRAÇÃO: Métodos de Alocação
# ---------------------------------------------------------
class TestAlocacaoContigua(unittest.TestCase):
    def setUp(self):
        self.so = SistemaArquivos(tamanho=10, metodo="Alocação Contígua", bloco_tam=4)

    def test_criar_e_estender_com_sucesso(self):
        self.so.criar_arquivo("a1", 4) # Usa bloco 0
        self.so.estender_arquivo("a1", 4) # Estende para o bloco 1
        self.assertEqual(self.so.diretorio["a1"].blocos, [0, 1])
        self.assertEqual(self.so.diretorio["a1"].tamanho, 8)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_falha_extensao_nao_contigua(self, mock_stdout):
        self.so.criar_arquivo("a1", 4) # Usa bloco 0
        self.so.criar_arquivo("a2", 4) # Usa bloco 1 (bloqueia o a1)
        self.so.estender_arquivo("a1", 4) # Vai tentar estender a1, mas o bloco 1 está ocupado
        self.assertIn("Falha: não há espaço contíguo", mock_stdout.getvalue())

class TestAlocacaoEncadeada(unittest.TestCase):
    def setUp(self):
        self.so = SistemaArquivos(tamanho=5, metodo="Alocação Encadeada", bloco_tam=4)

    def test_criar_e_estender_fragmentado(self):
        # Ocupa blocos específicos para forçar fragmentação
        self.so.disco.blocos[0] = "x"
        self.so.disco.blocos[2] = "y"
        # Livres: 1, 3, 4. 
        self.so.criar_arquivo("a1", 4) # Deve pegar bloco 1
        self.so.estender_arquivo("a1", 8) # Deve pegar blocos 3 e 4
        self.assertEqual(self.so.diretorio["a1"].blocos, [1, 3, 4])

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_ler_arquivo_encadeado(self, mock_stdout):
        self.so.criar_arquivo("a1", 8)  # 2 blocos encadeados
        self.so.ler_arquivo("a1")
        saida = mock_stdout.getvalue()
        self.assertIn("Encadeamento:", saida)
        self.assertIn("-> FIM", saida)
        self.assertIn("Acesso: lento", saida)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_falha_extensao_sem_blocos_livres(self, mock_stdout):
        # Disco de 5 blocos: ocupa todos exceto os usados pelo próprio arquivo
        self.so.criar_arquivo("a1", 4)  # usa 1 bloco, restam 4 livres
        for i in self.so.disco.livres():
            self.so.disco.blocos[i] = "outro"  # ocupa todo o resto do disco
        self.so.estender_arquivo("a1", 4)  # não há bloco livre para estender
        self.assertIn("Falha: não há blocos livres", mock_stdout.getvalue())

class TestAlocacaoIndexada(unittest.TestCase):
    def setUp(self):
        self.so = SistemaArquivos(tamanho=5, metodo="Alocação Indexada", bloco_tam=4)

    def test_criar_e_deletar_limpando_indice(self):
        self.so.criar_arquivo("a1", 4) 
        # Um arquivo de 4KB exige 1 bloco de dados + 1 bloco de índice
        arq = self.so.diretorio["a1"]
        self.assertEqual(arq.bloco_indice, 0) # Bloco 0 vira índice
        self.assertEqual(arq.blocos, [1])     # Bloco 1 vira dados
        
        # Deleta e verifica se tudo foi limpo (inclusive o índice)
        self.so.deletar_arquivo("a1")
        self.assertNotIn("a1", self.so.diretorio)
        self.assertEqual(len(self.so.disco.livres()), 5)

    def test_estender_arquivo_indexado(self):
        # Indexada usa a mesma lógica de "qualquer bloco livre" que a Encadeada na extensão
        self.so.criar_arquivo("a1", 4)  # índice=0, dados=[1]
        self.so.estender_arquivo("a1", 4)  # deve pegar o próximo bloco livre (2)
        self.assertEqual(self.so.diretorio["a1"].blocos, [1, 2])

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_ler_arquivo_indexado(self, mock_stdout):
        self.so.criar_arquivo("a1", 4)
        self.so.ler_arquivo("a1")
        saida = mock_stdout.getvalue()
        self.assertIn("Acesso: intermediário", saida)
        self.assertIn("Índice: 0", saida)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_exibir_diretorio_indexado(self, mock_stdout):
        self.so.criar_arquivo("a1", 4)
        self.so.exibir_diretorio()
        self.assertIn("índice 0", mock_stdout.getvalue())


# ---------------------------------------------------------
# 3. TESTES DE INTEGRAÇÃO: Validações de Erro e Saídas (Prints)
# ---------------------------------------------------------
class TestValidacoesESaidas(unittest.TestCase):
    def setUp(self):
        self.so = SistemaArquivos(10, "Alocação Contígua")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_erros_de_criacao_e_extensao(self, mock_stdout):
        # 1. Arquivo inválido ou duplicado
        self.so.criar_arquivo("a1", 0)
        self.assertIn("tamanho inválido", mock_stdout.getvalue())
        
        self.so.criar_arquivo("a2", 4)
        self.so.criar_arquivo("a2", 4)
        self.assertIn("Arquivo já existe", mock_stdout.getvalue())
        
        # 2. Estender arquivo inexistente
        self.so.estender_arquivo("fantasma", 5)
        self.assertIn("Arquivo não existe", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_disco_cheio(self, mock_stdout):
        self.so.criar_arquivo("gigante", 100) # 100KB requerem mais de 10 blocos
        self.assertIn("Falha na alocação", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_ler_e_exibir_diretorio(self, mock_stdout):
        self.so.criar_arquivo("a1", 4)
        self.so.ler_arquivo("a1")
        self.assertIn("Acesso: rápido", mock_stdout.getvalue())
        
        self.so.exibir_diretorio()
        self.assertIn("--- Diretório ---", mock_stdout.getvalue())
        self.assertIn("a1 |", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_exibir_disco(self, mock_stdout):
        self.so.criar_arquivo("a1", 4)
        self.so.exibir_disco()
        saida = mock_stdout.getvalue()
        self.assertIn("--- Disco ---", saida)
        self.assertIn("LIVRE", saida)
        self.assertIn("Livres: 9", saida)   # 10 blocos - 1 ocupado
        self.assertIn("Ocupados: 1", saida)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_ler_arquivo_inexistente(self, mock_stdout):
        self.so.ler_arquivo("fantasma")
        self.assertIn("Arquivo não existe", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_deletar_arquivo_inexistente(self, mock_stdout):
        self.so.deletar_arquivo("fantasma")
        self.assertIn("Arquivo não existe no diretório", mock_stdout.getvalue())


# ---------------------------------------------------------
# 4. TESTES DE SISTEMA: CLI Completa
# ---------------------------------------------------------
class TestSistemaCompletoCLI(unittest.TestCase):
    def test_fluxo_invalido_e_saida(self):
        """Testa como o sistema lida com um método de alocação inválido logo no início."""
        entradas = "10\n4\n" # 4 não é um método válido. O loop deve quebrar (break).
        proc = subprocess.run(['python', 'TrabalhoSO.py'], input=entradas, text=True, capture_output=True)
        self.assertIn("Método inválido", proc.stdout)

    def test_fluxo_todas_opcoes_menu(self):
        """Passa por todas as opções de 1 a 6 e depois sai no 0."""
        # Tamanho: 10, Método: 2 (Encadeada)
        # 1(Criar) arq1 8KB -> 2(Estender) arq1 4KB -> 4(Ler) arq1 -> 5(Diretório) -> 6(Disco) -> 0(Sair)
        entradas = "10\n2\n1\narq1\n8\n2\narq1\n4\n4\narq1\n5\n6\n0\n"
        proc = subprocess.run(['python', 'TrabalhoSO.py'], input=entradas, text=True, capture_output=True)
        
        saida = proc.stdout
        self.assertIn("Arquivo 'arq1' criado", saida)
        self.assertIn("Arquivo 'arq1' estendido", saida)
        self.assertIn("Encadeamento:", saida)     # Opção 4 (Ler - Encadeada)
        self.assertIn("--- Diretório ---", saida) # Opção 5
        self.assertIn("--- Disco ---", saida)     # Opção 6

    def test_fluxo_criar_e_deletar_pelo_menu(self):
        """Garante que a opção 3 (Deletar) funciona pelo fluxo real da CLI."""
        # Tamanho: 10, Método: 1 (Contígua)
        # 1(Criar) arq1 4KB -> 3(Deletar) arq1 -> 5(Diretório, deve estar vazio) -> 0(Sair)
        entradas = "10\n1\n1\narq1\n4\n3\narq1\n5\n0\n"
        proc = subprocess.run(['python', 'TrabalhoSO.py'], input=entradas, text=True, capture_output=True)

        saida = proc.stdout
        self.assertIn("Arquivo 'arq1' criado", saida)
        self.assertIn("Arquivo 'arq1' deletado com sucesso", saida)
        self.assertIn("--- Diretório ---", saida)

if __name__ == '__main__':
    unittest.main(verbosity=2)
