#!/usr/bin/env python3
#-*- coding:utf-8 -*-
from PyQt5.QtWidgets import (QApplication,QMainWindow,QDockWidget,QWidget,QFrame,QLabel,
						QLineEdit,QAbstractScrollArea,QTextEdit,QPushButton,QDialog,QSlider,QMessageBox,
						QInputDialog,QFileDialog,QFontDialog,QColorDialog,QToolBar,
						QMenuBar,QStatusBar,QGroupBox,QGridLayout,QHBoxLayout,QVBoxLayout,
						QFormLayout,QListWidget,QScrollBar,QDesktopWidget,QProgressBar,
						QTextBrowser)
from PyQt5.QtGui import (QFont,QIcon,QPixmap,QMovie,QColor,QTextCursor,QPalette)
from PyQt5.QtCore import (Qt,QFile,QTimer,QDateTime,QThread,pyqtSignal,pyqtSlot,
						QBasicTimer,QCoreApplication)
# from PyQt5.QtMultimedia import QAudioInput,QAudioOutput,QAudioDeviceInfo
from random import randint
from res import res
import keyboard

class ui_Login():
	"""登录窗口"""
	def setupUi(self, QMainWindow):
		self.setWindowTitle("Log In") 				# 设置窗口标题
		self.setWindowIcon(QIcon(res.path("res\\win.ico")))		# 设置窗口图标
		self.resize(580, 300) # 设置窗口大小
		"""窗体居中"""
		screen = QDesktopWidget().screenGeometry()				# 获取屏幕坐标系
		size = self.geometry()									# 获取窗口坐标系
		self.move(int((screen.width()-size.width())/2), int((screen.height()-size.height())/2) ) # 窗体居中显示	
		# 中心QWidget####################################################
		self.master = QWidget(self)
		# self.frame = QFrame(self.master)
		self.frame_grid = QGridLayout(self.master) 				# 主布局管理
		self.frame_grid.setContentsMargins(10, 0, 10, 0) 		# 布局四周留白大小(left,top,right,bottom)
		self.master.setLayout(self.frame_grid) 					# 显示QWidget布局
		self.setCentralWidget(self.master) 						# 将QWidget控件设为中心
		self.statusbar() 										# 调取状态栏
		self.createWidget()  									# 调取中心QWidget窗体控件

	def statusbar(self):  	# 状态栏
		self.statusbar = QStatusBar(self)
		self.statusbar.setObjectName("statusbar")
		self.timer = QTimer()  								# 当前时间计时器
		self.timer.start()
		self.timer.timeout.connect(self.showtime)  			# 超时设定
		self.statusbar_label_time = QLabel()
		self.setStatusBar(self.statusbar)
		self.statusbar.addPermanentWidget(self.statusbar_label_time)

	def showtime(self):
		time = QDateTime.currentDateTime()
		timeDisplay = time.toString("yyyy/MM/dd hh:mm:ss ddd")
		self.statusbar_label_time.setText(timeDisplay)
		# self.statusbar.showMessage(timeDisplay)

	def createWidget(self):
		_translate = QCoreApplication.translate
		"""控件内容"""
		conText = (("IP地址:", "entry_1",),
					("用户名:", "entry_2"),
					("密码:", "entry_3"),
					("确认密码:", "entry_4"))
		for self.index, self.r in enumerate(conText):
			for self.cindex, self.c in enumerate(self.r):
				if self.c == "IP地址:":
					self.label_1 = QLabel()
					self.label_1.setObjectName("label_1")
					self.label_1.setText(_translate("self", self.c))
					self.label_1.setFont(QFont("微软雅黑", 9, QFont.Normal))
					# self.frame_grid.addWidget(self.label_1, self.index, self.cindex, 1, 1)
				elif self.c == "entry_1":
					self.entry_ip = QLineEdit()
					self.entry_ip.setObjectName("entry_ip")
					self.entry_ip.setFont(QFont("微软雅黑", 9, QFont.Normal))
					self.entry_ip.setPlaceholderText("000.000.000.000:port") 	# 设置浮显文字
					self.entry_ip.setAlignment(Qt.AlignLeft)
					self.label_1.setBuddy(self.entry_ip) 							# 伙伴关系
					# self.frame_grid.addWidget(self.entry_ip, self.index, self.cindex, 1, 6)
				elif self.c == "用户名:":
					self.label_2 = QLabel()
					self.label_2.setObjectName("label_2")
					self.label_2.setText(_translate("self", self.c))
					self.label_2.setFont(QFont("微软雅黑", 9, QFont.Normal))
					self.frame_grid.addWidget(self.label_2, self.index, self.cindex)
				elif self.c == "entry_2":
					self.entry_user = QLineEdit()
					self.entry_user.setObjectName("entry_user")
					self.entry_user.setFont(QFont("微软雅黑", 9, QFont.Normal))
					self.entry_user.setPlaceholderText("Nickname") 	# 设置浮显文字
					self.entry_user.setAlignment(Qt.AlignLeft)
					self.label_2.setBuddy(self.entry_user) 					# 伙伴关系
					self.frame_grid.addWidget(self.entry_user, self.index, self.cindex, 1, 6)
				elif self.c == "密码:":
					self.label_3 = QLabel()
					self.label_3.setObjectName("label_3")
					self.label_3.setText(_translate("self", self.c))
					self.label_3.setFont(QFont("微软雅黑", 9, QFont.Normal))
					self.frame_grid.addWidget(self.label_3, self.index, self.cindex)
				elif self.c == "entry_3":
					self.entry_pwd = QLineEdit()
					self.entry_pwd.setObjectName("entry_pwd")
					self.entry_pwd.setFont(QFont("微软雅黑", 9, QFont.Normal))
					self.entry_pwd.setPlaceholderText("Password") 	# 设置浮显文字
					self.entry_pwd.setAlignment(Qt.AlignLeft)
					self.entry_pwd.setEchoMode(QLineEdit.Password)
					self.label_3.setBuddy(self.entry_pwd) 					# 伙伴关系
					self.frame_grid.addWidget(self.entry_pwd, self.index, self.cindex, 1, 6)
				elif self.c == "确认密码:":
					self.label_4 = QLabel()
					self.label_4.hide()
					self.label_4.setObjectName("label_3")
					self.label_4.setText(_translate("self", self.c))
					self.label_4.setFont(QFont("微软雅黑", 9, QFont.Normal))
					self.frame_grid.addWidget(self.label_4, self.index, self.cindex)
				elif self.c == "entry_4":
					self.entry_pwd_check = QLineEdit()
					self.entry_pwd_check.hide()
					self.entry_pwd_check.setObjectName("entry_pwd_check")
					self.entry_pwd_check.setFont(QFont("微软雅黑", 9, QFont.Normal))
					self.entry_pwd_check.setPlaceholderText("Password_check") 	# 设置浮显文字
					self.entry_pwd_check.setAlignment(Qt.AlignLeft)
					self.entry_pwd_check.setEchoMode(QLineEdit.Password)
					self.label_4.setBuddy(self.entry_pwd_check) 					# 伙伴关系
					self.frame_grid.addWidget(self.entry_pwd_check, self.index, self.cindex, 1, 6)
		
		# "Log in"
		self.btn_Login = QPushButton()
		self.btn_Login.setObjectName("btn_Login")
		self.btn_Login.setText(_translate("self", "Login(&L)"))
		self.btn_Login.setToolTip("登录")
		self.btn_Login.setFont(QFont("微软雅黑", 9, QFont.Normal))
		self.btn_Login.setStyleSheet("QPushButton{color:limegreen}"
									"QPushButton:hover{color:white; background-color:limegreen}"
									"QPushButton:pressed{color:white; background-color:black}")
		self.frame_grid.addWidget(self.btn_Login, 4, 2, 1, 1)
		# "Log in"
		self.btn_login = QPushButton()
		self.btn_login.hide()
		self.btn_login.setObjectName("btn_login")
		self.btn_login.setText(_translate("self", "login(&L)"))
		self.btn_login.setToolTip("进入登录界面")
		self.btn_login.setFont(QFont("微软雅黑", 9, QFont.Normal))
		self.btn_login.setStyleSheet("QPushButton{color:limegreen}"
									"QPushButton:hover{color:white; background-color:limegreen}"
									"QPushButton:pressed{color:white; background-color:black}")
		self.frame_grid.addWidget(self.btn_login, 4, 2, 1, 1)
		# "register"
		self.btn_reg = QPushButton()
		self.btn_reg.setObjectName("btn_register")
		self.btn_reg.setText(_translate("self", "register(&R)"))
		self.btn_reg.setToolTip("进入注册界面")
		self.btn_reg.setFont(QFont("微软雅黑", 9, QFont.Normal))
		self.btn_reg.setStyleSheet("QPushButton{color:limegreen}"
									"QPushButton:hover{color:white; background-color:limegreen}"
									"QPushButton:pressed{color:white; background-color:black}")
		self.frame_grid.addWidget(self.btn_reg, 4, 3, 1, 1)
		# "Register"
		self.btn_Reg = QPushButton()
		self.btn_Reg.hide()
		self.btn_Reg.setObjectName("btn_Register")
		self.btn_Reg.setText(_translate("self", "Register(&R)"))
		self.btn_Reg.setToolTip("注册")
		self.btn_Reg.setFont(QFont("微软雅黑", 9, QFont.Normal))
		self.btn_Reg.setStyleSheet("QPushButton{color:limegreen}"
									"QPushButton:hover{color:white; background-color:limegreen}"
									"QPushButton:pressed{color:white; background-color:black}")
		self.frame_grid.addWidget(self.btn_Reg, 4, 3, 1, 1)

class ui_Client():
	"""对话窗口"""
	def setupUi(self, QMainWindow):
		# self.setWindowTitle("Group Chat") 					# 设置窗口标题
		self.setWindowIcon(QIcon(res.path("res\\win.ico")))		# 设置窗口图标
		self.resize(800, 600) # 设置窗口大小
		"""窗体居中"""
		screen = QDesktopWidget().screenGeometry()				# 获取屏幕坐标系
		size = self.geometry()									# 获取窗口坐标系
		self.move(int((screen.width()-size.width())/2), int((screen.height()-size.height())/2) ) # 窗体居中显示	
		# 中心QWidget####################################################
		self.master = QWidget(self)
		self.frame = QFrame(self.master)
		self.frame_grid = QGridLayout(self.master) 				# 主布局管理
		self.frame_grid.setContentsMargins(10, 0, 10, 0) 		# 布局四周留白大小(left,top,right,bottom)
		# 添加group布局组
		self.frame_grid.addWidget(self.frame_groupbox_2(), 0, 0, 1, 8) 	# 调取group布局组添加至主布局
		self.frame_grid.addWidget(self.frame_groupbox_1(), 1, 0, 7, 8) 	# 调取group布局组添加至主布局

		self.master.setLayout(self.frame_grid) 						# 显示QWidget布局
		self.setCentralWidget(self.master) 							# 将QWidget控件设为中心
		self.menubar() 												# 调取菜单栏/工具栏
		self.statusbar() 											# 调取状态栏
		self.createWidget()  										# 调取中心QWidget窗体控件
		self.dock_Widget() 										# 调取中心Dock窗体控件

	def frame_groupbox_1(self):
		self.frame_groupbox_1 = QGroupBox(self.frame) 				# 布局组
		self.frame_groupbox_1.setObjectName("groupbox_1")
		self.frame_groupbox_1.setFont(QFont("Arial Narrow", 9, QFont.Normal))
		self.frame_groupbox_1.setTitle("Input area") 				# 设置group组标题
		self.frame_groupbox_1.setAlignment(Qt.AlignLeft)			# 设置group组标题对齐方式
		self.frame_groupbox_1.setFlat(True) 						# group组默认边框_去除(True)/显示(False)
		# self.frame_groupbox_1.setCheckable(True)					# group可选状态_可选(True)/不可选(False)
		# self.frame_groupbox_1.setChecked(False) 					# group默认状态_选中(True)/不勾选(False)
		self.groupbox_1_grid_1 = QGridLayout(self.frame_groupbox_1) # group布局组内布局方式
		self.groupbox_1_grid_1.setObjectName("grid_1")
		self.groupbox_1_grid_1.setContentsMargins(10, 10, 10, 10) 	# 布局四周留白大小(left,top,right,bottom)
		self.groupbox_1_grid_1.setSpacing(5) 						# 控件之间的间距
		self.frame_groupbox_1.setLayout(self.groupbox_1_grid_1) 	# 将子布局添加至group组
		return self.frame_groupbox_1

	def frame_groupbox_2(self):
		self.frame_groupbox_2 = QGroupBox(self.frame) 				# 布局组
		self.frame_groupbox_2.setObjectName("groupbox_2")
		self.frame_groupbox_2.setFont(QFont("Arial Narrow", 9, QFont.Normal))
		self.frame_groupbox_2.setTitle("Output area") 				# 设置group组标题
		self.frame_groupbox_2.setAlignment(Qt.AlignLeft)			# 设置group组标题对齐方式
		self.frame_groupbox_2.setFlat(True) 						# group组默认边框_去除(True)/显示(False)
		# self.frame_groupbox_2.setCheckable(True)					# group可选状态_可选(True)/不可选(False)
		# self.frame_groupbox_2.setChecked(False) 					# group默认状态_选中(True)/不勾选(False)
		self.groupbox_2_grid_1 = QGridLayout(self.frame_groupbox_2) # group布局组内布局方式
		self.groupbox_2_grid_1.setObjectName("grid_2")
		self.groupbox_2_grid_1.setContentsMargins(10, 10, 10, 10) 	# 布局四周留白大小(left,top,right,bottom)
		self.groupbox_2_grid_1.setSpacing(5) 						# 控件之间的间距
		self.frame_groupbox_2.setLayout(self.groupbox_2_grid_1) 	# 将子布局添加至group组
		return self.frame_groupbox_2

	def dock_Widget(self):
		self.Dock = QDockWidget("Online users", self)
		self.Dock.setFeatures(QDockWidget.DockWidgetMovable)
		self.Dock.setObjectName("dock")
		self.dock_grid = QListWidget()							# 布局
		self.Dock.setWidget(self.dock_grid) 					# 添加布局
		self.Dock.setFloating(False) 							# 浮动状态_窗口外(True)/窗口内(False)
		self.addDockWidget(Qt.RightDockWidgetArea, self.Dock) 	# 添加Dock控件

	"""
	菜单栏/状态栏/工具栏
	"""
	def menubar(self):
		"""菜单栏"""	
		self.menubar = self.menuBar()
		# 一级菜单
		self.file = self.menubar.addMenu("File(&F)")
		self.help = self.menubar.addMenu("Help(&H)")
		# 二级菜单
		# file_open = self.file.addAction("Open(&O)")
		# file_open.triggered.connect(self.file_open)		# 动作与槽连接
		self.file.addSeparator()
		file_quit = self.file.addAction("Exit(&E)")
		file_quit.triggered.connect(self.close) 		# 动作与槽连接

		self.file.addSeparator()
		help_about = self.help.addAction("About(&A)")
		help_about.triggered.connect(self.help_about)
		# # 工具栏
		# self.toolbar_file = self.addToolBar("文件")
		# self.toolbar_file.setMovable(False) 			# 在工具栏的位置_可移动(True)/固定(False)
		# self.toolbar_file.addAction(file_open)
		# self.toolbar_file.addSeparator()
		# self.toolbar_file.addAction(file_quit)

	def statusbar(self):  	# 状态栏
		self.statusbar = QStatusBar(self)
		self.statusbar.setObjectName("statusbar")
		self.timer = QTimer()  								# 当前时间计时器
		self.timer.start()
		self.timer.timeout.connect(self.showtime)  			# 超时设定
		self.statusbar_label_time = QLabel()
		self.statusbar_label_progressbar = QLabel()
		self.progressbar = QProgressBar(self.statusbar)  	# Progressbar
		self.progressbar.setObjectName("progressbar")
		self.progressbar.setValue(0)  						# 设置进度条的初始值
		self.progressbar.setInvertedAppearance(False) 		# True进度条从左到右(水平进度条)/从上到下(垂直进度条)
		self.basictimer = QBasicTimer()  					# 进度条计时器
		self.step = 0 
		self.progressbar.hide() 							# 设置初始状态
		self.setStatusBar(self.statusbar)
		self.statusbar.addPermanentWidget(self.statusbar_label_time)
		self.statusbar.addPermanentWidget(self.progressbar)

	def help_about(self):
		self.about = QMessageBox(self)
		self.about.setWindowTitle("About")
		self.about.setWindowIcon(QIcon(res.path("res\\win.ico")))
		self.about.setText(f"{res.author}\n\n{res.myappid}   ")
		self.about.setStandardButtons(QMessageBox.Ok)
		self.about.button(QMessageBox.Ok).setText("确定")
		self.about.exec()

	def showtime(self):
		time = QDateTime.currentDateTime()
		timeDisplay = time.toString("yyyy/MM/dd hh:mm:ss ddd")
		self.statusbar_label_time.setText(timeDisplay)
		# self.statusbar.showMessage(timeDisplay)

	def createWidget(self):
		_translate = QCoreApplication.translate
		# "text"
		self.text = QTextBrowser()
		self.text.setObjectName("text")
		self.text.verticalScrollBar().setValue(self.text.verticalScrollBar().maximum()) # 滚动条最大值关联文本
		self.text.setFont(QFont("微软雅黑", 9, QFont.Normal))
		self.groupbox_2_grid_1.addWidget(self.text, 0, 0, 1, 8)
		# "textEdit"
		self.textEdit = QTextEdit()
		self.textEdit.setObjectName("textEdit")
		self.textEdit.setFont(QFont("微软雅黑", 9, QFont.Normal))
		self.textEdit.setPlaceholderText("Please input here") 	# 设置浮显文字
		self.textEdit.setAlignment(Qt.AlignLeft)
		self.textEdit.textChanged.connect(self.text_changed)	# 将该事件绑定到text_changed方法上
		self.groupbox_1_grid_1.addWidget(self.textEdit, 0, 0, 1, 8)
		# "Confirm"
		self.btn_confirm = QPushButton()
		self.btn_confirm.setObjectName("btn_confirm")
		self.btn_confirm.setText(_translate("self", "Send(&S)"))
		self.btn_confirm.setToolTip("Press <Ctrl+Enter> to Send")
		# self.btn_confirm.setAutoRepeat()
		self.btn_confirm.setFont(QFont("微软雅黑", 9, QFont.Normal))
		self.btn_confirm.setStyleSheet("QPushButton{color:limegreen}"
									"QPushButton:hover{color:white; background-color:limegreen}"
									"QPushButton:pressed{color:white; background-color:black}")
		self.groupbox_1_grid_1.addWidget(self.btn_confirm, 1, 3, 1, 1)
		# "Quit"
		self.btn_quit = QPushButton()
		self.btn_quit.setObjectName("btn_quit")
		self.btn_quit.setText(_translate("self", "Quit(&Q)"))
		self.btn_quit.setToolTip("Quit")
		self.btn_quit.setFont(QFont("微软雅黑", 9, QFont.Normal))
		self.btn_quit.setStyleSheet("QPushButton{color:orangered}"
								"QPushButton:hover{color:white; background-color:orangered}"
								"QPushButton:pressed{color:white; background-color:black}")
		self.groupbox_1_grid_1.addWidget(self.btn_quit, 1, 4, 1, 1)

	def text_changed(self):
		# 每当文本框内容发生改变一次，该方法即执行一次，这个应该可以理解吧
		self.msg = self.textEdit.toPlainText()		 # 首先在这里拿到文本框内容
		if self.msg.endswith("\n"):
		 	#做一个判断，textedit默认按回车换行，本质是在后面加了一个\n，那我们判断换行的根据就是判断\n是否在我那本框中，如果在，OK，那下一步
			if keyboard.is_pressed("Return"):
				self.msg.rstrip("\n")
				self.Client_confirm()
			elif keyboard.is_pressed("Control") and keyboard.is_pressed("Return"):
				pass



# ui_Client()