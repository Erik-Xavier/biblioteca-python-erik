Sistema de Biblioteca em Python
Estrutura Geral do Programa
Este programa simula um sistema básico de gerenciamento de biblioteca. Ele permite cadastrar livros e usuários, realizar empréstimos e devoluções, aplicar multas por atraso, e gerenciar o tempo dentro do sistema para simular o passar dos dias.

Organização dos Dados
Os dados são organizados utilizando a biblioteca dataclasses do Python, o que facilita a criação e manutenção das estruturas.

Livro: contém título, autor, ISBN e disponibilidade. (o isbn é utilizado para diferenciar um livro do outro, mesmo que tenham o mesmo título. Isso evita confusões na hora de fazer um empréstimo ou devolução, pois cada ISBN representa exatamente uma edição de um livro.)

Usuário: contém nome e um ID único.

Empréstimo: relaciona um livro a um usuário, com informações sobre datas de empréstimo, devolução prevista, devolução efetiva e multa.

O sistema permite que diferentes tipos de usuários (como alunos e professores) possam ter prazos diferenciados para empréstimos, podendo ser ajustado na lógica.


Principais Funções
Adicionar Livro/Usuário: cadastra novos livros e usuários.

Realizar Empréstimo: verifica disponibilidade do livro e existência do usuário, cria o empréstimo e define data de devolução prevista com base no prazo.

Realizar Devolução: registra a devolução, marca o livro como disponível e calcula multa caso haja atraso.

Gerenciamento de Tempo: permite avançar o tempo do sistema para testar situações de atraso e cálculo de multas.

Salvar e Carregar Dados: utiliza arquivos JSON para persistência dos dados entre execuções.

Lógica das Operações
Empréstimo: Ao emprestar um livro, verifica se ele está disponível e se o usuário existe. Define a data de devolução prevista somando o prazo escolhido ao dia atual do sistema.

Devolução e Multas: Ao devolver, compara a data efetiva com a prevista. Se a devolução for atrasada, calcula multa de R$ 0,50 por dia de atraso e registra no empréstimo.

Sistema de Data Simulado: O programa usa um contador interno dia_atual_sistema que pode ser avançado manualmente via menu para simular a passagem do tempo.


Demonstração do Sistema
O sistema possui menus interativos que permitem:

Cadastrar livros e usuários.

Realizar empréstimos e devoluções.

Visualizar listas de livros, usuários e empréstimos.

Avançar o tempo no sistema para simular atrasos e aplicar multas.

Assim, é possível testar todas as funcionalidades do sistema de forma prática e didática.
