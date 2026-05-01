DARK_THEME = """
QMainWindow {
    background-color: #0b0f0a;
}

/* Sidebar */
QFrame#Sidebar {
    background-color: #0b0f0a;
    border-right: 1px solid #1a1a1a;
}

/* Menu items */
QPushButton#MenuButton {
    color: #888;
    text-align: left;
    padding: 10px 20px;
    border: none;
    font-size: 13px;
    background-color: transparent;
}

QPushButton#MenuButton:hover {
    color: #96bf48;
    background-color: #141d14;
}

QPushButton#MenuButton[active="true"] {
    color: #96bf48;
    background-color: #141d14;
    border-left: 3px solid #96bf48;
}

/* La Carte Centrale (Saisie) */
QFrame#ProductionCard {
    background-color: #141d14;
    border-radius: 40px;
    border: 1px solid #1f2a1f;
}

/* Inputs */
QLineEdit, QComboBox, QDateEdit, QSpinBox {
    background-color: #0b0f0a;
    color: #96bf48;
    border: 1px solid #1f2a1f;
    border-radius: 10px;
    padding: 12px;
    font-size: 14px;
}

QComboBox::drop-down { border: none; }

/* Bouton Valider */
QPushButton#ValidBtn {
    background-color: #96bf48;
    color: #0b0f0a;
    font-weight: bold;
    border-radius: 15px;
    padding: 15px;
    font-size: 16px;
}

QPushButton#ValidBtn:hover {
    background-color: #a8d654;
}

/* --- FILTRES RÉCAPITULATIF --- */
QPushButton#FilterBtn {
    background-color: transparent;
    color: #666;
    font-weight: bold;
    font-size: 10px;
    border: none;
    padding: 8px 15px;
    border-radius: 12px;
}

QPushButton#FilterBtn:hover {
    color: #96bf48;
    background-color: #141d14;
}

QPushButton#FilterBtn[active="true"] {
    background-color: #96bf48;
    color: #0b0f0a;
}

/* Cartes Récapitulatif */
QFrame#WhiteCard {
    background-color: #141d14;
    border-radius: 25px;
    border: 1px solid #1f2a1f;
}

/* Labels Généraux */
QLabel { 
    color: #666; 
    font-size: 11px; 
}

QLabel#Title { 
    color: white; 
    font-size: 24px; 
    font-weight: bold; 
}

/* Tableaux */
QTableWidget {
    background-color: transparent;
    border: none;
    gridline-color: #1f2a1f;
    color: #bbb;
}

QHeaderView::section {
    background-color: transparent;
    color: #444;
    border: none;
    font-weight: bold;
    font-size: 10px;
    padding: 5px;
}
"""