import sys, crud
from main import form_groups, ROLES
from PyQt5.QtWidgets import QMainWindow, QDialog, QLabel, QLineEdit, QPushButton, QListWidget, QDialogButtonBox, QVBoxLayout, QGridLayout, QWidget, QAbstractItemView, QComboBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


STYLE_SHEET = """
QMainWindow{
    background-color: hsl(241, 46%, 35%);
}

QWidget{
    background-color: hsl(241, 46%, 35%);
}
QListWidget{
    font-family: 'Elephant';
    font: bold 24px;
    color: green;
}
QLabel{
    background-color: hsl(241, 79%, 35%);
    font-family: 'Informal Roman';
    font: bold 44px;
    color: white;
    padding: 8;
    border: 4px solid;
}
QLabel#Empty{
    background: rgba(255, 0, 0, 0);
    border: 0px;
}

QLabel#Header{
    background-color: hsl(241, 79%, 35%);
    font: bold 40px;
    font-family: 'Elephant';
    color: yellow;
    padding: 8px;
    margin: 10px;
    border: 4px solid;
    max-height: 50px;
}

QComboBox{
    height: 55px;
    width: 50px;
    color: hsl(134, 77%, 36%);
    padding: 5px;
    margin: 10px;
    
    font-family: 'Elephant';
    font: bold 28px;
    padding: 8;
}

QComboBox#LongBox{
    width: 150px;
}

QLineEdit{
    height: 50px;
    color: hsl(55, 92%, 40%);
    font-family: 'Elephant';
    
    font-size: 28px;
    padding: 4px;
    border: 4px solid;
    border-radius: 8px;
}

QPushButton#CentralButtons{
    background-color: hsl(241, 96%, 35%);
    color: white;
    font-family: 'Informal Roman';
    font-weight: bold;
    font-size: 56px;
    padding: 12px;
    margin: 4px;
    border: 4px solid;
    border-radius: 12px;
}
QPushButton#CentralButtons:hover{
    background-color: hsl(241, 96%, 55%);
    color: hsl(55, 92%, 40%);
}

QPushButton#UserButtons{
    background-color: hsl(241, 96%, 35%);
    color: yellow;
    font-family: 'Elephant';
    font-weight: bold;
    font-size: 24px;
    padding: 12px;
    margin: 4px;
    border: 4px solid;
    border-radius: 12px;
}
QPushButton#UserButtons:hover{
    background-color: hsl(241, 96%, 55%);
    color: hsl(55, 92%, 40%);
}

QPushButton#ExitButtons{
    background-color: hsl(7, 96%, 35%);
    color: white;
    font-family: 'Elephant';
    
    font-size: 20px;
    padding: 4px;
    border: 4px solid;
    border-radius: 8px;
}
QPushButton#ExitButtons:hover{
    background-color: hsl(7, 96%, 55%);
}
"""


TITLE: str = "Throne and Liberty - Automatischer Gruppenbilder"


DATABASEWINDOW_WIDTH: int = 1100
DATABASEWINDOW_HEIGHT: int = 800
DATABASEWINDOW_HEADER: str = "Datenbankverwaltung"

MAINWINDOW_WIDTH: int = 1100
MAINWINDOW_HEIGHT: int = 800
MAINWINDOW_HEADER: str = " Gruppenverwaltung"


SEPARATOR: str = " || "
SEPARATOR_LENGTH: int = 4


class ConfirmDialog(QDialog):
    def __init__(self, title: str, message: str):
        super().__init__()
        self.setWindowTitle(title)
        
        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        
        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        mssg = QLabel(message)
        mssg.setFont(QFont("Arial", 10))
        mssg.setAlignment(Qt.AlignCenter)
        
        layout = QVBoxLayout()
        layout.addWidget(mssg)
        layout.addWidget(self.buttonBox)
        
        self.setLayout(layout)

class OkDialog(QDialog):
    def __init__(self, title: str, message: str):
        super().__init__()
        self.setWindowTitle(title)
        
        button = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(button)
        self.buttonBox.accepted.connect(self.accept)
        
        mssg = QLabel(message)
        mssg.setFont(QFont("Arial", 10))
        mssg.setAlignment(Qt.AlignCenter)
        
        layout = QVBoxLayout()
        layout.addWidget(mssg)
        layout.addWidget(self.buttonBox)
        
        self.setLayout(layout)



class DatabaseWindow(QWidget):
    def __init__(self, parent):
        self.parent = parent
        super().__init__()
        self.setWindowTitle(TITLE)
        self.setFixedSize(DATABASEWINDOW_WIDTH, DATABASEWINDOW_HEIGHT)
        self.setStyleSheet(STYLE_SHEET)
        
        self.lbl_Header = QLabel(DATABASEWINDOW_HEADER)
        self.lbl_Character = QLabel("Charakter", self)
        self.lbl_Role = QLabel("Rolle", self)
        self.lbl_Empty_1 = QLabel(self)
        self.lbl_Empty_2 = QLabel(self)
        
        self.txtBox_Character = QLineEdit(self)
        self.cmbBox_Role = QComboBox(self)
        
        self.list_Members = QListWidget(self)
        
        self.btn_Add_Member = QPushButton("Hinzufügen", self)
        self.btn_Edit_Member = QPushButton("Aktualisieren", self)
        self.btn_Delete_Member = QPushButton("Entfernen", self)
        
        self.btn_Back = QPushButton("Zurück", self)
        self.btn_Exit = QPushButton("Beenden", self)
        
        self.initUI()
        
    def initUI(self):
        self.lbl_Header.setAlignment(Qt.AlignCenter)
        self.lbl_Header.setObjectName("Header")
        self.lbl_Empty_1.setObjectName("Empty")
        self.lbl_Empty_2.setObjectName("Empty")
        
        self.list_Members.itemClicked.connect(self.select_member)
        
        self.cmbBox_Role.addItems(["Tank", "Heal", "DPS"])
        
        self.btn_Add_Member.clicked.connect(self.add_member)
        self.btn_Add_Member.setObjectName("UserButtons")
        self.btn_Edit_Member.clicked.connect(self.edit_member)
        self.btn_Edit_Member.setObjectName("UserButtons")
        self.btn_Delete_Member.clicked.connect(self.delete_member)
        self.btn_Delete_Member.setObjectName("UserButtons")
        
        self.btn_Back.clicked.connect(self.back)
        self.btn_Back.setObjectName("ExitButtons")
        self.btn_Exit.clicked.connect(self.exit_app)
        self.btn_Exit.setObjectName("ExitButtons")
        
        gBox = QGridLayout()
        gBox.addWidget(self.lbl_Header, 0, 1, 1, 7)
        #gBox.addWidget(self.lbl_Empty_1, 1, 1)
        gBox.addWidget(self.list_Members, 2, 1, 9, 4)
        gBox.addWidget(self.lbl_Character, 3, 5, 1, 3)
        gBox.addWidget(self.txtBox_Character, 4, 5, 1, 3)
        gBox.addWidget(self.lbl_Role, 6, 5, 1, 3)
        gBox.addWidget(self.cmbBox_Role, 7, 5, 1, 3)
        gBox.addWidget(self.btn_Add_Member, 8, 6, 1, 1)
        gBox.addWidget(self.btn_Edit_Member, 9, 6, 1, 1)
        gBox.addWidget(self.btn_Delete_Member, 10, 6, 1, 1)
        gBox.addWidget(self.lbl_Empty_2, 11, 1)
        gBox.addWidget(self.btn_Back, 12, 1, 1, 1)
        gBox.addWidget(self.btn_Exit, 12, 7, 1, 1)
        self.setLayout(gBox)
        
        self.load_database()
        
        
    def load_database(self):
        players: dict = crud.read_players()
        for player, role in players.items():
            self.list_Members.addItem(f"{player} || {role}")
    
    def select_member(self, item):
        selected_member: str = item.text()
        end: int = selected_member.index(SEPARATOR)
        selected_member_name: str = selected_member[:end]
        selected_member_role: str = selected_member[end+SEPARATOR_LENGTH:]
        cmbBox_index: int = self.cmbBox_Role.findText(selected_member_role)
        self.txtBox_Character.setText(selected_member_name)
        self.cmbBox_Role.setCurrentIndex(cmbBox_index)
    
    
    def add_member(self):
        try:
            name: str = self.txtBox_Character.text()
            
            for key, value in ROLES.items():
                if self.cmbBox_Role.currentText() == value:
                    role: int = key
            
            crud.add_player(name, role)
            self.txtBox_Character.clear()
            self.list_Members.clear()
            self.load_database()
            
        except:
            dlg = OkDialog("Error", "Da lief wohl etwas schief!\n Ist der Spieler bereits in der Datenbank vorhanden?")
            dlg.exec_()
    
    def edit_member(self):
        character: str = self.txtBox_Character.text()
        role_box: str = self.cmbBox_Role.currentText()
        
        for key, value in ROLES.items():
            if role_box == value:
                role: int = key
        
        crud.update_player(role, character)
        self.list_Members.clear()
        self.load_database()
    
    def delete_member(self):
        character: str = self.txtBox_Character.text()
        dlg = ConfirmDialog("Entfernen", f"Soll {character} aus der Datenbank entfernt werden?")
        if dlg.exec_():
            crud.delete_player(character)
            self.txtBox_Character.clear()
            self.list_Members.clear()
            self.load_database()
    
    
    def back(self):
        self.parent.__init__()
        self.parent.show()
        self.close()
        self = None
        
    def exit_app(self):
        dlg = ConfirmDialog("Exit", "Exit the application?")
        if dlg.exec_():
            sys.exit()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(TITLE)
        self.setFixedSize(MAINWINDOW_WIDTH, MAINWINDOW_HEIGHT)
        self.setStyleSheet(STYLE_SHEET)
        
        self.lbl_Header = QLabel(MAINWINDOW_HEADER, self)
        self.txtBox_Minimum_Tanks = QLineEdit(self)
        self.lbl_Minimum_Tanks = QLabel("Minimum Tanks", self)
        self.txtBox_Minimum_Heals = QLineEdit(self)
        self.lbl_Minimum_Heals = QLabel("Minimum Heals", self)
        self.list_Available_Players = QListWidget(self)
        self.btn_Select_Player = QPushButton("Auswählen", self)
        self.list_Selected_Players = QListWidget(self)
        self.btn_Form_Groups = QPushButton("Gruppen erstellen", self)
        self.btn_Database = QPushButton("Datenbank", self)
        self.btn_Exit = QPushButton("Beenden", self)
        
        self.initUI()
        
    def initUI(self):
        self.lbl_Header.setAlignment(Qt.AlignCenter)
        self.lbl_Header.setObjectName("Header")
        
        self.list_Available_Players.setSelectionMode(QAbstractItemView.MultiSelection)
        
        self.btn_Select_Player.clicked.connect(self.select_player)
        self.btn_Select_Player.setObjectName("UserButtons")
        self.btn_Form_Groups.clicked.connect(self.form_groups)
        self.btn_Form_Groups.setObjectName("UserButtons")
        self.btn_Database.clicked.connect(self.show_database)
        self.btn_Database.setObjectName("ExitButtons")
        self.btn_Exit.clicked.connect(self.exit_app)
        self.btn_Exit.setObjectName("ExitButtons")

        gBox = QGridLayout()
        gBox.addWidget(self.lbl_Header, 1, 3, 1, 5)
        #gBox.addWidget(self.txtBox_Minimum_Tanks, 2, 2, 1, 1)
        #gBox.addWidget(self.lbl_Minimum_Tanks, 2, 3, 1, 2)
        #gBox.addWidget(self.txtBox_Minimum_Heals, 2, 6, 1, 1)
        #gBox.addWidget(self.lbl_Minimum_Heals, 2, 7, 1, 2)
        gBox.addWidget(self.list_Available_Players, 3, 1, 5, 4)
        gBox.addWidget(self.btn_Select_Player, 5, 5, 1, 1)
        gBox.addWidget(self.list_Selected_Players, 3, 6, 5, 4)
        gBox.addWidget(self.btn_Form_Groups, 8, 4, 1, 3)
        gBox.addWidget(self.btn_Database, 9, 2, 1, 1)
        gBox.addWidget(self.btn_Exit, 9, 8, 1, 1)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(gBox)
        
        self.load_database()
    
    
    def load_database(self):
        players: dict = crud.read_players()
        for key, value in players.items():
            self.list_Available_Players.addItem(key)

    
    def select_player(self):
        selection: str = self.list_Available_Players.selectedItems()
        selected_player = [item.text() for item in selection]
        for player in selected_player:
            self.list_Selected_Players.addItem(player)
        
        for item in self.list_Available_Players.selectedItems():
            row = self.list_Available_Players.row(item)
            self.list_Available_Players.takeItem(row)
            del row

    def form_groups(self):  # Replace function once finished testing --> put selected players in lists and start function in main-file
        players: list = []
        for i in range(self.list_Selected_Players.count()):
            players.append(self.list_Selected_Players.item(i).text())
            
        tanks: list = []
        heals: list = []
        dps: list = []
        
        for name in players:
            player = crud.get_single_player(name)
            if player[1] == 1:
                tanks.append(player[0])
            elif player[1] == 2:
                heals.append(player[0])
            elif player[1] == 3:
                dps.append(player[0])
        
        grouplist: list = form_groups(tanks, heals, dps)
        groups: str = ""
        for i, group in enumerate(grouplist, 1):
            groups += f"Group#{i}:\n{group}\n\n"
            
        dlg = OkDialog("Success", groups)
        dlg.exec_()
    
    
    def show_database(self):
        self.new_window = DatabaseWindow(self)
        self.hide()
        self.new_window.show()
    
    def exit_app(self):
        dlg = ConfirmDialog("Exit", "Exit the application?")
        if dlg.exec_():
            sys.exit()
