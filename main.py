import os
import sys

import requests
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow,QApplication, QWidget, QLabel, QGridLayout
from PyQt6.QtCore import Qt

SCREEN_SIZE = [600, 600]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.lon = "37.530887"
        self.lat = "55.703118"
        self.zoom = 5
        self.delta = "0.002,0.002"
        self.initUI()
        self.getImage()


    def getImage(self):
        server_address = 'https://static-maps.yandex.ru/v1?'
        api_key = 'f5e8d0d9-e8bf-40fb-8f03-b0f301319c2a'
        map_params = {
            # позиционируем карту центром на наш исходный адрес
            "ll": ",".join([self.lon,self.lat]),
            "apikey": api_key,
            "z": self.zoom
        }

        response = requests.get(server_address, params=map_params)

        if not response:
            self.status.setText("Ошибка выполнения запроса! Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        else:
            self.status.setText("Запрос успешен")

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        ## Изображение
        self.status = QLabel(self)
        self.status.move(10,570)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_PageUp and self.zoom < 21:
            self.zoom += 1
            self.getImage()
        if event.key() == Qt.Key.Key_PageDown and self.zoom > 0:
            self.zoom -= 1
            self.getImage()


    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())