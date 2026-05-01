from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QFrame, QGridLayout, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt6.QtCore import Qt

class DashboardView(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

        
        stats_layout = QHBoxLayout()
        self.card_total = self.create_stat_card("PRODUCTION TOTALE", "{total_qty}", "pièces")
        self.card_effectif = self.create_stat_card("EFFECTIF PRÉSENT", "0", "personnes")
       
        stats_layout.addWidget(self.card_total)
        stats_layout.addWidget(self.card_effectif)
        
        self.main_layout.addLayout(stats_layout)

        
        middle_layout = QHBoxLayout()
        
        
        self.graph_frame = QFrame()
        self.graph_frame.setStyleSheet("background-color: #141d14; border-radius: 15px; border: 1px solid #222;")
        graph_vbox = QVBoxLayout(self.graph_frame)
        graph_vbox.addWidget(QLabel("ANALYSE DU FLUX DE PRODUCTION"))
        
        self.graph_placeholder = QLabel("Graphique en cours de chargement...")
        graph_vbox.addWidget(self.graph_placeholder, alignment=Qt.AlignmentFlag.AlignCenter)
        
        
        self.top5_frame = QFrame()
        self.top5_frame.setFixedWidth(300)
        self.top5_frame.setStyleSheet("background-color: #141d14; border-radius: 15px; border: 1px solid #222;")
        self.top5_layout = QVBoxLayout(self.top5_frame)
        self.top5_layout.addWidget(QLabel("🏆 TOP 5 PERFORMANCE"))
        
        middle_layout.addWidget(self.graph_frame, 3)
        middle_layout.addWidget(self.top5_frame, 1)
        self.main_layout.addLayout(middle_layout)

        
        self.recent_frame = QFrame()
        self.recent_frame.setStyleSheet("background-color: #141d14; border-radius: 15px; border: 1px solid #222;")
        recent_layout = QVBoxLayout(self.recent_frame)
        recent_layout.addWidget(QLabel("DERNIÈRES SAISIES"))
        
        self.table_recent = QTableWidget()
        self.table_recent.setColumnCount(4)
        self.table_recent.setHorizontalHeaderLabels(["MATRICULE", "STYLE", "TOTAL PCS", "ÉTAT"])
        self.table_recent.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_recent.setStyleSheet("background: transparent; color: white; border: none;")
        recent_layout.addWidget(self.table_recent)
        
        self.main_layout.addWidget(self.recent_frame)

    def create_stat_card(self, title, value, unit):
        card = QFrame()
        card.setStyleSheet("background-color: #141d14; border-radius: 15px; border: 1px solid #222; padding: 10px;")
        l = QVBoxLayout(card)
        t = QLabel(title)
        t.setStyleSheet("color: #888; font-size: 10px; font-weight: bold;")
        v = QLabel(f"<span style='font-size:24px; color:white;'>{value}</span> <span style='color:#96bf48;'>{unit}</span>")
        l.addWidget(t)
        l.addWidget(v)
        card.value_label = v
        card.unit = unit
        return card

    def update_dashboard(self, data):
        if not data: return
        self.card_total.value_label.setText(f"<span style='font-size:24px; color:white;'>{data['total']}</span> <span style='color:#96bf48;'>pièces</span>")
        self.card_effectif.value_label.setText(f"<span style='font-size:24px; color:white;'>{data['effectif']}</span> <span style='color:#96bf48;'>personnes</span>")
        
        
        for i in reversed(range(1, self.top5_layout.count())): 
            self.top5_layout.itemAt(i).widget().setParent(None)
        for i, (mat, qty) in enumerate(data['top_5']):
            lbl = QLabel(f"{i+1:02d}  {mat} <span style='float:right;'>{qty} PCS</span>")
            lbl.setStyleSheet("color: white; padding: 5px; border-bottom: 1px solid #222;")
            self.top5_layout.addWidget(lbl)

        
        self.table_recent.setRowCount(0)
        for row, entry in enumerate(data['recent']):
            self.table_recent.insertRow(row)
            for col, val in enumerate(entry):
                item = QTableWidgetItem(str(val))
                item.setForeground(Qt.GlobalColor.white if col != 2 else Qt.GlobalColor.green)
                self.table_recent.setItem(row, col, item)