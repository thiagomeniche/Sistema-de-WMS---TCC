from models import  Usuario, Pessoa, Endereco_Pessoa, ContatoPessoa, Funcionario

SQL_CADASTRAR_USUARIO = 'insert into Usuario (id_tipopessoa, nome_usuario, email_usuario, dt_cadastro,  senha_aplicacao) values (?, ?, ?, ?, ?)'
SQL_CADASTRAR_PESSOA = 'insert into Pessoa(id_pessoa, id_tipo_pessoa, nome) values (?, ?, ?)'
SQL_CADASTRAR_ENDERECO = 'insert into Endereco_Pessoa(id_pessoa, endereco, complemento, cidade, uf ,cep) values (?, ?, ?, ?, ?, ?)'
SQL_CADASTRAR_CONTATO = 'insert into Contato_Pessoa(id_pessoa, celular, telefone, email, nome_contato) values (?, ?, ?, ?, ?)'
SQL_CADASTRAR_FUNCIONARIO = 'insert into Funcionario(id_pessoa, cargo) values (?,?)'


SQL_PROCEDURE_INSERT_USUARIO = "{CALL sp_insert_usuario (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)}"


class cadastrar_usuario:
    def __init__(self, db):
        self.__db = db
    

    def cadastra_usuario(self, usuario,Pessoa,Endereco_Pessoa,ContatoPessoa,Funcionario):
        cursor= self.__db

        values = (
            Funcionario.cargo, usuario.nome_usuario, Pessoa.inscricao, usuario.id_tipopessoa,
            usuario.nome_usuario, usuario.email_usuario, usuario.dt_cadastro, usuario.senha_aplicacao,
            ContatoPessoa.celular, ContatoPessoa.telefone, ContatoPessoa.email, ContatoPessoa.nome_contato,
            Endereco_Pessoa.endereco, Endereco_Pessoa.complemento, Endereco_Pessoa.cidade, Endereco_Pessoa.uf,
            Endereco_Pessoa.cep, Endereco_Pessoa.num_endereco
        )

        cursor.execute(SQL_PROCEDURE_INSERT_USUARIO, values)

        """
        cursor.execute(SQL_CADASTRAR_PESSOA, (Pessoa.id_pessoa, Pessoa.id_tipo_pessoa, Pessoa.nome))
        cursor.execute(SQL_CADASTRAR_USUARIO, (usuario.id_tipopessoa, usuario.nome_usuario, usuario.email_usuario, usuario.dt_cadastro, usuario.senha_aplicacao))
        cursor.execute(SQL_CADASTRAR_ENDERECO, (Endereco_Pessoa.id_pessoa, Endereco_Pessoa.endereco, Endereco_Pessoa.complemento, Endereco_Pessoa.cidade, Endereco_Pessoa.uf, Endereco_Pessoa.cep))
        cursor.execute(SQL_CADASTRAR_CONTATO, (ContatoPessoa.id_pessoa, ContatoPessoa.celular, ContatoPessoa.telefone, ContatoPessoa.email, ContatoPessoa.nome_contato))
        cursor.execute(SQL_CADASTRAR_FUNCIONARIO, (Funcionario.id_pessoa, Funcionario.cargo))
        usuario.cod_usuario = cursor.execute('SELECT @@IDENTITY AS cod_usuario;')
        Pessoa.id_pessoa = cursor.execute('SELECT @@IDENTITY AS id_pessoa;')
        """
        self.__db.connection.commit()
        return usuario,Pessoa