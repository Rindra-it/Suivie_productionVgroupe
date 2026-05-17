import sys
from PyQt6.QtWidgets import (QApplication, QInputDialog, QMainWindow, QMessageBox, QWidget, 
                             QHBoxLayout, QVBoxLayout, QPushButton, 
                             QStackedWidget, QFrame, QLabel)
from PyQt6.QtCore import Qt

from database import setup_database
from styles import DARK_THEME
from database import (get_all_workers, get_recent_suggestions, save_production, 
                      get_aggregated_production, get_worker_stats, save_worker,
                      get_dashboard_data, get_all_styles, add_style_to_repo, delete_style, update_style_code) 
from views.dashboard_view import DashboardView
from views.input_view import InputView
from views.recap_view import RecapView
from views.worker_view import AddWorkerDialog, WorkerView 
from views.style_view import StyleManagementView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("INCONNNUE - Suivie de production")
        self.resize(1280, 850)
        self.setStyleSheet(DARK_THEME)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(15, 30, 0, 20)
        sidebar_layout.setSpacing(5)

        logo = QLabel("INCONNUES")
        logo.setStyleSheet("color: #96bf48; font-size: 22px; font-weight: bold;")
        sidebar_layout.addWidget(logo)
        
        sub_logo = QLabel("SUIVIE DE PRODUCTION")
        sub_logo.setStyleSheet("color: #444; font-size: 9px; font-weight: bold; margin-bottom: 30px;")
        sidebar_layout.addWidget(sub_logo)

        def add_section_label(text):
            lbl = QLabel(text)
            lbl.setStyleSheet("color: #444; font-weight: bold; margin-top: 15px; margin-left: 5px; font-size: 10px;")
            sidebar_layout.addWidget(lbl)

        add_section_label("PRINCIPAL")
        self.btn_dash = self.create_nav_button("  Dashboard")
        self.btn_saisie = self.create_nav_button("  Saisie")
        sidebar_layout.addWidget(self.btn_dash)
        sidebar_layout.addWidget(self.btn_saisie)

        add_section_label("RAPPORTS")
        self.btn_recap = self.create_nav_button("  Récapitulatif")
        self.btn_graph = self.create_nav_button("  Graphiques")
        sidebar_layout.addWidget(self.btn_recap)
        sidebar_layout.addWidget(self.btn_graph)

        add_section_label("ADMINISTRATION")
        self.btn_emp = self.create_nav_button("  Employés")
        self.btn_styles = self.create_nav_button("  Configuration Styles")
        self.btn_sal = self.create_nav_button("  Salaires")
        sidebar_layout.addWidget(self.btn_emp)
        sidebar_layout.addWidget(self.btn_styles)
        sidebar_layout.addWidget(self.btn_sal)

        self.menu_buttons = [self.btn_dash, self.btn_saisie, self.btn_recap, 
                            self.btn_graph, self.btn_emp, self.btn_styles, self.btn_sal]

        sidebar_layout.addStretch()

        self.user_info = QFrame()
        self.user_info.setStyleSheet("background-color: #141d14; border-radius: 12px; padding: 10px; border: none; margin-right: 10px;")
        user_layout = QHBoxLayout(self.user_info)
        avatar = QLabel("AD")
        avatar.setFixedSize(35, 35)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet("background-color: #96bf48; color: #0b0f0a; border-radius: 17px; font-weight: bold;")

        self.content_area = QStackedWidget()
        
        self.dash_page = DashboardView()
        self.input_page = InputView()
        self.recap_page = RecapView()
        self.worker_page = WorkerView() 
        self.style_page = StyleManagementView()

        self.content_area.addWidget(self.dash_page)
        self.content_area.addWidget(self.input_page)
        self.content_area.addWidget(self.recap_page)
        self.content_area.addWidget(self.worker_page)
        self.content_area.addWidget(self.style_page)
        
        main_layout.addWidget(self.sidebar, 1)
        main_layout.addWidget(self.content_area, 5)

        self.btn_dash.clicked.connect(self.show_dashboard)
        self.btn_saisie.clicked.connect(self.show_saisie)
        self.btn_recap.clicked.connect(self.show_recap)
        self.btn_emp.clicked.connect(self.show_worker_page) 
        self.btn_styles.clicked.connect(self.show_style_page)
        
        self.style_page.btn_add_style.clicked.connect(self.handle_add_style)
        self.input_page.btn_valid.clicked.connect(self.handle_save_production)
        self.worker_page.btn_open_add.clicked.connect(self.open_add_worker_dialog)
        self.worker_page.search_input.textChanged.connect(self.handle_search_worker)
        
        self.recap_page.btn_all.clicked.connect(lambda: self.refresh_recap("all"))
        self.recap_page.btn_day.clicked.connect(lambda: self.refresh_recap("day"))
        self.recap_page.btn_week.clicked.connect(lambda: self.refresh_recap("week"))
        self.recap_page.btn_month.clicked.connect(lambda: self.refresh_recap("month"))

        self.refresh_ui_data()
        self.show_dashboard()


    def create_nav_button(self, text):
        btn = QPushButton(text)
        btn.setObjectName("MenuButton")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setCheckable(True) 
        return btn

    def set_active_menu(self, active_btn):
        for btn in self.menu_buttons:
            btn.setChecked(btn == active_btn)
            btn.setProperty("active", "true" if btn == active_btn else "false")
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def show_dashboard(self):
        self.set_active_menu(self.btn_dash)
        data = get_dashboard_data()
        self.dash_page.update_dashboard(data)
        self.content_area.setCurrentWidget(self.dash_page)

    def show_saisie(self):
        self.set_active_menu(self.btn_saisie)
        self.content_area.setCurrentWidget(self.input_page)
        self.refresh_ui_data()

    def show_recap(self):
        self.set_active_menu(self.btn_recap)
        self.content_area.setCurrentWidget(self.recap_page)
        self.refresh_recap("all")

    def show_worker_page(self):
        self.set_active_menu(self.btn_emp)
        self.content_area.setCurrentWidget(self.worker_page)
        self.worker_page.update_table(get_all_workers())

    def show_style_page(self):
        self.set_active_menu(self.btn_styles)
        self.content_area.setCurrentWidget(self.style_page)
        self.refresh_styles_list()

    # ── Styles ──────────────────────────────────────────────────────────────

    def handle_add_style(self):
        code = self.style_page.input_new_style.text().strip()
        if code:
            if add_style_to_repo(code):
                self.style_page.input_new_style.clear()
                self.refresh_styles_list()

    def refresh_styles_list(self):
        """Unique définition — recharge et passe les deux callbacks."""
        data = get_all_styles()
        self.style_page.update_table(data, self.handle_edit_style, self.handle_delete_style)
        self.style_page.table_styles.viewport().update()

    def handle_delete_style(self, style_code):
        confirm = QMessageBox.question(
            self, "Supprimer", f"Supprimer le style « {style_code} » ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            if delete_style(style_code):
                self.refresh_styles_list()
            else:
                QMessageBox.warning(self, "Erreur", f"Impossible de supprimer {style_code}.")

    def handle_edit_style(self, old_code):
        new_code, ok = QInputDialog.getText(
            self, "Modifier le style", "Nouveau code :", text=old_code
        )
        if ok and new_code.strip():
            if update_style_code(old_code, new_code.strip().upper()):
                self.refresh_styles_list()
            else:
                QMessageBox.warning(self, "Erreur", f"Impossible de modifier {old_code}.")

    # ── Employés ─────────────────────────────────────────────────────────────

    def open_add_worker_dialog(self):
        dialog = AddWorkerDialog(self)
        if dialog.exec(): 
            mat = dialog.input_mat.text().strip().upper()
            nom = dialog.input_nom.text().strip().upper()
            pre = dialog.input_prenom.text().strip()
            if mat and nom:
                if save_worker(mat, nom, pre):
                    self.worker_page.update_table(get_all_workers())

    def handle_search_worker(self):
        query = self.worker_page.search_input.text().lower()
        table = self.worker_page.table_workers
        for row in range(table.rowCount()):
            match = any(
                query in (table.item(row, col).text().lower() if table.item(row, col) else "")
                for col in range(3)
            )
            table.setRowHidden(row, not match)

    # ── Production ───────────────────────────────────────────────────────────

    def handle_save_production(self):
        date_p = self.input_page.date.date().toPyDate()
        mat = self.input_page.matricule.text().strip()
        sty = self.input_page.style.text().strip()
        et = self.input_page.etat.currentText()
        ca = self.input_page.cat.currentText()
        qy = self.input_page.qty.value()
        tk = self.input_page.ticket.text().strip()

        if not mat or not sty or qy <= 0:
            return

        if save_production(date_p, mat, sty, et, ca, qy, tk):
            self.input_page.qty.setValue(0)
            self.input_page.ticket.clear()
            self.refresh_ui_data()
        else:
            QMessageBox.warning(self, "Erreur", "Impossible d'enregistrer la production.")

    def refresh_ui_data(self):
        mats = get_recent_suggestions("matricule")
        stys = get_recent_suggestions("code_style")
        self.input_page.set_suggestions(mats, stys)
        if self.input_page.etat.count() == 0:
            self.input_page.etat.addItems(["PROD", "SMS", "REJECT"])
        if self.input_page.cat.count() == 0:
            self.input_page.cat.addItems(["Manche", "Colar", "Other"])

    # ── Récapitulatif ────────────────────────────────────────────────────────

    def refresh_recap(self, filter_type):
        style_data = get_aggregated_production(filter_type)
        worker_data = get_worker_stats(filter_type)
        self.recap_page.update_table(style_data)
        
        while self.recap_page.worker_list_area.count():
            child = self.recap_page.worker_list_area.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for row in worker_data:
            if len(row) >= 2:
                self.recap_page.add_worker_card(row[0], row[1], row[2] if len(row) > 2 else 0)


if __name__ == "__main__":
    setup_database()
    app = QApplication(sys.argv)
    try:
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        import traceback
        traceback.print_exc()