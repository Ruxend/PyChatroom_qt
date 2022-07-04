#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import socket,threading,queue,os,sys
import json  # json.dumps(some)打包   json.loads(some)解包
import os.path

IP = "127.0.0.1"
PORT = 2204	 # 端口
messages = queue.Queue()
lst_users = []   # 用户连接队列 0:userName 1:connection
lock = threading.Lock()

def onlines():	# 统计当前在线人员
	online = []
	for i in range(len(lst_users)):
		online.append(lst_users[i][0])
	return online

class ChatServer(threading.Thread):
	global lst_users, lock
	def __init__(self):		 # 构造函数
		super().__init__()
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		os.chdir(sys.path[0])
		# 防止socket server重启后端口被占用（socket.error: [Errno 98] Address already in use）
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	
	# 接受来自客户端的用户名，如果用户名为空，使用用户的IP与端口作为用户名。如果用户名出现重复，则在出现的用户名依此加上后缀“2”、“3”、“4”……
	def receive(self, conn, addr):	# 接收消息
		user = conn.recv(1024)		# 用户名称
		user = user.decode()
		# print(f"接收的addr:{addr}")
		# print(f"接收的用户名:{user}")
		lst_users.append((user, conn))
		# print(f"接受的用户列表:{lst_users}")
		online_users = onlines()		# 更新在线用户列表
		# print(f"在线用户列表:{online_users}")
		self.Load(online_users, addr)
		# 在获取用户名后便会不断地接受用户端发来的消息(即聊天内容)，结束后关闭连接。
		try:
			while True:
				data = conn.recv(1024)			# 接收发送来消息
				data = data.decode()
				data = data.split("~")
				userName = data[0]
				time = data[1]
				message = data[2]
				chatWith = data[3]
				# print(f"接收发送来消息:{data}")
				send_data = user +"~"+ time +"~\n    "+ message.rstrip("\n").replace("\n", "\n    ") +"~"+ chatWith
				# print(f"加入队列的消息:{send_data}")
				self.Load(send_data, addr)
			conn.close()
		# 如果用户断开连接，将该用户从用户列表中删除，然后更新用户列表。
		except:   
			j = 0			# 用户断开连接
			for man in lst_users:
				if man[0] == user:
					lst_users.pop(j)		# 服务器段删除退出的用户
					break
				j = j+1
			online_users = onlines()		# 更新在线用户列表
			self.Load(online_users, addr)
			conn.close()

	# 将地址与数据(需发送给客户端)存入messages队列。
	def Load(self, data, addr):
		lock.acquire()
		try:
			messages.put((addr, data))
		# except Exception as e:
		# 	print("Load Exception:", e)
		finally:
			lock.release()

	# 服务端在接受到数据后，会对其进行一些处理然后发送给客户端，如下图，对于聊天内容，服务端直接发送给客户端，而对于用户列表，便由json.dumps处理后发送。
	def sendData(self): # 发送数据
		while  True:
			if not messages.empty():
				message = messages.get()
				# print(f"取得消息队列:{message}")
				if isinstance(message[1], str):            # 传送消息
					for i in range(len(lst_users)):
						data = message[1]
						# print(f"取得队列消息:{data}")
						lst_users[i][1].send(data.encode())
						print(f"发送的消息:{data}")

				if isinstance(message[1], list):           # 传送用户列表
					data = json.dumps(message[1])
					for i in range(len(lst_users)):
						try:
							lst_users[i][1].send(data.encode())
						except:
							pass

	def run(self):
		self.sock.bind((IP, PORT))
		self.sock.listen(108)       # 监听数量
		q = threading.Thread(target=self.sendData)
		q.start()
		while True:
			conn, addr = self.sock.accept()
			t = threading.Thread(target=self.receive, args=(conn, addr))
			t.start()
		self.sock.close()

if __name__ == "__main__":
	cserver = ChatServer()
	cserver.start()
