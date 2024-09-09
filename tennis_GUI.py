import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QRadioButton,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
)
from PyQt5.QtGui import QPixmap
import qdarkstyle
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QTimer, QDateTime, pyqtSignal
import json

class Tennis_competition(QWidget):

    def __init__(self):
        # everything in self scope is required to be named the same
        super().__init__()

        with open("players.json","r") as f:
            self.players = dict(json.load(f))

        # set window title - add code below
        self.setWindowTitle("Serve Strategist")
        # Widgets - add code below
        self.description = QLabel('In tennis, a player gets 2 chances to get their serve in to start off the point. Typically, a player will hit their first serve aggressively, and their second serve will be significantly weaker. A weak second serve is easier to attack, hence giving the opponent a significant advantage in the point. Using statistics from players on the ATP tour, we have found that some players will benefit from hitting 2 first serves (both of them at maximum intensity) rather than a first serve and a second serve.')
        self.instructions = QLabel('Select two players to see which serving strategy is optimal for them in this specific match and their overall game.')
        self.player1 = QComboBox()
        self.player1.addItems(self.players.keys())
        self.player2 = QComboBox()
        self.player2.addItems(self.players.keys())
        self.image1 = QLabel()
        self.image2 = QLabel()
        self.image1.setPixmap(QPixmap(f'{self.player1.currentText()}.png'))
        self.image2.setPixmap(QPixmap(f'{self.player2.currentText()}.png'))
        self.head_to_head = QLabel("Serve Strategist")
        individual_percentage = self.individual_serve_strategy(self.players[self.player1.currentText()])
        self.usual1 = QLabel(f'- {self.player1.currentText()}\'s chance of winning overall will benefit by {round(abs(individual_percentage)*100,2)}% if he {"does 2 first serves." if individual_percentage>0 else "sticks to doing a second serve."}')
        individual_percentage = self.individual_serve_strategy(self.players[self.player2.currentText()])
        self.usual2 = QLabel(f'- {self.player2.currentText()}\'s chance of winning overall will benefit by {round(abs(individual_percentage)*100,2)}% if he {"does 2 first serves." if individual_percentage>0 else "sticks to doing a second serve."}')
        competitor_percentage = self.competitor_serve_strategy(self.players[self.player1.currentText()], self.players[self.player2.currentText()])
        self.specific1 = QLabel(f'- {self.player1.currentText()}\'s chance of winning against {self.player2.currentText()} specifically will benefit by {round(abs(competitor_percentage)*100,2)}% if he {"does 2 first serves." if competitor_percentage>0 else "sticks to doing a second serve."}')
        competitor_percentage = self.competitor_serve_strategy(self.players[self.player2.currentText()], self.players[self.player1.currentText()])
        self.specific2 = QLabel(f'- {self.player2.currentText()}\'s chance of winning against {self.player1.currentText()} specifically will benefit by {round(abs(competitor_percentage)*100,2)}% if he {"does 2 first serves." if competitor_percentage>0 else "sticks to doing a second serve."}')
        self.add_player = QPushButton("Add New Player")

        #Styling
        self.head_to_head.setStyleSheet("color: green;"
            "background-color: #E0E0E0;"
            "border: 3px outset black;"
            "font-size: 40px;"
            'font-family: "Garamond", Times, serif;'
            "font-weight: bold;")
        self.description.setStyleSheet("color: black;"
            "font-size: 28px;"
            'font-family: "Garamond", Times, serif;'
            # "background-color: #E0E0E0;"
            # "border: 5px outset #A9BA9D;"
            )
        self.instructions.setStyleSheet("font-size: 28px;"
            'font-family: "Garamond", Times, serif;')
        self.player1.setStyleSheet("color: blue;"
            #"background-color: white;")
            )
        self.player2.setStyleSheet("color: blue;"
            #"background-color: white;")
            )
        self.usual1.setStyleSheet("font-size: 24px;")
        self.usual2.setStyleSheet("font-size: 24px;")
        self.specific1.setStyleSheet("font-size: 24px;")
        self.specific2.setStyleSheet("font-size: 24px;")


        #self.setStyleSheet("background-color: #A9BA9D;")



        #Formatting
        self.specific2.setWordWrap(True)
        self.specific1.setWordWrap(True)
        self.usual2.setWordWrap(True)
        self.usual1.setWordWrap(True)
        self.instructions.setWordWrap(True)
        self.description.setWordWrap(True)
        self.head_to_head.setAlignment(Qt.AlignCenter)
        self.description.setAlignment(Qt.AlignCenter)
        self.instructions.setAlignment(Qt.AlignCenter)

        # Connections - add code below
        self.player1.currentIndexChanged.connect(self.player_changed)
        self.player2.currentIndexChanged.connect(self.player_changed)
        self.add_player.clicked.connect(self.show_second_window)
        
        #Data

        ####################################
        # Layout
        self.outer = QVBoxLayout()

        self.outer.addWidget(self.head_to_head)
        self.outer.addWidget(self.description)
        self.outer.addWidget(self.instructions)
        

        #Level 1
        self.level_1 = QHBoxLayout()
        #Level 1 L
        self.level_1L = QVBoxLayout()
        self.level_1L.addWidget(self.image1)
        self.level_1L.addWidget(self.player1)
        self.level_1L.addWidget(self.specific1)
        self.level_1L.addWidget(self.usual1)

        self.level_1.addLayout(self.level_1L)

        #Level 1 R
        self.level_1R = QVBoxLayout()
        self.level_1R.addWidget(self.image2)
        self.level_1R.addWidget(self.player2)
        self.level_1R.addWidget(self.specific2)
        self.level_1R.addWidget(self.usual2)

        self.level_1.addLayout(self.level_1R)

        self.outer.addLayout(self.level_1)
        self.outer.addWidget(self.add_player)

        

        # Set Layout
        self.setLayout(self.outer)

        #SECOND WINDOW
        # Create an instance of SecondWindow
        self.second_window = AdderWindow()

        # Connect the signal from SecondWindow to a slot in MainWindow
        self.second_window.information_sent.connect(self.receive_information)
        

        ####################################
        # Initial Text Entry & Button Status
        

    ########################################

    #FUNCTIONS



    def receive_information(self, information):
        self.players[information[0]] = information[1]
        self.player1.addItem(information[0])
        self.player2.addItem(information[0])



    def show_second_window(self):
        self.second_window.show()

    def player_changed(self):
        player = self.player1.currentText()
        competitor_percentage = self.competitor_serve_strategy(self.players[player], self.players[self.player2.currentText()])
        self.specific1.setText(f'- {player}\'s chance of winning against {self.player2.currentText()} specifically will benefit by {round(abs(competitor_percentage)*100,2)}% if he {"does 2 first serves." if competitor_percentage>0 else "sticks to doing a second serve."}')
        individual_percentage = self.individual_serve_strategy(self.players[player])
        self.usual1.setText(f'- {player}\'s chance of winning overall will benefit by {round(abs(individual_percentage)*100,2)}% if he {"does 2 first serves." if individual_percentage>0 else "sticks to doing a second serve."}')
        player = self.player2.currentText()
        competitor_percentage = self.competitor_serve_strategy(self.players[player], self.players[self.player1.currentText()])
        self.specific2.setText(f'- {player}\'s chance of winning against {self.player1.currentText()} specifically will benefit by {round(abs(competitor_percentage)*100,2)}% if he {"does 2 first serves." if competitor_percentage>0 else "sticks to doing a second serve."}')
        individual_percentage = self.individual_serve_strategy(self.players[player])
        self.usual2.setText(f'- {player}\'s chance of winning overall will benefit by {round(abs(individual_percentage)*100,2)}% if he {"does 2 first serves." if individual_percentage>0 else "sticks to doing a second serve."}')
        if self.player1.currentText() in ["Novak Djokovic","Andrey Rublev","Carlos Alcaraz","Daniil Medvedev","Jannik Sinner"]:
            self.image1.setPixmap(QPixmap(f'{self.player1.currentText()}.png'))
        else:
            self.image1.setPixmap(QPixmap('stock.png'))
        if self.player2.currentText() in ["Novak Djokovic","Andrey Rublev","Carlos Alcaraz","Daniil Medvedev","Jannik Sinner"]:
            self.image2.setPixmap(QPixmap(f'{self.player2.currentText()}.png'))
        else:
            self.image2.setPixmap(QPixmap('stock.png'))


    def individual_serve_strategy(self, player):
        second_serve = player["sp1"]*player["sw1"]+(1-player["sp1"])*player["sp2"]*player["sw2"]
        first_serve = player["sp1"]*player["sw1"]+(1-player["sp1"])*player["sp1"]*player["sw1"]
        return(first_serve-second_serve)

    def competitor_serve_strategy(self, serving_player, returning_player):
        second_serve = serving_player["sp1"]*(1-returning_player['rp1']) + serving_player["sp1"]*returning_player['rp1']*(1-returning_player["rw1"]) + (1-serving_player["sp1"])*serving_player["sp2"]*(1-returning_player["rp2"]) + (1-serving_player["sp1"])*serving_player["sp2"]*returning_player["rp2"]*(1-returning_player["rw2"])
        first_serve = serving_player["sp1"]*(1-returning_player['rp1']) + serving_player["sp1"]*returning_player['rp1']*(1-returning_player["rw1"]) + (1-serving_player["sp1"])*serving_player["sp1"]*(1-returning_player["rp1"]) + (1-serving_player["sp1"])*serving_player["sp1"]*returning_player["rp1"]*(1-returning_player["rw1"])
        return(first_serve-second_serve)

class AdderWindow(QWidget):
    # Define a signal to send information
    information_sent = pyqtSignal(tuple)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add new player")

        # Create a button to send information
        self.name1 = QLabel("Name: ")
        self.name2 = QLineEdit()
        self.sp1a = QLabel("Percentage of first serves in play (decimal form): ")
        self.sp1b = QLineEdit()
        self.sw1a = QLabel("Percentage of first serves won (decimal form): ")
        self.sw1b = QLineEdit()
        self.sp2a = QLabel("Percentage of second serves in play (decimal form): ")
        self.sp2b = QLineEdit()
        self.sw2a = QLabel("Percentage of second serves won (decimal form): ")
        self.sw2b = QLineEdit()
        self.rp1a = QLabel("Percentage of first serve returns in play (decimal form): ")
        self.rp1b = QLineEdit()
        self.rw1a = QLabel("Percentage of first serve returns won (decimal form): ")
        self.rw1b = QLineEdit()
        self.rp2a = QLabel("Percentage of second serve returns in play (decimal form): ")
        self.rp2b = QLineEdit()
        self.rw2a = QLabel("Percentage of second serve returns won (decimal form): ")
        self.rw2b = QLineEdit()
        self.numerical_errorr = QLabel("ERROR: Values must be numerical")
        self.value_errorr = QLabel("ERROR: Values must be less than 1")
        self.name_errorr = QLabel("ERROR: Name must be non-null")
        self.add_button = QPushButton("Add Player")
        self.add_button.clicked.connect(self.send_information)

        # Layout
        layout = QVBoxLayout()
        level_1 = QHBoxLayout()
        level_1.addWidget(self.name1)
        level_1.addWidget(self.name2)
        layout.addLayout(level_1)
        level_2 = QHBoxLayout()
        level_2.addWidget(self.sp1a)
        level_2.addWidget(self.sp1b)
        layout.addLayout(level_2)
        level_3 = QHBoxLayout()
        level_3.addWidget(self.sw1a)
        level_3.addWidget(self.sw1b)
        layout.addLayout(level_3)
        level_4 = QHBoxLayout()
        level_4.addWidget(self.sp2a)
        level_4.addWidget(self.sp2b)
        layout.addLayout(level_4)
        level_5 = QHBoxLayout()
        level_5.addWidget(self.sw2a)
        level_5.addWidget(self.sw2b)
        layout.addLayout(level_5)
        level_6 = QHBoxLayout()
        level_6.addWidget(self.rp1a)
        level_6.addWidget(self.rp1b)
        layout.addLayout(level_6)
        level_7 = QHBoxLayout()
        level_7.addWidget(self.rw1a)
        level_7.addWidget(self.rw1b)
        layout.addLayout(level_7)
        level_8 = QHBoxLayout()
        level_8.addWidget(self.rp2a)
        level_8.addWidget(self.rp2b)
        layout.addLayout(level_8)
        level_9 = QHBoxLayout()
        level_9.addWidget(self.rw2a)
        level_9.addWidget(self.rw2b)
        layout.addLayout(level_9)
        layout.addWidget(self.name_errorr)
        layout.addWidget(self.numerical_errorr)
        layout.addWidget(self.value_errorr)
        layout.addWidget(self.add_button)
        self.setLayout(layout)

        self.numerical_errorr.setHidden(True)
        self.value_errorr.setHidden(True)
        self.name_errorr.setHidden(True)


        self.numerical_errorr.setStyleSheet("font-size: 28px;"
            'color: red;')
        self.value_errorr.setStyleSheet("font-size: 28px;"
            'color: red;')
        self.name_errorr.setStyleSheet("font-size: 28px;"
            'color: red;')

    def send_information(self):
        # Create a dictionary to send
        numerical_error = False
        value_error = False
        name_error = False
        for x in [self.sp1b.text(),self.sw1b.text(),self.sp2b.text(),self.sw2b.text(),self.rp1b.text(),self.rw1b.text(),self.rp2b.text(),self.rw2b.text()]:
            if x.replace(".", "").isnumeric()==False:
                numerical_error = True
            elif(float(x)>1):
                value_error = True
        if self.name2.text() == '':
            name_error = True
        if numerical_error==False and value_error==False and name_error==False:
            self.numerical_errorr.setHidden(True)
            self.value_errorr.setHidden(True)
            self.name_errorr.setHidden(True)
            new_dict = {
                    "sp1": float(self.sp1b.text()),
                    "sw1": float(self.sw1b.text()),
                    "sp2": float(self.sp2b.text()),
                    "sw2": float(self.sw2b.text()),
                    "rp1": float(self.rp1b.text()),
                    "rw1": float(self.rw1b.text()),
                    "rp2": float(self.rp2b.text()),
                    "rw2": float(self.rw2b.text())
                }
            name = self.name2.text()
            # Emit the signal with the dictionary
            self.name2.clear()
            self.sp1b.clear()
            self.sw1b.clear()
            self.sp2b.clear()
            self.sw2b.clear()
            self.rp1b.clear()
            self.rw1b.clear()
            self.rp2b.clear()
            self.rw2b.clear()
            self.information_sent.emit((name,new_dict))
            self.close()
        else:
            if numerical_error:
                self.numerical_errorr.setHidden(False)
            else:
                self.numerical_errorr.setHidden(True)
            if value_error:
                self.value_errorr.setHidden(False)
            else:
                self.value_errorr.setHidden(True)
            if name_error:
                self.name_errorr.setHidden(False)
            else:
                self.name_errorr.setHidden(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Tennis_competition()
    main.show()
    exit_code = app.exec_()
    sys.exit(exit_code)

































