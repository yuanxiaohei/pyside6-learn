import sys
from PySide6.QtWidgets import QApplication,QTextEdit,QWidget,QVBoxLayout,QPushButton\
,QHBoxLayout,QFileDialog,QRadioButton,QLineEdit
# from PySide6.QtGui import QFont
from os import getcwd,listdir,curdir
from os.path import basename
from random import choice,shuffle
from collections import defaultdict
import pymysql

class Children_window_dian_ming(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(600,450,500,300)
        self.setWindowTitle('点名系统')
        self.button_wen_jian=QPushButton('文件')
        self.button_xuan_ren=QPushButton('选人')
        self.button_tian_jia=QPushButton('添加')
        self.button_jian_shao=QPushButton('减少')
        self.children_window_dian_ming_main_layout=QHBoxLayout()
        self.children_window_dian_ming_text=QTextEdit()

        self.children_window_search=QHBoxLayout()
        self.children_window_search_text=QLineEdit()
        self.children_window_search_text.setPlaceholderText("输入查找学生的学号")
        
        self.button_search=QPushButton("查找")
        self.children_window_search.addWidget(self.children_window_search_text)
        self.children_window_search.addWidget(self.button_search)

        self.layout_left_main=QVBoxLayout()
        self.layout_left_main.addWidget(self.children_window_dian_ming_text)
        self.layout_left_main.addLayout(self.children_window_search)

        self.button_dian_ming_radiobutton_chongfu=QRadioButton('重复')
        self.button_dian_ming_radiobutton_no_chongfu=QRadioButton('不重复')
        self.button_dian_ming_radiobutton_no_chongfu.setChecked(True)
        
        
        self.children_window_dian_ming_button_layout=QVBoxLayout()
        self.children_window_dian_ming_button_layout.addWidget(self.button_wen_jian)
        self.children_window_dian_ming_button_layout.addWidget(self.button_xuan_ren)
        self.children_window_dian_ming_button_layout.addWidget(self.button_tian_jia)
        self.children_window_dian_ming_button_layout.addWidget(self.button_jian_shao)
        self.children_window_dian_ming_button_layout.addWidget(self.button_dian_ming_radiobutton_chongfu)
        self.children_window_dian_ming_button_layout.addWidget(self.button_dian_ming_radiobutton_no_chongfu)
        
        self.children_window_dian_ming_main_layout.addLayout(self.layout_left_main)
        self.children_window_dian_ming_main_layout.addLayout(self.children_window_dian_ming_button_layout)
        self.setLayout(self.children_window_dian_ming_main_layout)
        self.children_font_style()
        self.children_window_chufa_shijian()
        
        
    def children_font_style(self):
        style="""
            color: black;
            font-weight: bold;font-size: 16px;
            font-family:宋体;
            
        """
        self.button_wen_jian.setStyleSheet(style)
        self.button_xuan_ren.setStyleSheet(style)
        self.children_window_dian_ming_text.setStyleSheet(style)
        self.button_tian_jia.setStyleSheet(style)
        self.button_jian_shao.setStyleSheet(style)
        self.button_search.setStyleSheet(style)

        
    def children_window_chufa_shijian(self):
        self.button_wen_jian.clicked.connect(self.button_wen_jian_function)
        self.button_xuan_ren.clicked.connect(self.button_xuan_ren_function)
        self.button_tian_jia.clicked.connect(self.button_tian_jia_function)
        self.button_jian_shao.clicked.connect(self.button_jian_shao_function)
        self.button_search.clicked.connect(self.search_stu)
            
    def button_wen_jian_function(self):
        self.dian_ming_file_path,_=QFileDialog.getOpenFileName(self,'名单数据',getcwd(),filter='*.txt')
        print(self.dian_ming_file_path)
        with open(self.dian_ming_file_path,mode='r',encoding='utf-8') as f:
            self.std_name_list=f.readlines()
        self.children_window_dian_ming_text.setText('数据加载完毕')
        shuffle(self.std_name_list)
        print(len(self.std_name_list))
        self.no_repeat_len=len(self.std_name_list)
        self.i=0
        self.table_name=basename(self.dian_ming_file_path).split('.')[0].strip()
        print(self.table_name)
    def button_xuan_ren_function(self):
        if self.button_dian_ming_radiobutton_chongfu.isChecked():
            student_info=choice(self.std_name_list)
            self.children_window_dian_ming_text.clear()
            self.children_window_dian_ming_text.setText(student_info)
        else:
            if self.i<self.no_repeat_len:
                self.children_window_dian_ming_text.clear()
                self.children_window_dian_ming_text.setText(self.std_name_list[self.i])
                self.i+=1   
            else:
                self.children_window_dian_ming_text.setText(f'点名完毕,一共{self.i}名学生')
    def button_tian_jia_function(self):
        name=self.children_window_dian_ming_text.toPlainText()
        # name=name.strip()
        try:
            name=name.strip().split('已经')[0]
        except:
            name=name.strip()
        conn=pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='yuanyongchao3')
        cursor=conn.cursor()  
        cursor.execute("create database if not exists data_stu default charset utf8 collate utf8_general_ci")
        cursor.execute("use data_stu")
        cursor.execute(f"create table if not exists {self.table_name}(name text,num tinyint)")
        cursor.execute(f"select * from {self.table_name}")
        data1=cursor.fetchall()#查看数据库数据
        data_name=[i[0].strip() for i in data1]
        if len(data1)==0:
            cursor.execute(f"insert into {self.table_name} values(%s,%s)",(name,1))
            conn.commit()
            cursor.execute(f"select * from {self.table_name} where name=%s",(name))
            name1=cursor.fetchall()
            self.children_window_dian_ming_text.clear()
            self.children_window_dian_ming_text.setText(f'{name1[0][0]}已经旷课{name1[0][1]}次了')
        else:
            if name not in data_name:
                cursor.execute(f"insert into {self.table_name} values(%s,%s)",(name,1))
                conn.commit()
                cursor.execute(f"select * from {self.table_name} where name=%s",(name))
                name2=cursor.fetchall()
                self.children_window_dian_ming_text.clear()
                self.children_window_dian_ming_text.setText(f'{name2[0][0]}已经旷课{name2[0][1]}次了')
            else:
                cursor.execute(f"select * from {self.table_name} where name=%s",(name))
                cishu1=cursor.fetchall()
                cishu1=cishu1[0][1]+1
                cursor.execute(f"update {self.table_name} set num=%s where name=%s",(cishu1,name))
                conn.commit()
                self.children_window_dian_ming_text.clear()
                self.children_window_dian_ming_text.setText(f"{name}已经旷课{cishu1}次了")

        cursor.close()
        conn.close()
       


            
    def button_jian_shao_function(self):
        conn=pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='yuanyongchao3')
        cursor=conn.cursor()
        cursor.execute('use data_stu')
        # cursor.execute("select * from test_table")
        # data=cursor.fetchall()
        # print(data)
        # data=self.children_window_dian_ming_text.toPlainText()
        print(self.data)
        cursor.execute(f"update {self.table_name} set num=%s where name=%s",(int(self.data[0][1])-1,self.data[0][0]))
        conn.commit()

        cursor.execute(f"select * from {self.table_name} where name=%s",(self.data[0][0]))
        name2=cursor.fetchall()
        self.children_window_dian_ming_text.clear()
        self.children_window_dian_ming_text.setText(f"{name2[0][0]}已经旷课{name2[0][1]}次了")
        cursor.close()
        conn.close()

    def search_stu(self):
        name_data=self.children_window_search_text.text()
        print(name_data)

        conn=pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='yuanyongchao3')
        cursor=conn.cursor()
        cursor.execute('use data_stu')
        # if  cursor.execute(f'select * from test_table where name like "{name_data}%"'):
        #     print('sucess')
        # else:
        #     print("error")
        if cursor.execute(f"select * from {self.table_name} where name like %s",(f'{name_data}%')):
            self.data=cursor.fetchall()
            self.children_window_dian_ming_text.clear()
            self.children_window_dian_ming_text.setText(f'{self.data[0][0]}已经旷课{self.data[0][1]}次了')
        else:
            self.children_window_dian_ming_text.clear()
            self.children_window_dian_ming_text.setText(f'该同学未旷课')
        cursor.close()
        conn.close()


    