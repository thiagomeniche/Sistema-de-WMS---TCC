QUERY = 'SELECT p.codigo_produto, p.descricao, p.valor_venda, '
QUERY += 'c.descricao, m.descricao, i.quantidade '
QUERY += 'FROM PRODUTO AS p '
QUERY += 'INNER JOIN Categoria_Produto AS c ON p.id_categoria = c.id_categoria '
QUERY += 'INNER JOIN Marca_Produto AS m ON p.id_marca = m.id_marca '
QUERY += 'INNER JOIN Compra AS co ON p.codigo_produto = co.codigo_produto  '
QUERY += 'INNER JOIN Item AS i ON co.id_item = i.id_item '


class listar_produtos_caixa:
    def __init__(self, db):
        self.__db = db

    def listar(self):
            cursor = self.__db.connection.cursor()
            cursor.execute(QUERY)
         
            dados = []

            for row in cursor:
                dados.append(row)

            print('aqui', dados)

            return dados
            

