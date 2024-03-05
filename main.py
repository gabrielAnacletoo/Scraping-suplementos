import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt5.QtGui import QMovie
from scraper import scraper

class ProductSearchWorker(QThread):
    finished = pyqtSignal(object)
    
    def __init__(self, product_name):
        super().__init__()
        self.product_name = product_name
    
    def run(self):
        result_growth = scraper(self.product_name)
        self.finished.emit(result_growth)

class ProductSearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pesquisar suplementos")
        self.showMaximized()  # Exibe a janela maximizada
        
        self.label = QLabel("Nome do suplemento:")
        self.entry = QLineEdit()
        self.search_button = QPushButton("Pesquisar")
        self.search_button.setStyleSheet("background-color: #4CAF50; color: white; border: none; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 8px;")
        self.search_button.clicked.connect(self.search_product)
        
        # Botão "Fechar"
        self.close_button = QPushButton("Fechar")
        self.close_button.setStyleSheet("background-color: #f44336; color: white; border: none; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 8px;")
        self.close_button.clicked.connect(self.close)
        
        # Tabela para exibir os resultados
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Produto", "Preço", "Avaliações", "Link"])
        
        # Label para exibir o spinner
        self.spinner_label = QLabel(self)
        self.spinner_label.setAlignment(Qt.AlignCenter)
        self.spinner_label.setMinimumSize(100, 100)
        
        # Layouts
        main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        
        # Adiciona os elementos ao layout principal
        main_layout.addWidget(self.label)
        main_layout.addWidget(self.entry)
        main_layout.addWidget(self.table)  # Adiciona a tabela
        main_layout.addWidget(self.spinner_label)  # Adiciona o spinner
        
        # Adiciona os botões ao layout de botões
        button_layout.addWidget(self.search_button)
        button_layout.addWidget(self.close_button)
        
        # Adiciona o layout de botões ao layout principal
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
        
        # Cache para armazenar os resultados da pesquisa
        self.cache = {}
        
        # Cria o spinner
        self.movie = QMovie("./spinner.gif")
        self.spinner_label.setMovie(self.movie)
    
    def search_product(self):
        product_name = self.entry.text()
        self.spinner_label.setVisible(True)
        self.movie.start()
        
        # Inicia a thread para realizar a pesquisa
        self.worker = ProductSearchWorker(product_name)
        self.worker.finished.connect(self.show_result)
        self.worker.start()
    
    def show_result(self, result):
        # Limpa a tabela
        self.table.setRowCount(0)
        
        # Ordena os resultados pelo preço antes de exibi-los
        sorted_result = sorted(result, key=lambda x: float(x['Preço'].replace('R$', '').replace(',', '.')))
        
        # Preenche a tabela com os resultados ordenados
        row = 0
        for product in sorted_result:
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(product['Produto']))
            self.table.setItem(row, 1, QTableWidgetItem(product['Preço']))
            self.table.setItem(row, 2, QTableWidgetItem(product['Avaliações']))
            self.table.setItem(row, 3, QTableWidgetItem(product['Link']))
            row += 1
        
        # Define o tamanho máximo da tabela
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Ajusta a largura mínima das colunas
        self.table.horizontalHeader().setMinimumSectionSize(200)
        self.table.verticalHeader().setMinimumSectionSize(50)
        
        # Define que a última coluna preencha todo o espaço disponível
        self.table.horizontalHeader().setStretchLastSection(True)
        
        # Esconde o spinner
        self.movie.stop()
        self.spinner_label.setVisible(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProductSearchApp()
    window.show()
    sys.exit(app.exec_())
