from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                             QPushButton, QLabel, QFrame, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QDialog)
from PyQt6.QtCore import Qt


class AddWorkerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nouvel Employé")
        self.setFixedSize(350, 450)
        self.setStyleSheet("background-color: #141d14; color: white;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 40, 30, 40)
        layout.setSpacing(15)

        title = QLabel("AJOUT EMPLOYÉ")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #96bf48; margin-bottom: 10px;")
        layout.addWidget(title)

        
        input_style = "background-color: #0b0f0a; border: 1px solid #333; padding: 10px; border-radius: 5px; color: white;"

        self.input_mat = QLineEdit()
        self.input_mat.setPlaceholderText("Matricule")
        self.input_mat.setStyleSheet(input_style)
        
        self.input_nom = QLineEdit()
        self.input_nom.setPlaceholderText("Nom")
        self.input_nom.setStyleSheet(input_style)

        self.input_prenom = QLineEdit()
        self.input_prenom.setPlaceholderText("Prénom")
        self.input_prenom.setStyleSheet(input_style)

        layout.addWidget(QLabel("MATRICULE"))
        layout.addWidget(self.input_mat)
        layout.addWidget(QLabel("NOM"))
        layout.addWidget(self.input_nom)
        layout.addWidget(QLabel("PRÉNOM"))
        layout.addWidget(self.input_prenom)

        self.btn_confirm = QPushButton("ENREGISTRER")
        self.btn_confirm.setStyleSheet("""
            QPushButton { background-color: #96bf48; color: #0b0f0a; font-weight: bold; padding: 12px; border-radius: 5px; margin-top: 10px; }
            QPushButton:hover { background-color: #a8d652; }
        """)
        layout.addWidget(self.btn_confirm)
        
        
        self.btn_confirm.clicked.connect(self.accept)

class WorkerView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        
        header_layout = QHBoxLayout()
        title = QLabel("Gestion du Personnel")
        title.setStyleSheet("color: #96bf48; font-size: 24px; font-weight: bold;")
        
        self.btn_open_add = QPushButton("+ AJOUT D'EMPLOYÉ")
        self.btn_open_add.setFixedSize(180, 40)
        self.btn_open_add.setStyleSheet("""
            QPushButton { background-color: #96bf48; color: #0b0f0a; font-weight: bold; border-radius: 5px; }
            QPushButton:hover { background-color: #a8d652; }
        """)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.btn_open_add)
        layout.addLayout(header_layout)

       
        search_frame = QFrame()
        search_frame.setStyleSheet("background-color: #141d14; border-radius: 8px; padding: 10px;")
        search_layout = QHBoxLayout(search_frame)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Rechercher par matricule, nom ou prénom...")
        self.search_input.setStyleSheet("background-color: #0b0f0a; color: white; padding: 10px; border: 1px solid #333;")
        
        search_layout.addWidget(QLabel("🔍"))
        search_layout.addWidget(self.search_input)
        layout.addWidget(search_frame)

        self.table_workers = QTableWidget()
        self.table_workers.setColumnCount(3)
        self.table_workers.setHorizontalHeaderLabels(["Matricule", "Nom", "Prénom"])
        self.table_workers.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_workers.setStyleSheet("""
            QTableWidget { background-color: #0b0f0a; color: white; gridline-color: #222; border: none; }
            QHeaderView::section { background-color: #141d14; color: #96bf48; padding: 10px; font-weight: bold; border: none; }
        """)
        layout.addWidget(self.table_workers)

    def update_table(self, workers_data):
        self.table_workers.setRowCount(0)
        for row_number, row_data in enumerate(workers_data):
            self.table_workers.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable)
                self.table_workers.setItem(row_number, column_number, item)