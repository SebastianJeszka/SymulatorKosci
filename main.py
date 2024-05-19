import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QListWidget, QMessageBox, QListWidgetItem
from dice import Dice
from diceroller import DiceRoller

class DiceApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dice_roller = DiceRoller()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Symulator Rzutu Kośćmi")
        self.setGeometry(100, 100, 400, 600)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #F3F4F6;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333;
            }
            QPushButton {
                font-size: 14px;
                font-weight: bold;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton#AddButton {
                background-color: #4CAF50;
                color: white;
            }
            QPushButton#AddButton:hover {
                background-color: #45A049;
            }
            QPushButton#RemoveButton {
                background-color: #FF7F7F;
                color: white;
            }
            QPushButton#RemoveButton:hover {
                background-color: #FF6A6A;
            }
            QPushButton#RollButton {
                background-color: #5DADE2;
                color: white;
            }
            QPushButton#RollButton:hover {
                background-color: #4D9DE0;
            }
            QListWidget {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                background-color: #FFF;
            }
        """)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        vbox = QVBoxLayout()

        self.lst_dice = QListWidget()
        vbox.addWidget(QLabel("Pula Kości:"))
        vbox.addWidget(self.lst_dice)

        for sides in [4, 6, 8, 10, 12, 20]:
            btn = QPushButton(f"Dodaj D{sides}")
            btn.setObjectName("AddButton")
            btn.clicked.connect(lambda _, s=sides: self.add_dice(s))
            vbox.addWidget(btn)

        btn_remove_dice = QPushButton("Usuń wybraną kość")
        btn_remove_dice.setObjectName("RemoveButton")
        btn_remove_dice.clicked.connect(self.remove_dice)
        vbox.addWidget(btn_remove_dice)

        btn_roll_dice = QPushButton("Rzuć kośćmi")
        btn_roll_dice.setObjectName("RollButton")
        btn_roll_dice.clicked.connect(self.roll_dice)
        vbox.addWidget(btn_roll_dice)

        central_widget.setLayout(vbox)

    def add_dice(self, sides):
        dice = Dice(sides)
        if not self.dice_roller.addDice(dice):
            QMessageBox.warning(self, "Ostrzeżenie", "Maksymalna liczba kości (12) została osiągnięta.")
        self.update_dice_pool()

    def remove_dice(self):
        selected_dice = self.lst_dice.currentRow()
        if selected_dice != -1:
            self.dice_roller.delDice(selected_dice)
            self.update_dice_pool()
        else:
            QMessageBox.information(self, "Informacja", "Wybierz kość do usunięcia.")

    def update_dice_pool(self):
        self.lst_dice.clear()
        for dice in self.dice_roller.dice_pool:
            item = QListWidgetItem()
            label = QLabel(f"Kość {dice.sides}-ścienna")
            label.setStyleSheet("font-size: 18px;")
            self.lst_dice.addItem(item)
            self.lst_dice.setItemWidget(item, label)
            item.setSizeHint(label.sizeHint())

    def roll_dice(self):
        if not self.dice_roller.dice_pool:
            QMessageBox.critical(self, "Błąd", "Nie dodano żadnych kości.")
            return 

        try:
            results = self.dice_roller.rollAllDice()
            QMessageBox.information(self, "Wyniki", self.dice_roller.showResult(results))
            self.ask_repeat()
        except Exception as e:
            QMessageBox.critical(self, "Błąd", "Wystąpił błąd podczas rzucania kośćmi: " + str(e))

    def ask_repeat(self):
        answer = QMessageBox.question(self, "Pytanie", "Czy chcesz rzucić ponownie?")
        if answer == QMessageBox.Yes:
            self.roll_dice()
        else:
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DiceApp()
    ex.show()
    sys.exit(app.exec_())
