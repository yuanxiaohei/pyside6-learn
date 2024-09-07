import sys
from PySide6.QtWidgets import QApplication,QTextEdit,QMainWindow,QWidget,QVBoxLayout,QPushButton\
,QHBoxLayout,QFileDialog,QRadioButton
# from PySide6.QtGui import QFont
from os import getcwd
from random import choice,shuffle
sys.path.append(getcwd())
# print(sys.path)
from module_windows.Children_dianming_window import Children_window_dian_ming

class MenuExample(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(600,450,500,250)
        self.setWindowTitle('随便写写')
        self.w1=QWidget()
        self.layout1=QVBoxLayout()
        self.w1.setLayout(self.layout1)
        self.button1=QPushButton('点名')
        self.button2=QPushButton('题库')
        self.layout1.addWidget(self.button1)
        self.layout1.addWidget(self.button2)
        self.setCentralWidget(self.w1)
        self.function_chufa_tiaojian()
        self.main_font_style()
    def function_chufa_tiaojian(self):
        self.button1.clicked.connect(self.dian_ming)
        self.button2.clicked.connect(self.ti_ku)
    def dian_ming(self):
        self.children_window_dian_ming_main_window=Children_window_dian_ming()
        # self.children_window_dian_ming_main_window.setStyle("Fusion")
        self.children_window_dian_ming_main_window.show()
    def ti_ku(self):
        pass
    def main_font_style(self):
        style="""
            color: black;
            font-weight: bold;
            font-size: 16px;
            font-family:宋体; 
        """
        self.button1.setStyleSheet(style)
        self.button2.setStyleSheet(style)



        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")#设置整个app风格
    example = MenuExample()
    example.show()
    sys.exit(app.exec())
