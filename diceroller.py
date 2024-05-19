import tkinter as tk
from tkinter import messagebox

class DiceRoller:
    def __init__(self):
        self.dice_pool = []

    def addDice(self, dice):
        if len(self.dice_pool) < 12:
            self.dice_pool.append(dice)
            return True
        return False

    def delDice(self, index):
        if 0 <= index < len(self.dice_pool):
            del self.dice_pool[index]
            return True
        return False

    def rollAllDice(self):
        return [dice.roll() for dice in self.dice_pool]

    def showResult(self, results):
        return "\n".join(f"Kość {index+1}: {result}" for index, result in enumerate(results))

    def checkErrors(self):
        if not self.dice_pool:
            return "Nie ma kości do rzucenia. Dodaj kości do puli."
        elif len(self.dice_pool) > 12:
            return "Zbyt wiele kości w puli. Maksymalna liczba to 12."
        return None

    def repeatRoll(self, root, roll_dice):
        answer = messagebox.askyesno("Pytanie", "Czy chcesz rzucić ponownie?")
        if answer:
            roll_dice()
        else:
            if messagebox.askyesno("Pytanie", "Czy chcesz zmodyfikować pulę kości?"):
                return
            else:
                root.quit()
