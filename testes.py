import unittest
import subprocess
from TrabalhoSO import Disco, SistemaArquivos

# ---------------------------------------------------------
# 1. TESTES DE UNIDADE
# Foco: Testar partes isoladas do código (Classe Disco).
# ---------------------------------------------------------
class TestDisco(unittest.TestCase):
    
    def setUp(self):
        # Prepara um disco de tamanho 5 antes de cada teste
        self.disco = Disco(5)

    def test_inicializacao_disco(self):
        """Verifica se o disco inicializa com o tamanho correto e totalmente vazio."""
        self.assertEqual(self.disco.tamanho, 5)
        self.assertEqual(self.disco.blocos, [None, None, None, None, None])

    def test_livres_e_ocupados(self):
        """Verifica se os métodos de contagem de blocos livres e ocupados funcionam."""
        self.disco.blocos[0] = "arq_teste"
        self.disco.blocos[1] = "arq_teste"
        
        # Ocupamos 2 blocos, devem sobrar 3 livres
        self.assertEqual(self.disco.ocupados(), [0, 1])
        self.assertEqual(self.disco.livres(), [2, 3, 4])


# ---------------------------------------------------------
# 2. TESTES DE INTEGRAÇÃO
# Foco: Testar o funcionamento conjunto de várias classes 
# (SistemaArquivos, Arquivo e Disco).
# ---------------------------------------------------------
class TestSistemaArquivos(unittest.TestCase):

    def setUp(self):
        # Prepara um sistema de arquivos com alocação contígua e tamanho 10
        self.so = SistemaArquivos(tamanho=10, metodo="Alocação Contígua")

    def test_integracao_criar_e_deletar_arquivo(self):
        """Testa se a criação e deleção refletem no diretório e nos blocos do disco."""
        # Ação: Criar arquivo
        self.so.criar_arquivo("documento", 6) # 6KB usam 2 blocos (tamanho do bloco=4)
        
        # Verificações de criação
        self.assertIn("documento", self.so.diretorio)
        self.assertEqual(len(self.so.disco.ocupados()), 2)
        
        # Ação: Deletar arquivo
        self.so.deletar_arquivo("documento")
        
        # Verificações de deleção
        self.assertNotIn("documento", self.so.diretorio)
        self.assertEqual(len(self.so.disco.ocupados()), 0)
        self.assertEqual(len(self.so.disco.livres()), 10)

    def test_integracao_estender_arquivo(self):
        """Testa o crescimento de um arquivo e o impacto na fragmentação interna."""
        self.so.criar_arquivo("foto", 3) # 3KB usa 1 bloco (sobra 1KB de frag. interna)
        arq = self.so.diretorio["foto"]
        
        self.assertEqual(arq.frag_interna, 1)
        self.assertEqual(len(arq.blocos), 1)

        # Ação: Estender arquivo em mais 5KB (Total = 8KB, vai usar exatos 2 blocos)
        self.so.estender_arquivo("foto", 5)
        
        self.assertEqual(arq.tamanho, 8)
        self.assertEqual(len(arq.blocos), 2)
        self.assertEqual(arq.frag_interna, 0) # Sem desperdício agora


# ---------------------------------------------------------
# 3. TESTES DE SISTEMA (Interface do Usuário / CLI)
# Foco: Simular a sessão de um usuário real digitando 
# comandos no menu do terminal, do começo ao fim.
# ---------------------------------------------------------
class TestSistemaCompletoCLI(unittest.TestCase):

    def test_fluxo_usuario_real(self):
        """Simula entradas de teclado (stdin) e lê as saídas do terminal (stdout)."""
        
        # Sequência de teclas que o usuário digitaria:
        # 10 (tamanho disco) -> 1 (alocação contígua) -> 1 (criar) -> arq1 -> 8 (kb) 
        # -> 6 (exibir disco) -> 3 (deletar) -> arq1 -> 0 (sair)
        entradas_usuario = "10\n1\n1\narq1\n8\n6\n3\narq1\n0\n"
        
        # Executa o script principal como um processo separado
        processo = subprocess.run(
            ['python', 'TrabalhoSO.py'], 
            input=entradas_usuario, 
            text=True, 
            capture_output=True
        )
        
        saida_terminal = processo.stdout

        # Verificamos se as mensagens esperadas apareceram na tela do usuário
        self.assertIn("Arquivo 'arq1' criado", saida_terminal)
        self.assertIn("Ocupados: 2", saida_terminal) # Exibir disco deve mostrar 2 blocos ocupados
        self.assertIn("Arquivo 'arq1' deletado com sucesso", saida_terminal)


if __name__ == '__main__':
    unittest.main(verbosity=2)
