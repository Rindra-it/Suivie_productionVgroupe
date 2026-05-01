from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFrame, 
                             QLabel, QComboBox, QDateEdit, QLineEdit, 
                             QSpinBox, QPushButton, QCompleter)
from PyQt6.QtCore import Qt, QDate

class InputView(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QFrame()
        card.setObjectName("ProductionCard")
        card.setFixedSize(650, 580)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(50, 40, 50, 40)
        card_layout.setSpacing(15)

        title = QLabel("PRODUCTION")
        title.setObjectName("Title")
        card_layout.addWidget(title)

       
        row1 = QHBoxLayout()
        col1 = QVBoxLayout(); col1.addWidget(QLabel("ÉTAT")); self.etat = QComboBox(); col1.addWidget(self.etat)
        col2 = QVBoxLayout(); col2.addWidget(QLabel("DATE")); self.date = QDateEdit(); self.date.setDisplayFormat("dd/MM/yyyy"); self.date.setDate(QDate.currentDate()); col2.addWidget(self.date)
        row1.addLayout(col1); row1.addLayout(col2)
        card_layout.addLayout(row1)

        
        row2 = QHBoxLayout()
        col3 = QVBoxLayout(); col3.addWidget(QLabel("MATRICULE (Saisie libre)")); self.matricule = QLineEdit(); col3.addWidget(self.matricule)
        col4 = QVBoxLayout(); col4.addWidget(QLabel("STYLE (Saisie libre)")); self.style = QLineEdit(); col4.addWidget(self.style)
        row2.addLayout(col3); row2.addLayout(col4)
        card_layout.addLayout(row2)

        
        row3 = QHBoxLayout()
        col5 = QVBoxLayout(); col5.addWidget(QLabel("CATÉGORIE")); self.cat = QComboBox(); col5.addWidget(self.cat)
        col6 = QVBoxLayout(); col6.addWidget(QLabel("QUANTITÉ")); self.qty = QSpinBox(); self.qty.setRange(0, 10000); col6.addWidget(self.qty)
        row3.addLayout(col5); row3.addLayout(col6)
        card_layout.addLayout(row3)

        card_layout.addWidget(QLabel("NUMÉRO TICKET"))
        self.ticket = QLineEdit()
        card_layout.addWidget(self.ticket)

        self.btn_valid = QPushButton("💾 VALIDER LA SAISIE")
        self.btn_valid.setObjectName("ValidBtn")
        card_layout.addSpacing(20)
        card_layout.addWidget(self.btn_valid)

        main_layout.addWidget(card)

    def set_suggestions(self, matricules, styles):
        """Applique l'auto-complétion sur les champs de saisie"""
        for data, widget in [(matricules, self.matricule), (styles, self.style)]:
            completer = QCompleter(data)
            completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            completer.setFilterMode(Qt.MatchFlag.MatchContains)
            widget.setCompleter(completer)
           
            widget.setPlaceholderText("Tapez ou choisissez...")