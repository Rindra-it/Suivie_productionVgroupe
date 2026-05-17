from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                             QPushButton, QLabel, QTableWidget, QTableWidgetItem,
                             QHeaderView, QFrame)
from PyQt6.QtCore import Qt


class StyleManagementView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        title = QLabel("RÉFÉRENTIEL DES STYLES")
        title.setStyleSheet("color: #96bf48; font-size: 22px; font-weight: bold;")
        layout.addWidget(title)

        add_card = QFrame()
        add_card.setStyleSheet("background-color: #0b0f0a; border-radius: 10px; border: 1px solid #1a1a1a;")
        add_layout = QHBoxLayout(add_card)

        self.input_new_style = QLineEdit()
        self.input_new_style.setPlaceholderText("Nouveau Code Style...")
        self.input_new_style.setStyleSheet(
            "background: transparent; color: white; border: 1px solid #333; padding: 10px;"
        )

        self.btn_add_style = QPushButton("➕ ENREGISTRER")
        self.btn_add_style.setFixedSize(150, 40)
        self.btn_add_style.setStyleSheet(
            "background-color: #96bf48; color: #050705; font-weight: bold;"
        )

        add_layout.addWidget(self.input_new_style)
        add_layout.addWidget(self.btn_add_style)
        layout.addWidget(add_card)

        self.table_styles = QTableWidget()
        self.table_styles.setColumnCount(2)
        self.table_styles.setHorizontalHeaderLabels(["CODE STYLE", "ACTIONS"])
        self.table_styles.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table_styles.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        self.table_styles.setColumnWidth(1, 120)
        self.table_styles.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table_styles.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table_styles.setStyleSheet(
            "QTableWidget { background-color: transparent; color: white; }"
        )
        layout.addWidget(self.table_styles)

    def update_table(self, styles_data, edit_callback, delete_callback):
        """Recharge le tableau avec les styles et branche les callbacks."""
        # Bloquer les signaux pendant le rechargement pour éviter les glitches
        self.table_styles.setUpdatesEnabled(False)
        self.table_styles.setRowCount(0)

        for row_idx, style_tuple in enumerate(styles_data):
            style_name = str(style_tuple[0])
            self.table_styles.insertRow(row_idx)

            item = QTableWidgetItem(style_name)
            item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            self.table_styles.setItem(row_idx, 0, item)

            # Widget d'actions
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(5, 2, 5, 2)
            actions_layout.setSpacing(5)

            btn_edit = QPushButton("✎ Modifier")
            btn_edit.setFixedHeight(26)
            btn_edit.setStyleSheet(
                "background-color: #2c3e50; color: white; border-radius: 4px; padding: 0 8px;"
            )
            # Capture explicite de style_name dans la lambda
            btn_edit.clicked.connect(lambda checked, s=style_name: edit_callback(s))

            btn_del = QPushButton("✕ Supprimer")
            btn_del.setFixedHeight(26)
            btn_del.setStyleSheet(
                "background-color: #c0392b; color: white; border-radius: 4px; padding: 0 8px;"
            )
            btn_del.clicked.connect(lambda checked, s=style_name: delete_callback(s))

            actions_layout.addWidget(btn_edit)
            actions_layout.addWidget(btn_del)
            actions_layout.addStretch()

            self.table_styles.setCellWidget(row_idx, 1, actions_widget)

        self.table_styles.setUpdatesEnabled(True)
        self.table_styles.viewport().update()