from validate_email_address import validate_email
import mysql.connector
from django.shortcuts import render, redirect
from django.contrib import messages

def index(request):
    return render(request, 'sistema/html_cadastro.html')

def segunda_pagina(request):
    return render(request, 'sistema/segundapag.html')

def conectar_banco():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='25143577Dan@',
            database='teste',
            autocommit=False  # Adicionado para controle manual de transações
        )
        return conexao
    except mysql.connector.Error as err:
        print(f'Erro ao conectar ao banco de dados: {err}')
        return None

def cadastrar_cliente(request):
    if request.method == "POST":
        nome_apelido = request.POST.get('nome_cliente', '').strip()
        email = request.POST.get('email', '').strip().lower()  # Normaliza email para minúsculas
        senha = request.POST.get('senha', '').strip()
        
        # Validações melhoradas
        if not nome_apelido or not nome_apelido.replace(" ", "").isalpha():
            messages.error(request, 'Digite um nome válido (apenas letras e espaços)')
            return redirect('index')
        
        if not email or '@' not in email or '.' not in email.split('@')[-1]:
            messages.error(request, 'Digite um email válido')
            return redirect('index')
        
        if not senha or not senha.isdigit():
            messages.error(request, 'A senha deve conter apenas números')
            return redirect('index')
        
        print(f"Tentativa de cadastro - Nome: {nome_apelido}, E-mail: {email}, Senha: {senha}")
        
        conexao = None
        cursor = None
        try:
            conexao = conectar_banco()
            if not conexao or not conexao.is_connected():
                messages.error(request, 'Erro na conexão com o banco de dados')
                return redirect('index')
            
            cursor = conexao.cursor(dictionary=True)
            
            # Verifica se email já existe (consulta corrigida)
            cursor.execute("SELECT idteste FROM clientes WHERE email = %s", (email,))
            if cursor.fetchone():
                messages.error(request, 'Este e-mail já está cadastrado!')
                return redirect('index')
            
            # Insere os dados do cliente
            sql = """INSERT INTO clientes (nome_cliente, senha, email)
                     VALUES (%s, %s, %s)"""
            cursor.execute(sql, (nome_apelido, senha, email))
            conexao.commit()  # Confirma a transação
            
            print('Cliente cadastrado com sucesso no banco de dados!')
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('segunda_pagina')
            
        except mysql.connector.Error as err:
            print(f'Erro MySQL ao cadastrar cliente: {err}')
            if conexao:
                conexao.rollback()  # Reverte em caso de erro
            messages.error(request, f'Erro no banco de dados: {err.msg}')
            return redirect('index')
            
        except Exception as e:
            print(f'Erro inesperado ao cadastrar cliente: {e}')
            if conexao:
                conexao.rollback()
            messages.error(request, 'Ocorreu um erro inesperado')
            return redirect('index')
            
        finally:
            # Fecha cursor e conexão de forma segura
            try:
                if cursor:
                    cursor.close()
            except Exception as e:
                print(f'Erro ao fechar cursor: {e}')
                
            try:
                if conexao and conexao.is_connected():
                    conexao.close()
            except Exception as e:
                print(f'Erro ao fechar conexão: {e}')
    
    return redirect('index')