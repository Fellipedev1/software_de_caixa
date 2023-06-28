import mysql.connector
import tkinter as tk
from tkinter.ttk import Combobox
from tkinter import messagebox


# Dicionário com os alimentos e seus respectivos preços
alimentos = {
    1: {"nome": "Caldo de feijão", "preco": 2.50},
    2: {"nome": "Caldo de mandioca", "preco": 1.75},
    3: {"nome": "Caldo de abóbora", "preco": 1.80},
    4: {"nome": "Cachorro Quente", "preco": 4.50},
    5: {"nome": "Milho Quente", "preco": 3.25},
    6: {"nome": "Pão de queijo", "preco": 2.00},
    7: {"nome": "Bolo de milho", "preco": 3.50},
    8: {"nome": "Biscoito de polvilho", "preco": 1.25},
    9: {"nome": "Café", "preco": 1.50},
    10: {"nome": "Canjica", "preco": 2.25},
    11: {"nome": "Doce de leite", "preco": 2.75},
    12: {"nome": "Pé de moleque", "preco": 1.80},
    13: {"nome": "Paçoca", "preco": 1.50},
    14: {"nome": "Cocada", "preco": 2.00}
}


# Variáveis para armazenar os itens selecionados, o valor total e os dados do cliente
itens_selecionados = []
valor_total = 0.0
nome_cliente = ""
cpf_cliente = ""

# Função para exibir o menu de alimentos
def exibir_menu():
    for id_alimento, info in alimentos.items():
        lista_alimentos.insert(tk.END, f"{id_alimento}. {info['nome']} - R${info['preco']:.2f}")

# Função para adicionar um item ao carrinho com uma determinada quantidade
def adicionar_item():
    id_alimento = int(combo_alimentos.get().split(".")[0])
    quantidade = int(entry_quantidade.get())
    if quantidade <= 0:
        messagebox.showwarning("Quantidade Inválida", "A quantidade deve ser maior que zero.")
    else:
        if id_alimento in alimentos:
            alimento = alimentos[id_alimento]
            valor_item = alimento['preco'] * quantidade
            itens_selecionados.append((id_alimento, alimento['nome'], alimento['preco'], quantidade))
            global valor_total
            valor_total += valor_item
            messagebox.showinfo("Sucesso", f"{quantidade}x {alimento['nome']} adicionado(a) ao carrinho.")
        else:
            messagebox.showwarning("Alimento Inválido", "Selecione um alimento válido.")

# Função para exibir o resumo do pedido
def exibir_resumo():
    resumo = f"Cliente: {nome_cliente}\nCPF: {cpf_cliente}\n\nResumo do pedido:\n"
    for id_alimento, item, preco, quantidade in itens_selecionados:
        valor_item = preco * quantidade
        resumo += f"{quantidade}x {item} - Valor: R${valor_item:.2f}\n"
    resumo += f"\nValor total: R${valor_total:.2f}"
    messagebox.showinfo("Resumo do Pedido", resumo)

# Função para atualizar os dados do cliente
def atualizar_dados():
    global nome_cliente, cpf_cliente
    nome_cliente = entry_cliente.get()
    cpf_cliente = entry_cpf.get()
    messagebox.showinfo("Sucesso", "Dados atualizados.")

# Função para calcular o total vendido até o momento
def calcular_total_vendido():
    # Conectando ao banco de dados
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="acesso123",
        database="arraia_senac"
    )

    # Verificando se a conexão foi bem-sucedida
    if conexao.is_connected():
        print("Conexão estabelecida com sucesso!")

    # Obtendo um cursor para executar as consultas SQL
    cursor = conexao.cursor()

    # Calculando o total vendido até o momento
    sql_total_vendido = "SELECT SUM(valor_comprado) FROM dados"
    cursor.execute(sql_total_vendido)
    quantidade_vendida = cursor.fetchone()[0]

    # Exibindo a quantidade vendida até o momento
    messagebox.showinfo("Total Vendido", f"Total Vendido até o Momento: R${quantidade_vendida:.2f}")

    # Fechando a conexão com o banco de dados
    conexao.close()

# Função para encerrar o programa e gravar os dados no banco de dados
def encerrar_programa():
    # Conectando ao banco de dados
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="acesso123",
        database="arraia_senac"
    )

    # Verificando se a conexão foi bem-sucedida
    if conexao.is_connected():
        print("Conexão estabelecida com sucesso!")

    # Obtendo um cursor para executar as consultas SQL
    cursor = conexao.cursor()

    # Inserindo os dados do cliente na tabela "dados"
    sql_dados = "INSERT INTO dados (nome, cpf, valor_comprado) VALUES (%s, %s, %s)"
    valores_dados = (nome_cliente, cpf_cliente, valor_total)
    cursor.execute(sql_dados, valores_dados)
    conexao.commit()
    messagebox.showinfo("Sucesso", "Dados do cliente inseridos na tabela 'dados' com sucesso!")

    # Inserindo os dados do cliente na tabela "produtos"
    for id_alimento, item, preco, quantidade in itens_selecionados:
        sql_produto = "INSERT INTO produtos (cpf, id, quantidade_vendida) VALUES (%s, %s, %s)"
        valores_produto = (cpf_cliente, id_alimento, quantidade)
        cursor.execute(sql_produto, valores_produto)
        conexao.commit()
        print(f"Item '{item}' inserido na tabela 'produtos' com sucesso!")

    # Fechando a conexão com o banco de dados
    conexao.close()
    window.destroy()

# Criação da janela principal
window = tk.Tk()
window.title("Festa Junina")
window.geometry("400x400")

# Listbox para exibir a lista de alimentos
lista_alimentos = tk.Listbox(window, width=40)
lista_alimentos.pack(padx=30, pady=30)

# Populando a lista de alimentos
exibir_menu()

# Rótulos e campos de entrada para dados do cliente
label_cliente = tk.Label(window, text="Nome do Cliente:")
label_cliente.pack()
entry_cliente = tk.Entry(window)
entry_cliente.pack()

label_cpf = tk.Label(window, text="CPF do Cliente:")
label_cpf.pack()
entry_cpf = tk.Entry(window)
entry_cpf.pack()

# Combobox e campo para selecionar itens alimentares
label_alimento = tk.Label(window, text="Selecione o Alimento:")
label_alimento.pack()
combo_alimentos = Combobox(window, values=[f"{id}. {info['nome']}" for id, info in alimentos.items()], state="readonly")
combo_alimentos.pack()

label_quantidade = tk.Label(window, text="Quantidade:")
label_quantidade.pack()
entry_quantidade = tk.Entry(window)
entry_quantidade.pack()

# Botões
# Botões
btn_adicionar = tk.Button(window, text="Adicionar Item", command=adicionar_item)
btn_adicionar.pack(pady=10)

btn_resumo = tk.Button(window, text="Exibir Resumo", command=exibir_resumo)
btn_resumo.pack(pady=10)

btn_atualizar = tk.Button(window, text="Atualizar Dados", command=atualizar_dados)
btn_atualizar.pack(pady=10)

btn_calcular_total = tk.Button(window, text="Calcular Total Vendido", command=calcular_total_vendido)
btn_calcular_total.pack(pady=10)

btn_encerrar = tk.Button(window, text="Encerrar Programa", command=encerrar_programa)
btn_encerrar.pack(pady=10)


window.mainloop()