from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
from dbutil import get_conn,close_conn
from 加密函数 import md5
from 正则表达式 import email_re,tel_re
import  datetime


################################################################
ui, _ = loadUiType('main.ui')
class Mainapp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self) # 构造界面
        self.handle_uichange()
        self.handle_button()

################################################################
    #建立ui变化处理
    def handle_uichange(self):
        self.theme_hide()
        self.tabWidget.tabBar().setVisible(False)
        self.show_type()
        self.show_author()
        self.show_publisher()
        self.show_combox_type()
        self.show_comboBox_author()
        self.show_comboBox_publisher()
        self.show_client()


    #建立槽与通信
    def handle_button(self):
        self.theme_Button.clicked.connect(self.theme_show)
        self.pushButton_change_theme.clicked.connect(self.theme_hide)
        self.book_Button.clicked.connect(self.bookopen)
        self.base_Button.clicked.connect(self.setting)
        self.pushButton_type_add.clicked.connect(self.add_type)
        self.pushButton_author_add.clicked.connect(self.add_author)
        self.pushButton_publisher_add.clicked.connect(self.add_publisher)
        self.add_book_button.clicked.connect(self.book_inf_get)
        self.add_book_reserch_button.clicked.connect(self.book_inf_search)
        self.edit_book_reserch_button.clicked.connect(self.book_edit_search)
        self.edit_book_button.clicked.connect(self.book_inf_change)
        self.user_Button.clicked.connect(self.user_admin)
        self.day_Button.clicked.connect(self.day_record)
        self.pushButton_user_add.clicked.connect(self.user_add)
        self.pushButton_user_change.setEnabled(False)
        self.pushButton_user_login.clicked.connect(self.user_login)
        self.pushButton_user_change.clicked.connect(self.user_change)
        self.client_Button.clicked.connect(self.client_admin)
        self.pushButton_add_client.clicked.connect(self.add_client)
        self.pushButton_search.clicked.connect(self.search_client)
        self.pushButton_client_change.clicked.connect(self.change_client)
        self.pushButton_client_del.clicked.connect(self.del_client)
        self.lineEdit_edit_tel.editingFinished.connect(self.tel_warning_change)
        self.lineEdit_client_tel.editingFinished.connect(self.tel_warning_add)
        self.day_Button.clicked.connect(self.day_admin)
        self.pushButton_borrow_book.clicked.connect(self.book_borrow)
        self.pushButton_return_book.clicked.connect(self.book_return)
        self.pushButton_show_borrow_book.clicked.connect(self.book_borrow_show)

    def tel_warning_change(self):
        tel = self.lineEdit_edit_tel.text()
        if tel:
            if not email_re(tel):
                self.label_edit_tel.setText("请输入正确的电话号码")

    def tel_warning_add(self):
        tel = self.lineEdit_client_tel.text()
        if tel:
            if not email_re(tel):
                self.label_client_add_tel.setText("请输入正确的电话号码")

        #类别下拉框信息显示


    def show_combox_type(self):
        conn,cursor = get_conn()
        sql = "select type from book_type"
        cursor.execute(sql)
        data = cursor.fetchall()
        self.comboBox_2.addItems([item[0] for item in data])
        self.comboBox_edit_type.addItems([item[0] for item in data])

    #作者下拉框信息显示
    def show_comboBox_author(self):
        conn,cursor = get_conn()
        sql = "SELECT name from author"
        cursor.execute(sql)
        data = cursor.fetchall()
        self.comboBox.addItems([item[0] for item in data])
        self.comboBox_edit_author.addItems([item[0] for item in data])

    # 出版社下拉框信息显示
    def show_comboBox_publisher(self):
        conn, cursor = get_conn()
        sql = "SELECT publisher from publisher"
        cursor.execute(sql)
        data = cursor.fetchall()
        self.comboBox_3.addItems([item[0] for item in data])
        self.comboBox_edit_publisher.addItems([item[0] for item in data])

    #书籍信息录入
    def book_inf_get(self):
        conn,cursor = get_conn()
        sql = "insert into book_inf(name,number,type,author,publisher,price,introduce) values(%s,%s,%s,%s,%s,%s,%s)"
        name = self.book_name.text()
        number = self.book_number.text()
        price = float(self.book_price.text())
        type = self.comboBox_2.currentText()
        author = self.comboBox.currentText()
        publisher = self.comboBox_3.currentText()
        introduce = self.book_introduce.toPlainText()
        # print(name,number,price)
        try:
            cursor.execute(sql,(name,number,type,author,publisher,price,introduce))
            conn.commit()
            close_conn(conn,cursor)
            self.statusBar().showMessage("书籍信息录入成功")
        except Exception:
            self.statusBar().showMessage("书籍信息录入失败")

    #书籍信息检索
    def book_inf_search(self):
        conn,cursor = get_conn()
        name = self.book_name.text()
        sql = "select name from book_inf where name=(%s)"
        cursor.execute(sql,(name,))
        data = cursor.fetchall()
        if data:
            QMessageBox.information(self, "查询结果", "书籍已经存在！",QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        else:
            QMessageBox.information(self, "查询结果", "书籍不存在，请添加",QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        close_conn(conn,cursor)

    #书籍信息编辑
    def book_edit_search(self):
        conn, cursor = get_conn()
        name = self.book_name_edit.text()
        sql = "select * from book_inf where name=(%s)"
        cursor.execute(sql, (name,))
        data = cursor.fetchone()
        self.book_number_edit.setText(str(data[7]))
        self.book_price_edit.setText(str(data[5]))
        self.book_introduce_edit.setPlainText(data[6])
        self.comboBox_edit_author.setCurrentText(data[2])
        self.comboBox_edit_type.setCurrentText(data[3])
        self.comboBox_edit_publisher.setCurrentText(data[4])

    #书籍信息修改
    def book_inf_change(self):

        conn, cursor = get_conn()
        name = self.book_name_edit.text()
        sql = "select * from book_inf where name=(%s)"
        cursor.execute(sql, (name,))
        data = cursor.fetchone()
        if data:
            author = self.comboBox_edit_author.currentText()
            type = self.comboBox_edit_type.currentText()
            publisher = self.comboBox_edit_publisher.currentText()
            price = float(self.book_price_edit.text())
            introduce = self.book_introduce_edit.toPlainText()
            number = self.book_number_edit.text()
            sql = "update book_inf set number = %s,author=%s,type=%s,publisher=%s,price=%s,introduce=%s where name=%s"
            cursor.execute(sql, (number, author, type, publisher, price,introduce,name))
            conn.commit()
            close_conn(conn,cursor)
            self.statusBar().showMessage("书籍信息修改成功")
        else:
            QMessageBox.warning(self,"警告","请不要修改查询书籍")
            close_conn(conn,cursor)

    #用户信息录入
    def user_add(self):
        username = self.lineEdit_username.text()
        email = self.lineEdit_email.text()
        password = self.lineEdit_password.text()
        password_ture = self.lineEdit_password_ture.text()
        if password == password_ture:
            password = md5(password)
            conn,cursor = get_conn()
            sql = "INSERT INTO user(username, email, password) VALUES (%s, %s,%s)"
            cursor.execute(sql,(username, email, password))
            conn.commit()
            close_conn(conn,cursor)
            self.statusBar().showMessage("用户添加成功！")
        else:
            QMessageBox.warning(self,"警告","两次密码输入不一致")

    #用户登录
    def user_login(self):
        username = self.lineEdit_username_login.text()
        password = self.lineEdit_password_login.text()

        conn,cursor = get_conn()
        sql = "SELECT username, password,email FROM user WHERE username=%s"
        cursor.execute(sql,(username,))
        data = cursor.fetchone()
        # print(data)
        if data:
            if md5(password) == data[1]:
                self.pushButton_user_change.setEnabled(True)
                self.lineEdit_username_change.setText(data[0])
                self.lineEdit_email_change.setText(data[2])
                close_conn(conn,cursor)
            else:
                QMessageBox.information(self, "登录", "密码错误")
                close_conn(conn, cursor)
        else:
            QMessageBox.information(self, "登录", "用户不存在")
            close_conn(conn, cursor)

    #用户信息修改
    def user_change(self):
        username = self.lineEdit_username_change.text()
        password = self.lineEdit_password_change.text()
        email = self.lineEdit_email_change.text()
        password_ture = self.lineEdit_password_change_ture.text()

        conn,cursor = get_conn()
        sql = "SELECT * FROM user WHERE username=%s"
        cursor.execute(sql,(username,))
        data = cursor.fetchone()
        # print(data)
        if data:
            sql = "update user SET username=%s,email=%s,password=%s WHERE username=%s"
            if password == password_ture:
                password = md5(password)
                cursor.execute(sql,(username,email,password,username))
                conn.commit()
                close_conn(conn,cursor)
            else:
                QMessageBox.warning(self, "警告", "两次密码输入不一致")
                close_conn(conn,cursor)
        else:
            QMessageBox.warning(self,"警告","数据库无法检索到该用户信息，无法修改")
            close_conn(conn,cursor)
        self.pushButton_user_change.setEnabled(False)

################################################################
    #导航栏设置
    #主题的显示和隐藏
    def theme_show(self):
        self.groupBox.show()

    def theme_hide(self):
        self.groupBox.hide()

    def bookopen(self):
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)

    def setting(self):
        self.tabWidget.setCurrentIndex(1)
        self.tabWidget_3.setCurrentIndex(0)

    def user_admin(self):
        self.tabWidget.setCurrentIndex(2)

    def day_record(self):
        self.tabWidget.setCurrentIndex(3)

    def client_admin(self):
        self.tabWidget.setCurrentIndex(3)
        self.tabWidget_4.setCurrentIndex(0)

    def day_admin(self):
        self.tabWidget.setCurrentIndex(4)
########################################################################
    #数据库处理
    #添加类别
    def add_type(self):
        #数据库操作流程
        #1.获取连接   2.获取cursor
        conn,cursor = get_conn()
        #3.sql语句
        sql = "insert into book_type(type) values(%s)"
        type_name = self.lineEd_type.text()
        #4.执行语句
        cursor.execute(sql,(type_name,))
        #5.insert,update,delete要进行提交操作
        conn.commit()
        #6.关闭数据库
        close_conn(conn,cursor)
        #消息提示
        self.statusBar().showMessage("类别信息添加成功")
        self.show_type()
        self.show_combox_type()

    #添加作者
    def add_author(self):
        # 1.获取连接   2.获取cursor
        conn, cursor = get_conn()
        # 3.sql语句
        sql = "insert into author(name,telephone,gender,home) values(%s,%s,%s,%s)"
        name = self.lineEd_author_name.text()
        telephone = self.lineEd_author_tel.text()
        gender = self.lineEd_author_sex.text()
        home = self.lineEd_author_home.text()
        # 4.执行语句
        cursor.execute(sql, (name,telephone,gender,home))
        # 5.insert,update,delete要进行提交操作
        conn.commit()
        # 6.关闭数据库
        close_conn(conn, cursor)
        # 消息提示
        self.statusBar().showMessage("作者信息添加成功")
        self.show_author()
        self.show_comboBox_author()

    #添加出版社
    def add_publisher(self):
        # 1.获取连接   2.获取cursor
        conn, cursor = get_conn()
        # 3.sql语句
        sql = "insert into publisher(publisher) values(%s)"
        publisher = self.lineEd_publisher.text()
        # 4.执行语句
        cursor.execute(sql, (publisher,))
        # 5.insert,update,delete要进行提交操作
        conn.commit()
        # 6.关闭数据库
        close_conn(conn, cursor)
        self.statusBar().showMessage("出版社信息添加成功")
        self.show_publisher()
        self.show_comboBox_publisher()

    #类别显示
    def show_type(self):
        # 1.获取连接   2.获取cursor
        conn, cursor = get_conn()
        # 3.sql语句
        sql = "select type from book_type"
        cursor.execute(sql)

        data = cursor.fetchall()
        if data:
            #设置行列，设置表头
            self.tableWidget_type.setRowCount(len(data))
            self.tableWidget_type.setColumnCount(len(data[0]))
            self.tableWidget_type.setHorizontalHeaderLabels(["类别"])
            # 表格加载内容
            for row,form in enumerate(data):
                for column,item in enumerate(form):
                    self.tableWidget_type.setItem(row,column,QTableWidgetItem(str(item)))
        close_conn(conn,cursor)

    #作者显示
    def show_author(self):
        # 1.获取连接   2.获取cursor
        conn, cursor = get_conn()
        # 3.sql语句
        sql = "select name,telephone,gender,home from author"
        cursor.execute(sql)

        data = cursor.fetchall()
        if data:
            # 设置行列，设置表头
            self.tableWidget_author.setRowCount(len(data))
            self.tableWidget_author.setColumnCount(len(data[0]))
            self.tableWidget_author.setHorizontalHeaderLabels(["姓名","电话","性别","家庭住址"])
            # 表格加载内容
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_author.setItem(row, column, QTableWidgetItem(str(item)))
        close_conn(conn, cursor)

    #出版社显示
    def show_publisher(self):
        # 1.获取连接   2.获取cursor
        conn, cursor = get_conn()
        # 3.sql语句
        sql = "select publisher from publisher"
        cursor.execute(sql)

        data = cursor.fetchall()
        if data:
            # 设置行列，设置表头
            self.tableWidget_publisher.setRowCount(len(data))
            self.tableWidget_publisher.setColumnCount(len(data[0]))
            self.tableWidget_publisher.setHorizontalHeaderLabels(["姓名", "电话", "性别", "家庭住址"])
            # 表格加载内容
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_publisher.setItem(row, column, QTableWidgetItem(str(item)))
        close_conn(conn, cursor)

    #添加顾客信息
    def add_client(self):

        name = self.lineEdit_client_name.text()
        telephone = self.lineEdit_client_tel.text()
        number = self.lineEdit_client_number.text()
        conn,cursor = get_conn()
        sql = "INSERT INTO client(name,telephone,number) VALUES(%s,%s,%s)"
        cursor.execute(sql,(name,telephone,number))
        conn.commit()
        close_conn(conn,cursor)
        self.statusBar().showMessage("顾客信息添加成功")
        self.show_client()
        self.tabWidget_4.setCurrentIndex(0)

    #展示顾客信息
    def show_client(self):

        conn,cursor = get_conn()
        sql = "select  name,telephone,number from  client "
        cursor.execute(sql)
        data = cursor.fetchall()

        # 设置行列，设置表头
        self.tableWidget_client.setRowCount(len(data))
        self.tableWidget_client.setColumnCount(len(data[0]))
        self.tableWidget_client.setHorizontalHeaderLabels(["姓名", "电话", "用户ID"])
        # 表格加载内容
        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.tableWidget_client.setItem(row, column, QTableWidgetItem(str(item)))
        close_conn(conn, cursor)

    #查询顾客信息
    def search_client(self):

        search_number = self.lineEdit_client_search.text()
        edit_name = self.lineEdit_edit_name.text()
        edit_number = self.lineEdit_edit_number.text()
        edit_telephone = self.lineEdit_edit_tel.text()

        conn,cursor = get_conn()
        sql  = "SELECT * FROM client WHERE number = %s"
        cursor.execute(sql,(search_number,))
        data = cursor.fetchone()
        if data:
            self.lineEdit_edit_name.setText(data[1])
            self.lineEdit_edit_tel.setText(data[2])
            self.lineEdit_edit_number.setText(data[3])
            close_conn(conn,cursor)
        else:
            QMessageBox.information(self,"提示","无法检索到此人" )

    #修改顾客信息
    def change_client(self):
        edit_name = self.lineEdit_edit_name.text()
        edit_number = self.lineEdit_edit_number.text()
        edit_telephone = self.lineEdit_edit_tel.text()

        conn,cursor = get_conn()
        sql = "SELECT * FROM client WHERE number = %s"
        cursor.execute(sql,(edit_number,))
        data = cursor.fetchone()
        if data:
            sql = "update client set number = %s, telephone = %s,name = %s where number = %s"
            cursor.execute(sql,(edit_number,edit_telephone,edit_name,edit_number))
            conn.commit()
            close_conn(conn,cursor)
            self.statusBar().showMessage("顾客更新添加成功")
            self.show_client()
            self.tabWidget_4.setCurrentIndex(0)
        else:
            QMessageBox.information(self,"警示","数据库无此成员信息，请先进行添加")
            close_conn(conn,cursor)

    #删除顾客信息
    def del_client(self):
        edit_name = self.lineEdit_edit_name.text()
        edit_number = self.lineEdit_edit_number.text()
        edit_telephone = self.lineEdit_edit_tel.text()

        conn, cursor = get_conn()
        sql = "SELECT * FROM client WHERE number = %s"
        cursor.execute(sql, (edit_number,))
        data = cursor.fetchone()
        if data:
            sql = "DELETE FROM client WHERE number = %s"
            cursor.execute(sql, (edit_number,))
            conn.commit()
            close_conn(conn, cursor)
            self.statusBar().showMessage("顾客删除添加成功")
            self.show_client()
            self.tabWidget_4.setCurrentIndex(0)
        else:
            QMessageBox.information(self, "警示", "数据库无此成员信息，请先进行添加")
            close_conn(conn, cursor)

    #借书操作
    def book_borrow(self):

        bookname = self.lineEdit_bookname.text()
        clientname = self.lineEdit_clientname.text()
        days = int(self.comboBox_borrow_time.currentText())
        from_day = datetime.datetime.now()
        to_day = from_day + datetime.timedelta(days=days)

        # print(bookname,clientname,days,from_day,to_day)
        conn,cursor = get_conn()
        sql = "insert into book_borrow(book_name,client_name,day,from_day,to_day) values (%s,%s,%s,%s,%s)"
        cursor.execute(sql,(bookname,clientname,days,from_day,to_day))
        conn.commit()
        close_conn(conn,cursor)
        self.statusBar().showMessage("借书信息添加成功！")

    #还书操作
    def book_return(self):
        book_name = self.lineEdit_bookname.text()
        client_name = self.lineEdit_clientname.text()

        conn,cursor = get_conn()
        sql = "SELECT * FROM book_borrow WHERE book_name= %s and client_name=%s"
        cursor.execute(sql,(book_name,client_name))
        data = cursor.fetchall()
        if data:
            # sql = "delete  from book_borrow WHERE client_name = %s and book_name = %s"
            sql = "DELETE FROM book_borrow WHERE book_name=%s and client_name = %s"
            cursor.execute(sql,(book_name,client_name))
            conn.commit()
            close_conn(conn,cursor)
            self.statusBar().showMessage("用户已经归还书籍")
        else:
            QMessageBox.information(self,"提示","用户未借阅该书，无法归还")
            close_conn(conn,cursor)

    #借阅展示
    def book_borrow_show(self):

        conn,cursor = get_conn()
        sql = "select book_name,client_name,day,from_day,to_day from book_borrow "
        cursor.execute(sql)
        data = cursor.fetchall()
        close_conn(conn,cursor)

        # 设置行列，设置表头
        self.tableWidget_book_borrow.setRowCount(len(data))
        self.tableWidget_book_borrow.setColumnCount(len(data[0]))
        self.tableWidget_book_borrow.setHorizontalHeaderLabels(["书籍", "顾客", "借阅时间", "借出日期","归还日期"])
        # 表格加载内容
        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.tableWidget_book_borrow.setItem(row, column, QTableWidgetItem(str(item)))



def main():
    app = QApplication([])

    window = Mainapp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()