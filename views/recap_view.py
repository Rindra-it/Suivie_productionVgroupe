from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFrame, 
                             QLabel, QPushButton, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QLineEdit, QScrollArea)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

class RecapView(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(20)

        
        header_layout = QHBoxLayout()
        
        title_vbox = QVBoxLayout()
        title_main = QLabel("RÉCAPITULATIF <span style='color:#96bf48;'>PRODUCTION</span>")
        title_main.setStyleSheet("font-size: 32px; font-weight: 900; color: white;")
        title_sub = QLabel("ANALYSE DES FLUX RÉELS")
        title_sub.setStyleSheet("color: #444; font-size: 10px; font-weight: bold; letter-spacing: 2px;")
        title_vbox.addWidget(title_main)
        title_vbox.addWidget(title_sub)
        
    
        filter_frame = QFrame()
        filter_frame.setStyleSheet("background-color: #0b0f0a; border-radius: 15px; border: 1px solid #1f2a1f;")
        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setContentsMargins(5, 5, 5, 5)
        
        self.btn_all = QPushButton("TOUT VOIR")
        self.btn_day = QPushButton("PAR JOUR")
        self.btn_week = QPushButton("PAR SEMAINE")
        self.btn_month = QPushButton("PAR MOIS")
        
        for btn in [self.btn_all, self.btn_day, self.btn_week, self.btn_month]:
            btn.setObjectName("FilterBtn")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            filter_layout.addWidget(btn)
        
        self.btn_all.setProperty("active", "true")

        header_layout.addLayout(title_vbox)
        header_layout.addStretch()
        header_layout.addWidget(filter_frame)
        self.main_layout.addLayout(header_layout)

        
        body_layout = QHBoxLayout()

        
        left_card = QFrame()
        left_card.setObjectName("WhiteCard")
        left_vbox = QVBoxLayout(left_card)
        left_vbox.setContentsMargins(25, 25, 25, 25)

        title_style = QLabel("📦 DÉTAILS PAR CODE STYLE")
        title_style.setStyleSheet("color: #96bf48; font-weight: bold; font-size: 12px; margin-bottom: 20px;")
        left_vbox.addWidget(title_style)

        self.style_table = QTableWidget()
        self.style_table.setColumnCount(5)
        self.style_table.setHorizontalHeaderLabels(["STYLE", "MANCHE", "COLLAR", "AUTRES", "TOTAL"])
        self.style_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.style_table.setStyleSheet("background: transparent; border: none; color: #666;")
        self.style_table.setShowGrid(False)
        self.style_table.verticalHeader().setVisible(False)
        left_vbox.addWidget(self.style_table)

        
        right_card = QFrame()
        right_card.setObjectName("WhiteCard")
        right_card.setFixedWidth(350)
        right_vbox = QVBoxLayout(right_card)
        right_vbox.setContentsMargins(25, 25, 25, 25)

        title_ouvrier = QLabel("👤 OUVRIERS")
        title_ouvrier.setStyleSheet("color: #96bf48; font-weight: bold; font-size: 12px;")
        right_vbox.addWidget(title_ouvrier)

        self.search_ouvrier = QLineEdit()
        self.search_ouvrier.setPlaceholderText("🔍 RECHERCHER MATRICULE...")
        self.search_ouvrier.setStyleSheet("background-color: #0b0f0a; border-radius: 10px; padding: 10px; color: white;")
        right_vbox.addWidget(self.search_ouvrier)

        self.worker_list_area = QVBoxLayout()
        right_vbox.addLayout(self.worker_list_area)
        right_vbox.addStretch()

        body_layout.addWidget(left_card, 2)
        body_layout.addWidget(right_card, 1)
        self.main_layout.addLayout(body_layout)


    def add_worker_card(self, matricule, total_qty, styles_count):
        w_card = QFrame()
        w_card.setStyleSheet("background-color: #0b0f0a; border-radius: 15px; padding: 15px; margin-bottom: 5px;")
        l = QHBoxLayout(w_card)
        
        info = QVBoxLayout()
        m_lbl = QLabel(f"<span style='color:#444; font-size:9px;'>MATRICULE</span><br><b style='color:white; font-size:14px;'>{matricule}</b>")
        info.addWidget(m_lbl)
        
        stat = QVBoxLayout()
        s_lbl = QLabel(f"<p align='right' style='color:#444; font-size:9px;'>{styles_count} STYLES</p><p align='right' style='color:#96bf48; font-size:20px; font-weight:bold;'>{total_qty}</p>")
        stat.addWidget(s_lbl)
        
        l.addLayout(info)
        l.addStretch()
        l.addLayout(stat)
        self.worker_list_area.addWidget(w_card)

    def update_table(self, data):
        """Met à jour le tableau avec les données agrégées"""
        self.style_table.setRowCount(0)
        if not data: return
        
        self.style_table.setRowCount(len(data))
        for i, row in enumerate(data):
            for j, val in enumerate(row):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                
                if j == 0:
                    f = QFont(); f.setBold(True); f.setItalic(True)
                    item.setFont(f); item.setForeground(QColor("white"))
                elif j == 4: 
                    f = QFont(); f.setBold(True); f.setPointSize(12)
                    item.setFont(f); item.setForeground(QColor("#96bf48"))
                else:
                    item.setForeground(QColor("#bbbbbb"))
                    
                self.style_table.setItem(i, j, item)