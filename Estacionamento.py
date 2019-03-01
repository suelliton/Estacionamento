

#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction, QApplication,QLabel,QHBoxLayout,
QVBoxLayout,QWidget,QLineEdit,QPushButton,QComboBox,QDialog,QFormLayout,QListWidget,QListWidgetItem,QMessageBox)
from PyQt5.QtGui import QIcon,QPixmap,QFont, QImage,QColor
from model import *

class MainWindow(QMainWindow,QWidget):
    def __init__(self):
        super(MainWindow,self).__init__()

        self.initUI()

    def initUI(self):
        #Itens do menu arquivo
        exit = QAction(QIcon('img/exit.png'),'Sair',self)
        exit.setShortcut('Crtl+Q')
        exit.setStatusTip('Sair da Aplicação')
        exit.triggered.connect(self.close)

        cadastro_carros = QAction(QIcon('img/car.png'),'Cadastrar carros',self)
        cadastro_carros.setStatusTip('Cadastramento de carros')
        cadastro_carros.triggered.connect(self.tela_cadastrar_carros)

        cadastro_clientes = QAction(QIcon('img/user.png'),'Cadastrar cliente',self)
        cadastro_clientes.setStatusTip('Cadastramento de clientes')
        cadastro_clientes.triggered.connect(self.tela_cadastrar_clientes)

        listar_carros = QAction(QIcon('img/list.png'),'Listar clientes',self)
        listar_carros.setStatusTip('Lista de carros')
        listar_carros.triggered.connect(self.tela_listar_clientes)

        listar_clientes = QAction(QIcon('img/list2.png'),'Listar carros',self)
        listar_clientes.setStatusTip('Lista de clientes')
        listar_clientes.triggered.connect(self.tela_listar_carros)

        self.statusBar()#habilita legendas na parte inferior

        menubar =  self.menuBar()
        fileMenu = menubar.addMenu("&Arquivo")
        infoMenu = menubar.addMenu("&Info")
        fileMenu.addAction(cadastro_carros)
        fileMenu.addAction(cadastro_clientes)
        fileMenu.addAction(listar_carros)
        fileMenu.addAction(listar_clientes)
        fileMenu.addAction(exit)


        #self.tela_cadastrar_clientes()#desenha tela de cadastro de clientes
        #self.tela_cadastrar_carros()
        #self.tela_listar_clientes()
        self.tela_listar_carros()

        self.setGeometry(250,100,900,400)

        self.setWindowTitle('Estacionamento')
        self.show()
    @db_session
    def tela_listar_clientes(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        #self.central_widget.setStyleSheet(" background-image: url(img/background-roxo.jpg); background-repeat: no-repeat;")
        text_titulo =  QLabel("Clientes cadastrados",self.central_widget)
        text_titulo.move(315,20)
        font_20 = QFont("Times", 20, QFont.Bold)
        text_titulo.setFont(font_20)


        clientes = Cliente.select()
        listClientes = QListWidget(self.central_widget)
        listClientes.move(100,100)
        listClientes.resize(700,300)
        for cliente in clientes:
            row = QListWidgetItem(str(cliente.id) + "    "+cliente.nome)
            listClientes.addItem(row)
        listClientes.itemActivated.connect(self.double_click_clientes)





    @db_session
    def tela_listar_carros(self):
        self.lista_widgets_dinamicos = []
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        #self.central_widget.setStyleSheet(" background-image: url(img/background-roxo.jpg); background-repeat: no-repeat;")
        text_titulo =  QLabel("Carros cadastrados",self.central_widget)
        text_titulo.move(315,10)
        font_20 = QFont("Times", 20, QFont.Bold)
        text_titulo.setFont(font_20)

        listCarros = QListWidget(self.central_widget)
        listCarros.move(50,90)
        listCarros.resize(100,270)
        listCarros.itemActivated.connect(self.double_click_carros)#double click
        listCarros.itemClicked.connect(self.single_click_carros)#click simples

        edit_busca = QLineEdit("Buscar placa",self.central_widget)
        edit_busca.move(50,60)
        edit_busca.resize(100,20)

        edit_busca.textChanged[str].connect(lambda:self.onChanged_busca(edit_busca.text(),listCarros))

        self.buscar_carros(edit_busca.text(),listCarros)#primeira execução inicial

    @db_session
    def buscar_carros(self,placa,listCarros):
        listCarros.clear()
        if placa == "Buscar placa" or placa == "":
            carros = Carro.select()
            for carro in carros:
                row = QListWidgetItem(str(carro.id) + "    "+ carro.placa)
                listCarros.addItem(row)
        else:
            try:
                #carro = Carro.get(placa=placa)
                filtro = "'"+placa+"%"+"'"
                carros = Carro.select_by_sql("SELECT * FROM carro WHERE placa LIKE "+filtro)
                for carro in carros:
                    row = QListWidgetItem(str(carro.id) + "    "+ carro.placa)
                    listCarros.addItem(row)
            except:
                print("Carro não encontrado")

    def onChanged_busca(self,placa,listCarros):
        self.buscar_carros(placa,listCarros)

    def double_click_carros(self,row):
        print("Double click")
        id_carro = int(row.text().split("    ")[0])
        self.dialog_atualizar_carro(id_carro)

    def single_click_carros(self,row):
        print("Single click")
        id_carro = int(row.text().split("    ")[0])
        self.preenche_info_carro(id_carro)

    @db_session
    def dialog_atualizar_carro(self,id_carro):
        carro = Carro.get(id=id_carro)
        self.marca_carro = carro.marca
        self.modelo_carro = carro.modelo
        self.placa_carro = carro.placa
        self.dono_carro = carro.dono
        dialog = QDialog(self)
        dialog.resize(400,190)
        text_titulo =  QLabel("Atualizar carro",dialog)
        text_titulo.move(100,5)
        font_20 = QFont("Times", 20, QFont.Bold)
        text_titulo.setFont(font_20)

        text_marca = QLabel("Marca",dialog)
        text_marca.move(25,50)
        font_15 = QFont("Times", 15, QFont.StyleNormal)
        text_marca.setFont(font_15)

        combo_marca = QComboBox(dialog)
        combo_marca.move(25,80)
        marcas = ["CHEVROLET","FIAT","VOLKSWAGEN","FORD","RENAULT","HYUNDAI","TOYOTA","HONDA","AUDI","PEUGEOT","NISSAN","JEEP","CITROEN"]
        for marca in marcas:
            combo_marca.addItem(marca)

        combo_marca.setCurrentText(carro.marca) #seta o valor lido do banco no combobox

        text_modelo = QLabel("Modelo",dialog)
        text_modelo.move(175,50)
        font_15 = QFont("Times", 15, QFont.StyleNormal)
        text_modelo.setFont(font_15)

        combo_modelo = QComboBox(dialog)
        combo_modelo.move(175,80)
        self.onComboBoxMarca(combo_marca.currentText(),combo_modelo) #já chama a função para preencher o combobox modelo
        combo_modelo.setCurrentText(carro.modelo)#seta automaticamente o modelo no combobox

        combo_marca.activated[str].connect(lambda:self.onComboBoxMarca(combo_marca.currentText(),combo_modelo))#triggers padrão

        text_placa = QLabel("Placa",dialog)
        text_placa.move(300,50)
        font_15 = QFont("Times", 15, QFont.StyleNormal)
        text_placa.setFont(font_15)

        edit_placa = QLineEdit("",dialog)
        edit_placa.move(300,80)
        edit_placa.resize(75,25)
        edit_placa.setText(carro.placa)

        text_dono = QLabel("Dono",dialog)
        text_dono.move(25,120)
        font_15 = QFont("Times", 15, QFont.StyleNormal)
        text_dono.setFont(font_15)

        combo_dono = QComboBox(dialog)
        combo_dono.move(25,150)
        clientes = select(c for c in Cliente).order_by(Cliente.nome)
        for cliente in clientes:
            combo_dono.addItem(cliente.nome)
        combo_dono.setCurrentText(carro.dono.nome)
        combo_dono.activated[str].connect(lambda:self.onComboBoxDono(combo_dono.currentText()))

        btn_atualizar_carro = QPushButton("Atualizar",dialog)
        btn_atualizar_carro.move(300,150)
        btn_atualizar_carro.setStyleSheet("background-color: %s" % QColor(0,240,100).name())
        btn_atualizar_carro.clicked.connect(lambda:self.atualizar_carro(id_carro,self.marca_carro,self.modelo_carro,edit_placa.text(),self.dono_carro,dialog))
        dialog.exec_()
    @db_session
    def atualizar_carro(self,id_carro,marca,modelo,placa,id_dono,dialog1):
        dialog1.close()
        dialog2 = QDialog(self)
        dialog2.resize(250,100)
        try:
            if marca != "" and modelo != "" and placa != "" and id_dono != 0:
                dono = Cliente.get(id=id_dono)
                carro = Carro.get(id=id_carro)
                carro.marca = marca
                carro.modelo = modelo
                carro.placa = placa
                carro.dono = dono
                commit()
                label_sucesso = QLabel("Carro atualizado com sucesso!",dialog2)
                label_sucesso.move(20,40)
        except:
            label_erro = QLabel("Erro ao tentar atualizar o carro!",dialog2)
            label_erro.move(20,40)
        dialog2.exec_()
        dialog2.close()
        self.tela_listar_carros()
    @db_session
    def preenche_info_carro(self,id_carro):
        print("Prennche")
        for widget in self.lista_widgets_dinamicos:
            widget.setText("")
        self.lista_widgets_dinamicos.clear()

        carro = Carro.get(id=id_carro)

        font_15 = QFont("Times", 15, QFont.Bold)
        font_16 = QFont("Times", 16, QFont.Normal)

        text_placa_desc = QLabel("Placa",self.central_widget)
        text_placa_desc.move(200,60)
        text_placa_desc.setFont(font_15)
        text_placa_desc.show()

        text_placa = QLabel(carro.placa,self.central_widget)
        text_placa.setFont(font_16)
        text_placa.move(200,130)
        text_placa.show()
        self.lista_widgets_dinamicos.append(text_placa)

        text_marca_desc = QLabel("Marca",self.central_widget)
        text_marca_desc.move(400,60)
        text_marca_desc.setFont(font_15)
        text_marca_desc.show()

        text_marca = QLabel(carro.marca,self.central_widget)
        text_marca.setFont(font_16)
        text_marca.move(400,130)
        text_marca.show()
        self.lista_widgets_dinamicos.append(text_marca)

        text_modelo_desc = QLabel("Modelo",self.central_widget)
        text_modelo_desc.move(700,60)
        text_modelo_desc.setFont(font_15)
        text_modelo_desc.show()

        text_modelo = QLabel(carro.modelo,self.central_widget)
        text_modelo.setFont(font_16)
        text_modelo.move(700,130)
        text_modelo.show()
        self.lista_widgets_dinamicos.append(text_modelo)

        text_dono_desc = QLabel("Dono",self.central_widget)
        text_dono_desc.move(200,300)
        text_dono_desc.setFont(font_15)
        text_dono_desc.show()

        text_dono = QLabel(carro.dono.nome,self.central_widget)
        text_dono.setFont(font_16)
        text_dono.move(200,330)
        text_dono.show()
        self.lista_widgets_dinamicos.append(text_dono)

        if carro.estacionado == False:
            btn_estacionar = QPushButton("Estacionar",self.central_widget)
            btn_estacionar.setStyleSheet("color:white;background-color: %s" % QColor(240,10,10).name())
            btn_estacionar.move(700,330)
            btn_estacionar.show()
            btn_estacionar.clicked.connect(lambda:self.estacionar_carro(id_carro))
        else:
            btn_liberar = QPushButton("Liberar",self.central_widget)
            btn_liberar.setStyleSheet("color:white;background-color: %s" % QColor(10,240,10).name())
            btn_liberar.move(700,330)
            btn_liberar.show()
            btn_liberar.clicked.connect(lambda:self.liberar_carro(id_carro))

    @db_session
    def liberar_carro(self,id_carro):
        carro = Carro.get(id=id_carro)
        dialog = QDialog(self)
        dialog.resize(250,100)
        try:
            carro.estacionado = False
            commit()
            label_sucesso = QLabel("Carro liberado com sucesso!",dialog)
            label_sucesso.move(20,40)
        except:
            label_erro = QLabel("Ocorreu um erro!",dialog)
            label_erro.move(20,40)
        dialog.exec_()
        self.tela_listar_carros()
    @db_session
    def estacionar_carro(self,id_carro):
        carro = Carro.get(id=id_carro)
        dialog = QDialog(self)
        dialog.resize(250,100)
        try:
            carro.estacionado = True
            commit()
            label_sucesso = QLabel("Carro estacionado com sucesso!",dialog)
            label_sucesso.move(20,40)
        except:
            label_erro = QLabel("Ocorreu um erro!",dialog)
            label_erro.move(20,40)
        dialog.exec_()
        self.tela_listar_carros()

    @db_session
    def double_click_clientes(self,row):
        id_cliente = int(row.text().split("   ")[0])
        print(id_cliente)
        cliente = Cliente.get(id=id_cliente)

        dialog = QDialog(self)
        dialog.resize(550,240)

        text_nome = QLabel("Nome",dialog)
        text_nome.move(20,20)
        edit_nome = QLineEdit(cliente.nome,dialog)
        edit_nome.move(20,40)
        edit_nome.resize(510,25)

        text_cpf = QLabel("CPF",dialog)
        text_cpf.move(20,80)
        edit_cpf = QLineEdit(str(cliente.cpf),dialog)
        edit_cpf.move(20,100)
        edit_cpf.resize(100,25)

        text_telefone = QLabel("Telefone",dialog)
        text_telefone.move(20,140)
        edit_telefone = QLineEdit(str(cliente.telefone),dialog)
        edit_telefone.move(20,160)
        edit_telefone.resize(100,25)

        btn_salvar = QPushButton("Salvar",dialog)
        btn_salvar.move(450,200)
        btn_salvar.clicked.connect(lambda:self.atualizar_cliente(id_cliente,edit_nome.text(),edit_cpf.text(),edit_telefone.text(),dialog))
        btn_deletar = QPushButton("Deletar",dialog)
        btn_deletar.move(20,200)
        btn_deletar.clicked.connect(lambda:self.deletar_cliente(id_cliente,dialog))

        dialog.exec_()

    def tela_cadastrar_clientes(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        #self.central_widget.setStyleSheet(" background-image: url(img/background-roxo.jpg); background-repeat: no-repeat;")
        text_titulo =  QLabel("Cadastro de clientes",self.central_widget)
        #print(self.rect().center())
        text_titulo.move(320,20)
        font_20 = QFont("Times", 20, QFont.Bold)
        text_titulo.setFont(font_20)

        text_nome = QLabel("Nome",self.central_widget)
        text_nome.move(100,100)
        font_15 = QFont("Times", 15, QFont.StyleNormal)
        text_nome.setFont(font_15)

        edit_nome = QLineEdit("",self.central_widget)
        edit_nome.move(100,130)
        edit_nome.resize(700,25)

        text_cpf = QLabel("CPF",self.central_widget)
        text_cpf_warning = QLabel("Apenas números*",self.central_widget)
        text_cpf_warning.move(305,200)
        text_cpf.move(100,160)
        font_15 = QFont("Times", 15, QFont.StyleNormal)
        text_cpf.setFont(font_15)

        edit_cpf = QLineEdit("",self.central_widget)
        edit_cpf.move(100,190)
        edit_cpf.resize(200,25)

        text_telefone = QLabel("Telefone",self.central_widget)
        text_telefone.move(100,220)
        font_15 = QFont("Times", 15, QFont.StyleNormal)
        text_telefone.setFont(font_15)

        edit_telefone = QLineEdit("",self.central_widget)
        edit_telefone.move(100,250)
        edit_telefone.resize(200,25)

        btn_salvar_cliente = QPushButton("Salvar",self.central_widget)
        btn_salvar_cliente.move(720,310)
        btn_salvar_cliente.setStyleSheet("background-color: %s" % QColor(0,240,100).name())
        btn_salvar_cliente.clicked.connect(lambda:self.salvar_cliente(edit_nome.text(),edit_cpf.text(),edit_telefone.text()))
    @db_session
    def salvar_cliente(self,nome,cpf,telefone):
        dialog = QDialog(self)
        dialog.resize(250,100)
        if nome != "" and cpf != "" and telefone != "":
            cliente = Cliente(nome=nome,cpf=cpf,telefone=telefone)
            commit()
            label_sucesso = QLabel("Cliente adicionado com sucesso!",dialog)
            label_sucesso.move(20,40)
        else:
            label_erro = QLabel("Dados incompletos, verifique preenchimento!",dialog)
            label_erro.move(20,40)
        dialog.exec_()
        self.tela_cadastrar_clientes()
    @db_session
    def atualizar_cliente(self,id,nome,cpf,telefone,dialog1):
        dialog1.close()
        dialog2 = QDialog(self)
        dialog2.resize(250,100)
        try:
            cliente = Cliente.get(id=id)
            cliente.nome = nome
            cliente.cpf = cpf
            cliente.telefone = telefone
            commit()
            label_sucesso = QLabel("Cliente atualizado com sucesso!",dialog2)
            label_sucesso.move(20,40)
        except:
            label_erro = QLabel("Erro ao tentar atualizar o cliente!",dialog2)
            label_erro.move(20,40)
        dialog2.exec_()
        dialog2.close()
        self.tela_listar_clientes()
    @db_session
    def deletar_cliente(self,id,dialog1):
        dialog1.close()
        cliente = Cliente.get(id=id)
        pergunta = QMessageBox.question(self,'Mensagem','Voce realmente quer deletar o cliente '+ cliente.nome+' ?' ,QMessageBox.Yes | QMessageBox.No,QMessageBox.No)

        if pergunta == QMessageBox.Yes:
            cliente.delete()
            self.tela_listar_clientes()
        else :
            print("Operação cancelada")

    @db_session
    def tela_cadastrar_carros(self):
        #variaveis globais pois o preenchimento envolve várias funções
        self.marca_carro = ""
        self.modelo_carro = ""
        self.placa_carro = ""
        self.dono_carro = 0

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        text_titulo =  QLabel("Cadastro de carros",self.central_widget)
        text_titulo.move(320,20)
        font_20 = QFont("Times", 20, QFont.Bold)
        text_titulo.setFont(font_20)

        text_marca = QLabel("Marca",self.central_widget)
        text_marca.move(100,100)
        font_15 = QFont("Times", 15, QFont.StyleNormal)
        text_marca.setFont(font_15)

        combo_marca = QComboBox(self.central_widget)
        combo_marca.move(100,130)
        marcas = ["CHEVROLET","FIAT","VOLKSWAGEN","FORD","RENAULT","HYUNDAI","TOYOTA","HONDA","AUDI","PEUGEOT","NISSAN","JEEP","CITROEN"]
        for marca in marcas:
            combo_marca.addItem(marca)

        text_modelo = QLabel("Modelo",self.central_widget)
        text_modelo.move(230,100)
        font_15 = QFont("Times", 15, QFont.StyleNormal)
        text_modelo.setFont(font_15)

        combo_modelo = QComboBox(self.central_widget)
        combo_modelo.move(230,130)
        combo_marca.activated[str].connect(lambda:self.onComboBoxMarca(combo_marca.currentText(),combo_modelo))#precisa enviar o combo modelo por isso esta depois da inicializaçao do combo_modelo

        text_placa = QLabel("Placa",self.central_widget)
        text_placa.move(100,170)
        font_15 = QFont("Times", 15, QFont.StyleNormal)
        text_placa.setFont(font_15)

        edit_placa = QLineEdit("",self.central_widget)
        edit_placa.move(100,200)
        edit_placa.resize(200,25)

        text_dono = QLabel("Dono",self.central_widget)
        text_dono.move(100,240)
        font_15 = QFont("Times", 15, QFont.StyleNormal)
        text_dono.setFont(font_15)

        combo_dono = QComboBox(self.central_widget)
        combo_dono.move(100,270)
        clientes = select(c for c in Cliente).order_by(Cliente.nome)
        for cliente in clientes:
            combo_dono.addItem(cliente.nome)

        combo_dono.activated[str].connect(lambda:self.onComboBoxDono(combo_dono.currentText()))

        btn_salvar_carro = QPushButton("Salvar",self.central_widget)
        btn_salvar_carro.move(720,330)
        btn_salvar_carro.setStyleSheet("background-color: %s" % QColor(0,240,100).name())
        btn_salvar_carro.clicked.connect(lambda:self.salvar_carro(self.marca_carro,self.modelo_carro,edit_placa.text(),self.dono_carro))
    @db_session
    def salvar_carro(self,marca,modelo,placa,id_dono):
        dialog = QDialog(self)
        dialog.resize(250,100)
        if marca != "" and modelo != "" and placa != "" and id_dono != 0:
            dono = Cliente.get(id=id_dono)
            Carro(dono=dono,marca=marca,modelo=modelo,placa=placa)
            commit()
            label_sucesso = QLabel("Carro adicionado com sucesso!",dialog)
            label_sucesso.move(20,40)
            self.tela_cadastrar_carros()
        else:
            label_erro = QLabel("Dados incompletos, verifique preenchimento!",dialog)
            label_erro.move(20,40)
        dialog.exec_()

    def onComboBoxMarca(self,marca,combo_modelo):
        print(marca)
        self.marca_carro = marca
        combo_modelo.clear()
        modelos = []
        if marca == "CHEVROLET":
            modelos = ["CORSA","CELTA","ONIX","PRISMA"]
        elif marca == "FIAT":
            modelos = ["SIENA","UNO","PALIO","PUNTO"]
        elif marca == "VOLKSWAGEN":
            modelos = ["GOL","FOX","SAVEIRO","VOYAGE"]
        elif marca == "FORD":
            modelos = ["FOCUS","ECOSPORT","FIESTA","KA"]

        for modelo in modelos:
            combo_modelo.addItem(modelo)
        combo_modelo.activated[str].connect(self.onComboBoxModelo)

    def onComboBoxModelo(self,modelo):
        self.modelo_carro = modelo
    @db_session
    def onComboBoxDono(self,dono_nome):
        cliente = Cliente.get(nome=dono_nome)
        self.dono_carro = cliente.id

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
