import dataclasses
import json

# Definição das classes para Livro, Usuário e Empréstimo
@dataclasses.dataclass
# representa um livro na biblioteca
class Livro:
    titulo: str
    autor: str
    isbn: str #é utilizado para diferenciar um livro do outro, mesmo que tenham o mesmo título
    disponivel: bool = True # indica se o livro está disponível para empréstimo

# Definição das classes para Usuário e Empréstimo
@dataclasses.dataclass
# representa um usuário da biblioteca
class Usuario:
    nome: str
    id_usuario: str # ID único do usuário

@dataclasses.dataclass
# representa um empréstimo de livro
class Emprestimo:
    livro: Livro
    usuario: Usuario
    data_emprestimo: int # Representa o dia do empréstimo
    data_devolucao_prevista: int # Representa o dia da devolução prevista
    data_devolucao_efetiva: int = None # Representa o dia da devolução efetiva, inicialmente None
    multa: float = 0.0 # Multa acumulada por atraso na devolução, inicialmente 0.0

class Biblioteca:
    # Classe que gerencia a biblioteca, incluindo livros, usuários e empréstimos
    def __init__(self):
        self.livros = [] # Lista de livros na biblioteca
        self.usuarios = [] # Lista de usuários registrados na biblioteca
        self.emprestimos = [] # Lista de empréstimos realizados
        self.dia_atual_sistema = 1 # Movido para atributo da classe

    def adicionar_livro(self, titulo, autor, isbn):
        # Adiciona um novo livro à biblioteca
        livro = Livro(titulo, autor, isbn) 
        self.livros.append(livro) 
        print(f"Livro \'{titulo}\' adicionado com sucesso.") 

    def listar_livros(self):
        # Lista todos os livros cadastrados na biblioteca
        if not self.livros: # Verifica se a lista de livros está vazia
            print("Nenhum livro cadastrado.")
            return
        print("=== Livros Cadastrados ===")
        for livro in self.livros:  # Percorre a lista de livros
            # Exibe informações do livro, incluindo título, autor, ISBN e status (dispon
            status = "Disponível" if livro.disponivel else "Emprestado"
            print(f"Título: {livro.titulo}, Autor: {livro.autor}, ISBN: {livro.isbn}, Status: {status}") 

    def adicionar_usuario(self, nome, id_usuario):
        # Adiciona um novo usuário à biblioteca
        usuario = Usuario(nome, id_usuario) # Cria um novo objeto Usuario
        self.usuarios.append(usuario) # Adiciona o usuário à lista de usuários
        # Exibe mensagem de sucesso ao adicionar o usuário
        print(f"Usuário \'{nome}\' adicionado com sucesso.")

    def listar_usuarios(self):
        # Lista todos os usuários cadastrados na biblioteca
        if not self.usuarios:
            print("Nenhum usuário cadastrado.")
            return
        print("=== Usuários Cadastrados ===") 
        for usuario in self.usuarios: # Percorre a lista de usuários
            print(f"Nome: {usuario.nome}, ID: {usuario.id_usuario}")

    def realizar_emprestimo(self, isbn_livro, id_usuario, prazo_dias):
        # Realiza o empréstimo de um livro para um usuário
        livro_encontrado = None # Procura o livro pelo ISBN
        for livro in self.livros: # Percorre a lista de livros
            if livro.isbn == isbn_livro and livro.disponivel: # Verifica se o livro está disponível
                # Se o livro for encontrado e estiver disponível, atribui à variável livro_encontrado
                livro_encontrado = livro
                break

        usuario_encontrado = None # procura o usuário pelo ID
        for usuario in self.usuarios: # Percorre a lista de usuários
            if usuario.id_usuario == id_usuario: # Verifica se o ID do usuário corresponde ao ID fornecido
                # Se o usuário for encontrado, atribui à variável usuario_encontrado
                usuario_encontrado = usuario
                break

        if livro_encontrado and usuario_encontrado:
            # see o livro e o usuário forem encontrados, cria um novo empréstimo
            livro_encontrado.disponivel = False #marca o livro como não disponível
            # Define a data de empréstimo e a data de devolução prevista
            data_emprestimo = self.dia_atual_sistema 
            data_devolucao_prevista = self.dia_atual_sistema + prazo_dias # Calcula a data de devolução prevista com base no prazo fornecido
            # Cria um novo objeto Emprestimo e adiciona à lista de empréstimos
            emprestimo = Emprestimo(livro_encontrado, usuario_encontrado, data_emprestimo, data_devolucao_prevista)
            self.emprestimos.append(emprestimo) #adiciona o empréstimo à lista de empréstimos
            print(f"Empréstimo do livro \'{livro_encontrado.titulo}\' para o usuário \'{usuario_encontrado.nome}\' realizado com sucesso.") # Exibe mensagem de sucesso
            print(f"Data de empréstimo: Dia {data_emprestimo}, Data de devolução prevista: Dia {data_devolucao_prevista}") #Exibe informações sobre o empréstimo
        elif not livro_encontrado:
            print(f"Livro com ISBN {isbn_livro} não encontrado ou não disponível.")
        elif not usuario_encontrado:
            print(f"Usuário com ID {id_usuario} não encontrado.")

    def realizar_devolucao(self, isbn_livro, id_usuario):
        # Realiza a devolução de um livro emprestado
        emprestimo_encontrado = None 
        for emprestimo in self.emprestimos:
            if emprestimo.livro.isbn == isbn_livro and emprestimo.usuario.id_usuario == id_usuario and emprestimo.data_devolucao_efetiva is None:
                emprestimo_encontrado = emprestimo
                break

        if emprestimo_encontrado:
            emprestimo_encontrado.livro.disponivel = True
            emprestimo_encontrado.data_devolucao_efetiva = self.dia_atual_sistema

            if emprestimo_encontrado.data_devolucao_efetiva > emprestimo_encontrado.data_devolucao_prevista: # Verifica se houve atraso na devolução
                dias_atraso = emprestimo_encontrado.data_devolucao_efetiva - emprestimo_encontrado.data_devolucao_prevista
                multa_por_dia = 0.5  # Exemplo: R$ 0.50 por dia de atraso
                emprestimo_encontrado.multa = dias_atraso * multa_por_dia
                print(f"Devolução do livro \'{emprestimo_encontrado.livro.titulo}\' realizada com atraso de {dias_atraso} dias. Multa aplicada: R$ {emprestimo_encontrado.multa:.2f}")
            else: # Se não houve atraso, a multa permanece 0
                print(f"Devolução do livro \'{emprestimo_encontrado.livro.titulo}\' realizada com sucesso.")
            print(f"Data de devolução efetiva: Dia {emprestimo_encontrado.data_devolucao_efetiva}")
        else: # Se o empréstimo não for encontrado, exibe mensagem de erro
            print(f"Empréstimo não encontrado para o livro com ISBN {isbn_livro} e usuário com ID {id_usuario}, ou já devolvido.")

    def listar_emprestimos(self): 
        # Lista todos os empréstimos registrados
        if not self.emprestimos: # Lista de empréstimos vazia
            # Se não houver empréstimos, exibe mensagem
            print("Nenhum empréstimo registrado.")
            return
        print("=== Empréstimos Registrados ===")
        for emp in self.emprestimos:
            status = "Ativo" if emp.data_devolucao_efetiva is None else "Concluído"
            multa_info = f", Multa: R$ {emp.multa:.2f}" if emp.multa > 0 else ""
            print(f"Livro: {emp.livro.titulo}, Usuário: {emp.usuario.nome}, Empréstimo: Dia {emp.data_emprestimo}, Devolução Prevista: Dia {emp.data_devolucao_prevista}, Status: {status}{multa_info}")

    def salvar_dados(self, filename="biblioteca_dados.json"):
        # salva os dados da biblioteca em um arquivo JSON
        data = {
            "livros": [livro.__dict__ for livro in self.livros],
            "usuarios": [usuario.__dict__ for usuario in self.usuarios],
            "emprestimos": [],
            "dia_atual_sistema": self.dia_atual_sistema # Salva o dia atual do sistema
        }
        for emp in self.emprestimos:
            # Salva os dados do empréstimo, incluindo apenas o ISBN do livro e o ID do usuário
            emp_data = emp.__dict__.copy()
            emp_data["livro"] = emp.livro.isbn  # Salva apenas o ISBN do livro
            emp_data["usuario"] = emp.usuario.id_usuario  # Salva apenas o ID do usuário
            data["emprestimos"].append(emp_data)

        with open(filename, "w") as f: # Abre o arquivo para escrita
            json.dump(data, f, indent=4) # Salva os dados no formato JSON com indentação de 4 espaços
        # Exibe mensagem de sucesso ao salvar os dados
        print(f"Dados salvos em {filename}")

    def carregar_dados(self, filename="biblioteca_dados.json"):
        #caarrega os dados da biblioteca de um arquivo JSON
        try:
            with open(filename, "r") as f: # Abre o arquivo para leitura
                # Carrega os dados do arquivo JSON
                data = json.load(f)

            self.livros = [Livro(**l) for l in data["livros"]]
            self.usuarios = [Usuario(**u) for u in data["usuarios"]]
            self.dia_atual_sistema = data.get("dia_atual_sistema", 1) # Carrega o dia atual do sistema

            # Reconstruir empréstimos, ligando-os aos objetos Livro e Usuario existentes
            self.emprestimos = []
            for emp_data in data["emprestimos"]: # Cria uma lista de empréstimos
                livro_obj = next((l for l in self.livros if l.isbn == emp_data["livro"]), None) # Procura o livro pelo ISBN
                usuario_obj = next((u for u in self.usuarios if u.id_usuario == emp_data["usuario"]), None) # Procura o usuário pelo ID
                # Se ambos forem encontrados, cria um novo objeto Emprestimo
                if livro_obj and usuario_obj: # se o livro e o usuário forem encontrados
                    emp_data["livro"] = livro_obj # atualiza o livro para o objeto Livro
                    emp_data["usuario"] = usuario_obj # atualiza o usuário para o objeto Usuario
                    self.emprestimos.append(Emprestimo(**emp_data))  #cria o objeto Emprestimo com os dados carregados
            print(f"Dados carregados de {filename}")  # Exibe mensagem de sucesso
        except FileNotFoundError: #se o arquivo não for encontrado, inicializa com dados vazios
            print("🔄 Nenhum registro anterior encontrado.")
            print("📘 Iniciando o sistema com dados novos e vazios.")
            self.livros = [] # Lista de livros vazia
            self.usuarios = [] # Lista de usuários vazia
            self.emprestimos = [] # Lista de empréstimos vazia
        except Exception as e: # Captura qualquer outro erro ao carregar os dados
            print(f"Erro ao carregar dados: {e}")

def menu_gerenciar_tempo(biblioteca_instance): 
    # Função para gerenciar o tempo no sistema da biblioteca
    # Exibe um menu para avançar o dia do sistema, consultar o dia atual, etc.
    while True:
        # Exibe o menu de gerenciamento de tempo
        print("Bem-vindo ao Gerenciamento de Tempo da Biblioteca!")
        print("=======")
        print("=== Gerenciar Tempo ===")
        print(f"Dia Atual do Sistema: {biblioteca_instance.dia_atual_sistema}")
        print("1. Avançar 1 dia")
        print("2. Avançar 7 dias (1 semana)")
        print("3. Avançar N dias")
        print("4. Consultar dia atual")
        print("5. Voltar ao Menu Principal")
        print("=======")
        opcao_tempo = input("Escolha uma opção: ")

        if opcao_tempo == '1': # Avança o dia atual do sistema em 1 dia
            biblioteca_instance.dia_atual_sistema += 1
            print(f"Sistema avançou para o dia: {biblioteca_instance.dia_atual_sistema}")
        elif opcao_tempo == '2': # Avança o dia atual do sistema em 7 dias
            biblioteca_instance.dia_atual_sistema += 7
            print(f"Sistema avançou 7 dias. Novo dia: {biblioteca_instance.dia_atual_sistema}")
        elif opcao_tempo == '3': # Avança o dia atual do sistema em N dias
            try:
                n_dias = int(input("Quantos dias deseja avançar? "))
                if n_dias > 0: # Verifica se o número de dias é positivo
                    biblioteca_instance.dia_atual_sistema += n_dias
                    print(f"Sistema avançou {n_dias} dias. Novo dia: {biblioteca_instance.dia_atual_sistema}")
                else: # Se o número de dias não for positivo, exibe mensagem de erro
                    print("Por favor, insira um numero positivo de dias.")
            except ValueError: # Captura erro se a entrada não for um número inteiro
                print("Entrada inválida. Por favor, insira um número.")
        elif opcao_tempo == '4': # Consulta o dia atual do sistema
            print(f"O dia atual do sistema é: {biblioteca_instance.dia_atual_sistema}")
        elif opcao_tempo == '5': # Volta ao menu principal
            print("Retornando ao Menu Principal...")
            break 
        else: # Se a opção não for válida, exibe mensagem de erro
            print("Opção inválida. Tente novamente.")

def main():
    # Função principal que inicia o sistema da biblioteca
    print("Iniciando o Sistema de Biblioteca...")
    # Cria uma instância da classe Biblioteca
    biblioteca = Biblioteca() # Cria uma instância da biblioteca
    biblioteca.carregar_dados() # Carrega os dados ao iniciar

    while True:
        # Exibe o menu principal
        print("Bem-vindo ao Sistema de Biblioteca")
        print("======================")
        print("=== Menu Principal ===")
        print(f"Dia Atual do Sistema: {biblioteca.dia_atual_sistema}")
        print("1. Gerenciar Livros")
        print("2. Gerenciar Usuários")
        print("3. Gerenciar Empréstimos")
        print("4. Gerenciar Tempo")
        print("5. Salvar e Sair")
        print("======================")
        opcao_principal = input("Escolha uma opção: ")

        if opcao_principal == '1': #Gerencia os livros da biblioteca
            #exibe o menu de gerenciamento de livros
            while True: #
                print("=== Gerenciar Livros ===")
                print("======================")
                print("1. Adicionar Livro")
                print("2. Listar Livros")
                print("3. Voltar")
                print("======================")
                opcao_livro = input("Escolha uma opção: ")
                if opcao_livro == '1': # Adiciona um novo livro
                    titulo = input("Título: ")
                    autor = input("Autor: ")
                    isbn = input("ISBN: ")
                    biblioteca.adicionar_livro(titulo, autor, isbn)
                elif opcao_livro == '2': # Lista os livros cadastrados
                    biblioteca.listar_livros()
                elif opcao_livro == '3': # Volta ao menu principal
                    break
                else: # Se a opção não for válida, exibe mensagem de erro
                    print("Opção inválida.")
        elif opcao_principal == '2': # Gerencia os usuários da biblioteca
            while True: # Exibe o menu de gerenciamento de usuários
                print("=== Gerenciar Usuários ===")
                print("======================")
                print("1. Adicionar Usuário")
                print("2. Listar Usuários")
                print("3. Voltar")
                print("======================")
                opcao_usuario = input("Escolha uma opção: ")
                if opcao_usuario == '1': # Adiciona um novo usuário
                    print("=== Adicionar Usuário ===")
                    nome = input("Nome: ")
                    id_usuario = input("ID do Usuário: ")
                    biblioteca.adicionar_usuario(nome, id_usuario)
                elif opcao_usuario == '2': # Lista os usuários cadastrados
                    biblioteca.listar_usuarios()
                elif opcao_usuario == '3': # Volta ao menu principal
                    break
                else: # Se a opção não for válida, exibe mensagem de erro
                    print("Opção inválida.")
        elif opcao_principal == '3': # Gerencia os empréstimos de livros
            # Exibe o menu de gerenciamento de empréstimos
            while True:
                print("=== Gerenciar Empréstimos ===")
                print("======================")
                print("1. Realizar Empréstimo")
                print("2. Realizar Devolução")
                print("3. Listar Empréstimos")
                print("4. Voltar")
                print("======================")
                opcao_emprestimo = input("Escolha uma opção: ")
                if opcao_emprestimo == '1': # Realiza um novo empréstimo
                    print("=== Realizar Empréstimo ===")
                    isbn = input("ISBN do Livro: ")
                    id_usuario = input("ID do Usuário: ")
                    try:
                        prazo = int(input("Prazo de empréstimo (dias): "))
                        biblioteca.realizar_emprestimo(isbn, id_usuario, prazo)
                    except ValueError: # Captura erro se a entrada não for um número inteiro
                        print("Prazo inválido. Insira um número.")
                elif opcao_emprestimo == '2': # Realiza a devolução de um livro emprestado
                    print("=== Realizar Devolução ===")
                    isbn = input("ISBN do Livro: ")
                    id_usuario = input("ID do Usuário: ")
                    biblioteca.realizar_devolucao(isbn, id_usuario)
                elif opcao_emprestimo == '3': # Lista os empréstimos realizados
                    biblioteca.listar_emprestimos()
                elif opcao_emprestimo == '4': # Volta ao menu principal 
                    break
                else: # Se a opção não for válida, exibe mensagem de erro
                    print("Opção inválida.")
        elif opcao_principal == '4': # Gerencia o tempo de empréstimo
            menu_gerenciar_tempo(biblioteca)
        elif opcao_principal == '5': # Salva os dados e sai do sistema
            print("=== Salvar e Sair ===")
            biblioteca.salvar_dados() # Salva os dados antes de sair
            print("Saindo do sistema.")
            break
        else: # Se a opção não for válida, exibe mensagem de erro
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__": # Ponto de entrada do programa
    main()