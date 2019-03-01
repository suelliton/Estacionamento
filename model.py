from pony.orm import *
db = Database()

class Cliente(db.Entity):
    id = PrimaryKey(int,auto=True)
    nome = Required(str)
    cpf = Required(str)
    telefone = Required(str)
    carros = Set('Carro')

class Carro(db.Entity):
    marca = Required(str)
    modelo = Required(str)
    placa = Required(str)
    estacionado = Required(bool, default=False, sql_default='0')
    dono = Required(Cliente)

db.bind(provider = "mysql",host="127.0.0.1",user="root",passwd="suelliton",db="estacionamento")
db.generate_mapping(create_tables = True)
set_sql_debug(True)
