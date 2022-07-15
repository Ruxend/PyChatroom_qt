#!/usr/bin/env python3
#-*- coding:utf-8 -*-
from PyQt5.QtWidgets import (QApplication,QMainWindow,QDockWidget,QWidget,QFrame,QLabel,
						QLineEdit,QTextEdit,QPushButton,QDialog,QSlider,QMessageBox,
						QInputDialog,QFileDialog,QFontDialog,QColorDialog,QToolBar,
						QMenuBar,QStatusBar,QGroupBox,QGridLayout,QHBoxLayout,QVBoxLayout,
						QFormLayout,QListWidget,QScrollBar,QDesktopWidget,QProgressBar,
						QShortcut)
from PyQt5.QtGui import (QFont,QIcon,QPixmap,QColor,QTextCursor,QTextDocumentFragment,QPalette,QKeySequence)
from PyQt5.QtCore import (Qt,QFile,QTimer,QDateTime,QThread,pyqtSignal,QBasicTimer,QObject)
# from PyQt5.QtMultimedia import QAudioInput,QAudioOutput,QAudioDeviceInfo
import re,os,sys,time,json,threading,socket,logging,pymysql
from datetime import datetime
from random import randint
# from eth import eth
# from xlwt_style import style
from ui_Client import ui_Login,ui_Client
# from threads_Makedirs import WorkThread_Makedirs

users = []  							# 在线用户列表
chat_obj = "------Group chat-------"  	# 聊天对象

logging.basicConfig(level = logging.INFO,
			format="""[%(process)d]<%(asctime)s>  %(threadName)s[%(thread)d] %(pathname)s[line:%(lineno)d] 
			--> %(name)s %(levelname)s(%(levelno)s): *%(message)s """,
			datefmt="%Y-%m-%d %H:%M:%S", #日期格式，与asctime搭配
			# handlers=[
			# 	 logging.StreamHandler(),
			# 	 logging.FileHandler("log_file.txt", encoding="utf-8")
			# 	 ]
			)

class myWidget_Login(QMainWindow, ui_Login):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setupUi(self)
		self.btn_Login.clicked.connect(self.Login)			# 登录
		QShortcut(QKeySequence("Return"), self, self.Login)
		self.btn_login.clicked.connect(self.goto_login)		# 进入登录界面
		self.btn_Reg.clicked.connect(self.Register)			# 注册
		self.btn_reg.clicked.connect(self.goto_register) 	# 进入注册界面
		self.get_conn_mq()

	def get_conn_mq(self):
		# 连接mysql服务
		try:
			self.mq = pymysql.connect(host="127.0.0.1",	# mysql服务器所在的主机ip
								port=3306,			# 连接的mysql主机的端口,默认是3306
								user="root",		# 用户名
								password="root",	# 密码
								db="user",			# 连接的数据库名
								# autocommit=True,	# Automatic submission
								charset="utf8")		# 当读取数据出现中文会乱码的时候,python3默认采用的utf-8字符集
			self.cursor = self.mq.cursor()
		except Exception as e:
			QMessageBox.warning(self, "Warning", "%s" %e, QMessageBox.Ok, QMessageBox.Ok)
			# logging.warning(f"Exception->get_conn_mq:{e}")

	def get_user_info(self):
		# 获取用户注册信息
		self.cursor.execute("SELECT nickname,password FROM user_info")
		result = self.cursor.fetchall()
		self.user_dic = dict(result)

	def close_conn_mq(self):
		try:
			if self.mq:
				self.mq.close()
		except Exception as e:
			QMessageBox.warning(self, "Warning", "%s" %e, QMessageBox.Ok, QMessageBox.Ok)
			# logging.warning(f"Exception->close_conn_mq:{e}")

	def Login(self):
		self.get_user_info()
		# 登录
		global IP, PORT, user
		ip = "127.0.0.1:2204"
		user = self.entry_user.text()
		pwd = self.entry_pwd.text()
		if user:
			if user in self.user_dic.keys():
				if pwd == self.user_dic[user]:
					IP, PORT = ip.split(":")
					self.serverConn(user)
					# if re.search(r"\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}\:\d{0,5}", ip):
					# 	IP, PORT = self.entry_ip.text().strip().split(":")
					# 	self.serverConn(user)
				else:
					QMessageBox.warning(self, "Warning", "密码不正确,请重新输入!", QMessageBox.Ok, QMessageBox.Ok)
			else:
				QMessageBox.warning(self, "Warning", "用户名不存在,请先注册!", QMessageBox.Ok, QMessageBox.Ok)
		else:
			QMessageBox.warning(self, "Warning", "用户名不能为空,请输入!", QMessageBox.Ok, QMessageBox.Ok)

	def Register(self):
		self.get_user_info()
		# 注册
		user = self.entry_user.text()
		pwd = self.entry_pwd.text()
		pwd_check = self.entry_pwd_check.text()
		if user:
			if user not in self.user_dic.keys():
				if pwd:
					if pwd_check == pwd:
						try:
							self.cursor.execute("INSERT INTO user.user_info(nickname,password) VALUES('%s','%s')" %(user,pwd))
							self.mq.commit()
							QMessageBox.information(self, "Info", "注册成功,请登录!", QMessageBox.Ok, QMessageBox.Ok)
							self.goto_login()
						except Exception as e:
							# print("Exception:%s"%e)
							QMessageBox.warning(self, "Info", "%s" %e, QMessageBox.Ok, QMessageBox.Ok)
						# if re.search(r"\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}\:\d{0,5}", ip):
						# 	IP, PORT = self.entry_ip.text().strip().split(":")
						# 	self.serverConn(user)
						# else:
						# 	QMessageBox.warning(self, "Warning", "IP地址格式不正确,请重新输入!", QMessageBox.Ok, QMessageBox.Ok)
					else:
						QMessageBox.warning(self, "Warning", "您输入的密码前后不一致,请重新输入!", QMessageBox.Ok, QMessageBox.Ok)
				else:
					QMessageBox.warning(self, "Warning", "请输入密码!", QMessageBox.Ok, QMessageBox.Ok)
			else:
				QMessageBox.warning(self, "Warning", "该用户名已被注册,请重新输入!", QMessageBox.Ok, QMessageBox.Ok)
		else:
			QMessageBox.warning(self, "Warning", "注册名不能为空,请输入!", QMessageBox.Ok, QMessageBox.Ok)
		
	def goto_login(self):
		self.setWindowTitle("Log In") 				# 设置窗口标题
		self.btn_Reg.hide()
		self.btn_reg.show()
		self.label_4.hide()
		self.entry_pwd_check.hide()
		self.btn_login.hide()
		self.btn_Login.show()

	def goto_register(self):
		self.setWindowTitle("Sign Up") 				# 设置窗口标题
		self.btn_Login.hide()
		self.btn_login.show()
		self.label_4.show()
		self.entry_pwd_check.show()
		self.btn_reg.hide()
		self.btn_Reg.show()

	def serverConn(self, user):
		self.close_conn_mq()
		# 建立连接
		global sock
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect((IP, int(PORT)))
			sock.send(user.encode())  # 发送用户名
			self.child = myWidget_Client()
			self.child.setWindowModality(Qt.ApplicationModal)
			self.child.show()
			self.hide()
		except Exception as e:
			QMessageBox.warning(self, "Warning", "%s" %e, QMessageBox.Ok, QMessageBox.Ok)
			# logging.info(f"Exception->serverConn:{e}")

class myWidget_Client(QMainWindow, ui_Client):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setupUi(self)
		self.setWindowTitle(f"Group Chatroom")
		self.currTime = datetime.fromtimestamp(datetime.now().timestamp())
		self.btn_confirm.clicked.connect(self.Client_confirm) 	# 连接槽
		QShortcut(QKeySequence("Return"), self, self.Client_confirm)
		self.btn_quit.clicked.connect(self.close)					# 连接槽
		QShortcut(QKeySequence("Escape"), self, self.showMinimized)
		self.text.append("<font color=orange>欢迎进入群聊，大家开始聊天吧!</font>")
		self.thread = threading.Thread(target=self.work_receive)
		self.thread.start() 	# 开始线程接收信息

	def Client_confirm(self):
		self.textEdit_value = self.textEdit.toPlainText()
		if self.textEdit_value.strip()=="": 
			self.textEdit.clear()
			self.text_refresh()
			self.statusbar.showMessage("发送内容不能为空，请重新输入。", 1000)
		else:
			# try:
			self.work_send()
			self.text_refresh()
			# except Exception as e:
			# 	self.text.append("{}\n".format(e))  # 打印输出内容
			# 	self.text_refresh()
	
	def work_send(self):
		message = user +"~"+ f"{self.currTime}" +"~"+ f"{self.msg}" +"~"+ chat_obj
		sock.send(message.encode())
		self.textEdit.clear()
		# self.text.append("------------The program is running!------------\n")
		# self.statusbar.showMessage("请稍等,正在处理...", 3600000)
		# self.thread = WorkThread_Makedirs(entry_1=self.entry_1_value, entry_2=self.entry_2_value, 
		# 						entry_3=self.entry_3_value, entry_4=self.entry_4_value, 
		# 						text=self.text)
		# 将线程th的信号finishSignal和UI主线程中的槽函数button_finish进行连接
		# self.thread.finishSignal.connect(self.work_finish)
		# self.thread.signal_1.connect(self.signal_1_call)
		# self.thread.signal_2.connect(self.signal_2_call)
		# self.thread.signal_len.connect(self.call_progressbar)
		# self.thread.signal_step.connect(self.progressbar_flush)
		# self.thread.start()  				# 启动线程
	
	def work_receive(self):
		global lst_user
		while True:
			data = sock.recv(1024)
			data = data.decode()
			try:
				lst_user = json.loads(data)
				lst_online = [self.dock_grid.item(i).text() for i in range(self.dock_grid.count())]
				for i in range(self.dock_grid.count()):
					if self.dock_grid.item(i).text() not in lst_user:
						self.dock_grid.takeItem(i)
					else:
						pass
				for ind in range(len(lst_user)):
					if lst_user[ind] not in lst_online:
						self.dock_grid.addItem(lst_user[ind])
					else:
						pass
				users.append(chat_obj)
			except:
				# print(f"接受的消息:{data}")
				data = data.split("~")
				userName = data[0]
				time = data[1]
				message = data[2]
				chatwith = data[3]
				if chatwith == chat_obj: 	# 群聊
					if userName == user:
						self.text.append(f"<font color=green>{userName}</font>"+f"\t[<font color=silver>{time}</font>] :")
						lst = message.split("\n")[1:]
						for message in lst:
							self.text.append(f"<font color=black>{message}</font>")
						self.text_refresh()
					else:
						self.text.append(f"<font color=black>{userName}</font>"+f"\t[<font color=silver>{time}</font>] :")
						lst = message.split("\n")[1:]
						for message in lst:
							self.text.append(f"<font color=black>{message}</font>")
						self.text_refresh()
				elif userName == user or chatwith == user:  # 私聊
					if userName == user:
						self.text.append(f"<font color=orange>{message}</font>")
						self.text_refresh()
					else:
						self.text.append(f"<font color=green>{message}</font>")
						self.text_refresh()
		
	def text_refresh(self):
		self.text.moveCursor(QTextCursor.End)	   # 使滚动条位置一直处于最后
		# self.text.setTextColor(QColor(randint(0,255),randint(0,255),randint(0,255),255)) # 改变text字体颜色
		self.text.update()
		
	def closeEvent(self, event):
		"""重写该方法使用sys.exit(0) 时就会只要关闭了主窗口，所有关联的子窗口也会全部关闭"""
		reply = QMessageBox.question(self, "Quit", "Do you want to quit ?", QMessageBox.Yes, QMessageBox.No)
		if reply == QMessageBox.Yes:
			self.thread.stop()
			sock.close()
			event.accept()
		else:
			event.ignore()

	def keyPressEvent(self, QKeyEvent):
		"""绑定快捷键"""
		# if QKeyEvent.modifiers() & Qt.ControlModifier:
		if QKeyEvent.key() == Qt.Key_Return:
			try:
				doc = QTextDocumentFragment()
				self.textEdit.textCursor().insertFragment(doc.fromPlainText("\n"))
			except Exception as e:
				print(e)
	
if __name__ == "__main__":
	app = QApplication(sys.argv)
	# login = myWidget_Client()
	login = myWidget_Login()
	login.show()
	sys.exit(app.exec())
	