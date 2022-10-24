#################################### APLICAÇÃO FLASK ####################################

import os
from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory, jsonify
from http import server
from lib2to3.pgen2 import driver
from re import S
import hashlib
import pyodbc
import textwrap
from datetime import date, datetime

from metodos import metodo_login, metodo_criar_usuario, metodo_att_usuario, metodo_buscar_usuario,\
     metodo_deleta_usuario, metodo_criar_fornecedor, metodo_cadastrar_categoria, metodo_cadastrar_marca, metodo_cadastrar_produto,\
         metodo_att_usuario, metodo_buscar_fornecedor, metodo_buscar_usuario_por_id, metodo_att_fornecedor, metodo_buscar_fornecedor_por_id,\
            metodo_att_produto, metodo_buscar_produto_por_id, metodo_listar_produtos_caixa

from models import Usuario,Pessoa,Endereco_Pessoa,ContatoPessoa, exibe_usuario, Fornecedor,\
     Funcionario, Categoria_Produto, Marca_Produto, Produto, Item, Compra, Exibe_Produto

app = Flask(__name__)
app.secret_key = 'alura'
port = int(os.environ.get('PORT', 5000))


#################################### ^^^^^^^^^^^^^^^^^^ ####################################

#################################### CONEXÃO SQL SERVER ####################################

######## Specify the Driver ##############

driver = '{ODBC Driver 17 for SQL Server}'


######## Specify the Server Name and Database Name ##############

server_name = 'thiagoms-rm'
database = 'SQLBI'

####### CREATE OUR SERVER URl ##############
server = '{server_name}.database.windows.net'.format(server_name=server_name)

# Define Username & Password

username = 'jeffsing'
password = '85!@Hty9256'
Encrypt = 'yes'
TrustServerCertificate='no'
Authentication = 'ActiveDirectoryIntegrated'

parametro = pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
db = parametro.cursor()

#################################### FIM CONECÇÃO PYODBC ####################################

cadastrar_usu = metodo_criar_usuario.cadastrar_usuario(db)
atualiza_usuario = metodo_att_usuario.atualiza_usuario(db)
buscar_id_usuario = metodo_buscar_usuario.busca_usuario(db)
excluir = metodo_deleta_usuario.deletar(db)
cria_fornecedor = metodo_criar_fornecedor.cadastrar_fornecedor(db)
login_usu = metodo_login.UsuarioDao(db)
cadastrar_cate = metodo_cadastrar_categoria.cadastrar_categoria(db)
data_atual = date.today()
cadastrar_marca= metodo_cadastrar_marca.cadastrar_categoria(db)
cadastrar_produto = metodo_cadastrar_produto.cadastrar_produto(db)
atualizar_usuario = metodo_att_usuario.atualiza_usuario(db)
atualizar_fornecedor = metodo_att_fornecedor.atualiza_fornecedor(db)
atualizar_produto = metodo_att_produto.atualiza_produto(db)

#####
buscar_fornecedor = metodo_buscar_fornecedor.busca_fornecedor(db)
buscar_usuario_por_id = metodo_buscar_usuario_por_id.busca_usuario_por_id(db)
buscar_fornecedor_por_id = metodo_buscar_fornecedor_por_id.busca_fornecedor_por_id(db)
buscar_produto_por_id = metodo_buscar_produto_por_id.busca_produto_por_id(db)

listar_produtos_caixa = metodo_listar_produtos_caixa.listar_produtos_caixa(db)
####

#################################### ^^^^^^^^^^^^^^^^^^ ####################################

####################################        VIEWS ADMINISTRADOR       ####################################


@app.route('/')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app.route('/gerenciar_Estoque')
def gerenciar_Estoque():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('gerenciar_Estoque')))
    listaCategoria = cadastrar_cate.exibe_categoria()
    listaMarca = cadastrar_marca.exibe_marca()
    listaProduto = cadastrar_produto.exibe_produto()
    return render_template('DashBoard/area_adminstrador/gerenciar_Estoque.html',lista_categoria= listaCategoria, lista_marca= listaMarca, Lista_Produto= listaProduto)


@app.route('/gerenciar_Usuarios')
def gerenciar_Usuarios():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('gerenciar_Usuarios')))
    lista = buscar_id_usuario.listar()
    return render_template('DashBoard/area_adminstrador/gerenciar_Usuarios.html',lista_usuario=lista)



@app.route('/gerenciar_Fornecedores')
def gerenciar_Fornecedores():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('gerenciar_Fornecedores')))
    lista = cria_fornecedor.exibe_fornecedor()
    return render_template('DashBoard/area_adminstrador/gerenciar_Fornecedores.html',lista_fornecedor= lista)


@app.route('/relatorios')
def relatorios():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('relatorios')))
    return render_template('DashBoard/area_adminstrador/relatorios.html')

@app.route('/contato')
def contato():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('contato')))
    lista = cria_fornecedor.exibe_fornecedor()
    return render_template('DashBoard/area_adminstrador/contato.html',lista_fornecedor= lista)
    
####################################        VIEWS USUARIO       ####################################

@app.route('/caixa')
def caixa():
    

    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('caixa')))

    
    print(session['usuario_logado'])

    produtos = listar_produtos_caixa.listar()

    return render_template('DashBoard/area_usuario/caixa.html', produtos=produtos)


@app.route('/cadastrar_venda', methods=['POST', ])
def cadastrar_venda():
    teste = request.form.get('teste')

    print(teste)

    return redirect(url_for('caixa'))


#################################### ^^^^^^^^^^^^^^^^^^ ####################################

#################################### AUTENTICAÇÃO E CRUD ####################################


@app.route('/autenticar', methods=['POST', ])
def autenticar():
    usuario = login_usu.buscar_por_id(request.form['usuario'])
    password = request.form['senha']
    password_app = hashlib.md5(password.encode())
    senha_aplicacao = password_app.hexdigest()
    if usuario:
        if usuario.senha_aplicacao == senha_aplicacao:
                session['usuario_logado'] = usuario.email_usuario
                if usuario.id_tipopessoa == '1':
                    flash('Usuario(a)  ' + usuario.nome_usuario + ' logado!')
                    proxima_pagina = url_for('caixa')
                    return redirect(proxima_pagina)
                else:
                    flash('Administrador(a)  ' + usuario.nome_usuario + ' logado!')
                    proxima_pagina = url_for('gerenciar_Estoque')
                    return redirect(proxima_pagina)
        else:
            flash('Senha invalida, tente denovo!')
            return redirect(url_for('login'))
    else:
        flash('Usuario não encontrado!')
        return redirect(url_for('login'))



@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Deslogado com sucesso!')
    return redirect(url_for('login'))


@app.route('/cadastrar_usuario',methods=['POST',])
def cadastrar_usuario():
    password = request.form['senha_usuario']
    id_pessoa = cria_fornecedor.id_fornecedor() + 1
    password_app = hashlib.md5(password.encode())
    senha_aplicacao = password_app.hexdigest()
    id_tipopessoa = request.form['radio']
    nome_usuario = request.form['nome_usuario']
    email_usuario = request.form['login_usuario']
    dt_cadastro = data_atual
    dt_bloqueio = None
    motivo_bloqueio = None
    dt_ultimo_acesso = None
    qtde_senha_errada = None
    dt_ultima_troca_senha = None
    ind_bloqueado = None
    
    att_usuario = Usuario(id_tipopessoa, nome_usuario,email_usuario,dt_cadastro,dt_bloqueio,motivo_bloqueio,\
    dt_ultimo_acesso,qtde_senha_errada,dt_ultima_troca_senha,ind_bloqueado, senha_aplicacao)
    
    
    id_tipo_pessoa = request.form['radio']
    nome = request.form['nome_usuario']
    inscricao = 3
    data_cadastro = data_atual
    ind_cliente = None
    ind_funcionario = None
    ind_fornecedor = None
    att_pessoa= Pessoa(id_pessoa, id_tipo_pessoa, nome, data_cadastro, ind_cliente, ind_funcionario,ind_fornecedor, inscricao)
    
   
    cep = request.form['cep']
    cidade = request.form['cidade']
    uf = request.form['uf']
    endereco = request.form['endereco']
    numero_endereco = request.form['numero_endereco']
    
    complemento = request.form['numero_endereco']
    att_endereco = Endereco_Pessoa(id_pessoa, cep, endereco, numero_endereco, complemento, cidade, uf, None)

   
    ddd = None
    celular = request.form['celular']
    telefone = request.form['telefone']
    email = request.form['login_usuario']
    nome_contato = request.form['nome_usuario']
    att_contato = ContatoPessoa(id_pessoa, ddd, celular, telefone, email, nome_contato)

    
    cargo = request.form['cargo']
    att_funcionario = Funcionario(id_pessoa, cargo)

    usuario = login_usu.buscar_por_id(request.form['login_usuario'])
    if usuario:
        if usuario.email_usuario == email_usuario:
            atualiza_cadastrousuario = atualizar_usuario.att_usuario(att_usuario,att_pessoa, att_endereco, att_contato, att_funcionario)
            flash('Usuario atualizado com sucesso!')
            return redirect(url_for('gerenciar_Usuarios'))
    else:
        salvar_cadastrausuario= cadastrar_usu.cadastra_usuario(att_usuario,att_pessoa,att_endereco,att_contato,att_funcionario)
        flash('Usuario Cadastrado com sucesso!')
        return redirect(url_for('gerenciar_Usuarios'))


@app.route('/cadastrar_fornecedor',methods=['POST',])
def cadastrar_fornecedor():

    id_pessoa = cria_fornecedor.id_fornecedor() + 1
    id_tipo_pessoa = '3'
    nome = request.form['razaosocial']
    inscricao = request.form['cnpj']
    data_cadastro = data_atual
    ind_fornecedor = None
    ind_cliente = None
    ind_funcionario = None
    att_pessoa= Pessoa(id_pessoa, id_tipo_pessoa, nome, data_cadastro, ind_cliente, ind_funcionario,ind_fornecedor, inscricao )
    

  
    
    cep = request.form['cep']
    cidade = request.form['cidade']
    uf = request.form['UF']
    endereco = request.form['endereco']
    num_endereco = request.form['numero_endereco']
    complemento = request.form['complemento']
    att_endereco = Endereco_Pessoa(id_pessoa, cep, endereco, num_endereco, complemento, cidade, uf, None)

    update_endereco = Endereco_Pessoa(id_pessoa, cep, endereco, num_endereco, complemento, cidade, uf, None)
    
    ddd = None
    celular = request.form['celular']
    telefone = request.form['telefone']
    email = request.form['email']
    nome_contato = request.form['nome_contato']
    att_contato = ContatoPessoa(id_pessoa, ddd, celular, telefone, email, nome_contato)

    update_contato = ContatoPessoa(id_pessoa, ddd, nome_contato, email, telefone, celular)
    att_fornecedor = Fornecedor(id_pessoa)
 
    pessoa= atualizar_fornecedor.buscar_por_id(request.form['cnpj'])
    if pessoa:
        
        if (pessoa.id_pessoa):
            print('a', pessoa.id_pessoa)
            atualiza_fornecedor = atualizar_fornecedor.att_fornecedor(att_pessoa,att_endereco,update_contato)
            flash('Fornecedor atualizado com sucesso!')
            return redirect(url_for('gerenciar_Fornecedores'))
    else:
        salvar_fornecedor = cria_fornecedor.cadastra_fornecedor(att_pessoa, att_endereco, att_contato, att_fornecedor)
        flash('Fornecedor cadastrado com sucesso!')
        return redirect(url_for('gerenciar_Fornecedores'))


@app.route('/cadastrar_Categoria', methods=['POST' ,])
def cadastrar_Categoria():
   
    id_categoria = request.form['idCategoria']
    descricao = request.form['descricaoCategoria']
    att_categoria = Categoria_Produto(id_categoria, descricao)
    Cadastrar_Categoria_Produto = cadastrar_cate.salvar_categoria(att_categoria)
    flash('Categoria cadastrado com sucesso!')
    return redirect(url_for('gerenciar_Estoque'))
  

@app.route('/cadastrar_Marca', methods=['POST' ,])
def cadastrar_Marca():
   
    id_marca = request.form['id_marca']
    descricao = request.form['descricaomarca']
    att_marca = Marca_Produto(id_marca,descricao)
    cadastrar_marca_produto = cadastrar_marca.salvar_marca(att_marca)
    flash('Marca cadastrada com sucesso!')
    return redirect(url_for('gerenciar_Estoque'))


@app.route('/cadastrar_Produto', methods = ['POST', ])
def cadastrar_Produto():
    codigo_produto = request.form['codigoProduto']
    id_categoria = request.form['categoriaproduto']
    descricao = request.form['nomeProduto']
    id_marca =  request.form['marca']
    valor = request.form['valorProduto'].replace(".","",2)
    valor_venda = valor.replace(",",".")
    att_produto = Produto(codigo_produto, id_categoria, descricao, id_marca, valor_venda)
    

    id_item =cadastrar_produto.item_id() + 1
    quantidade = request.form['qtdProduto']
    att_item = Item(id_item, codigo_produto, quantidade)

   
    data_compra = request.form['data_nota']
    id_fornecedor = None
    id_funcionario = None
    num_notafiscal = request.form['numeroNotaFiscal']
    cnpj = request.form['cnpj']

    valor_mutiplicado = request.form['valorTotal'].replace(".","",2)
    valor_total = valor_mutiplicado.replace(",",".")
    att_compra = Compra(id_item, codigo_produto, id_fornecedor, cnpj, id_funcionario, data_compra, valor_total, num_notafiscal)

    produto_att = atualizar_produto.buscar_por_id(request.form['codigoProduto'])
    compra_att = atualizar_produto.tb_compra_por_id(request.form['codigoProduto'])
    if produto_att:
        if (produto_att.codigo_produto and compra_att.cnpj == request.form['cnpj']):
            atualiza_produto = atualizar_produto.att_produto(att_compra,att_item,att_produto)
            flash('Produto atualizado com sucesso!')
            return redirect(url_for('gerenciar_Estoque'))
        else:
            flash('Já existe o codigo cadastrado com o CNPJ: ' + compra_att.cnpj + ' por favor atualize o produto !')
            return redirect(url_for('gerenciar_Estoque'))
    else:
        cadastrar = cadastrar_produto.salvar_produto(att_produto, att_item, att_compra)
        flash('Produto cadastrado com sucesso!')
        return redirect(url_for('gerenciar_Estoque'))





@app.route('/excluir_usuario/<string:id>')
def excluir_usuario(id):
    excluir.deletar_usuario(id)
    flash('Usuario removido com sucesso!')
    return redirect(url_for('gerenciar_Usuarios'))

@app.route('/excluir_fornecedor/<string:id>')
def excluir_fornecedor(id):
    excluir.deletar_fornecedor(id)
    flash('Fornecedor removido com sucesso!')
    return redirect(url_for('gerenciar_Fornecedores'))

@app.route('/excluir_produto/<string:id>')
def excluir_produto(id):
    excluir.deletar_produto(id)
    flash('Produto removido com sucesso!')
    return redirect(url_for('gerenciar_Estoque'))



#################################### ^^^^^^^^^^^^^^^^^^ ####################################


#################################### ^^^^^^^^^^^^^^^^^^^ ###################################

#consultar fornecedor


@app.route('/consultar_fornecedor',  methods=['POST'])
def consultar_fornecedor():
    cnpj = request.form.get('cnpj')

    nome_fornecedor = buscar_fornecedor.listar(cnpj)

    return jsonify({
			'mensagem': nome_fornecedor if nome_fornecedor else ""
		})


@app.route('/buscar_usuario_por_id', methods=['POST'])
def consultar_usuario_por_id():
    id_usuario = int(request.form['id_usuario'])

    dados_usuario = buscar_usuario_por_id.listar(id_usuario)

    print(dados_usuario[0][0])

    return jsonify({
			'nome_usuario': dados_usuario[0][0],
            'cep': dados_usuario[0][1],
            'cidade': dados_usuario[0][2],
            'uf': dados_usuario[0][3],
            'endereco': dados_usuario[0][4],
            'numero_endereco': dados_usuario[0][5],
            'telefone': dados_usuario[0][6],
            'celular': dados_usuario[0][7],
            'cargo': dados_usuario[0][8],
            'email_usuario': dados_usuario[0][9],
            'id_tipo_pessoa': dados_usuario[0][10]

	})



@app.route('/buscar_fornecedor_por_id', methods=['POST'])
def consultar_fornecedor_por_id():
    id_fornecedor = int(request.form['id_fornecedor'])

    dados_fornecedor = buscar_fornecedor_por_id.listar(id_fornecedor)

    print(dados_fornecedor[0][0])

    return jsonify({
			'cnpj': dados_fornecedor[0][0],
            'razaosocial': dados_fornecedor[0][1],
            'cep': dados_fornecedor[0][2],
            'endereco': dados_fornecedor[0][3],
            'numero_endereco': dados_fornecedor[0][4],
            'complemento': dados_fornecedor[0][5],
            'cidade': dados_fornecedor[0][6],
            'uf': dados_fornecedor[0][7],
            'nome_contato': dados_fornecedor[0][8],
            'email': dados_fornecedor[0][9],
            'telefone': dados_fornecedor[0][10],
            'celular': dados_fornecedor[0][10]
	})

@app.route('/buscar_produto_por_id', methods=['POST'])
def consultar_produto_por_id():
    id_produto = int(request.form['id_produto'])

    dados_produto = buscar_produto_por_id.listar(id_produto)

    print(dados_produto[0][0])

    return jsonify({
			'cnpj': dados_produto[0][0],
            'data_nota': dados_produto[0][1],
            'numeroNotaFiscal': dados_produto[0][2],
            'codigoProduto': dados_produto[0][3],
            'nomeProduto': dados_produto[0][4],
            'valorProduto': dados_produto[0][5],
            'qtdProduto': dados_produto[0][6],
            'marca': dados_produto[0][7],
            'categoriaproduto': dados_produto[0][8],
            #'valorTotal': dados_produto[0][9]
	})




app.run(debug=True)


