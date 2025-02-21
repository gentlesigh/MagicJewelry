import socket
import json
from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

# 用于连接服务器的地址和端口
SERVER_HOST = '127.0.0.1'  # 根据服务器地址修改
SERVER_PORT = 13111  # 根据服务器端口修改


# 定义 PyQt 登录界面类
class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multiplayer Login")
        self.setGeometry(100, 100, 400, 250)

        # 创建布局与控件
        layout = QVBoxLayout()

        # 用户名输入
        self.account_label = QLabel("用户名:", self)
        self.account_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(self.account_label)

        self.account_input = QLineEdit(self)
        layout.addWidget(self.account_input)

        # 密码输入
        self.password_label = QLabel("密码:", self)
        self.password_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(self.password_label)

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)  # 密码显示为*
        layout.addWidget(self.password_input)

        # 登录按钮
        self.login_button = QPushButton("登录", self)
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)

        # 注册按钮
        self.register_button = QPushButton("没有账号？点击注册", self)
        self.register_button.clicked.connect(self.open_register_window)
        layout.addWidget(self.register_button)

        # 主窗口设置
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def handle_login(self):
        """通过 socket 将用户名和密码发送到服务器"""
        account = self.account_input.text().strip()
        password = self.password_input.text().strip()

        if not account or not password:
            print("用户名和密码不能为空！")
            return

        try:
            # 创建 socket 连接到服务器
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((SERVER_HOST, SERVER_PORT))

            # 构造包含用户名和密码的 JSON 数据
            credentials = {
                "action": "login",  # 登录行为
                "account": account,
                "password": password
            }

            # 发送数据到服务器
            client_socket.send(json.dumps(credentials).encode('utf-8'))

            # 接收服务器的响应
            response = client_socket.recv(1024).decode('utf-8')
            result = json.loads(response)  # 解析服务器返回的数据

            # 根据服务器返回的结果处理登录逻辑
            if result["status"] == "success":
                print(f'登录成功，欢迎 {result["nickname"]}！')
                self.close()  # 关闭登录窗口
            else:
                print(f"登录失败: {result['message']}")

        except Exception as e:
            print(f"连接服务器时出错: {e}")
        finally:
            client_socket.close()
    def open_register_window(self):
        """打开注册窗口"""
        self.register_window = RegisterWindow()
        self.register_window.show()


# 定义 PyQt 注册界面类
class RegisterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register Account")
        self.setGeometry(100, 100, 400, 300)

        # 创建布局与控件
        layout = QVBoxLayout()

        # 用户名输入
        self.account_label = QLabel("用户名:", self)
        self.account_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(self.account_label)

        self.account_input = QLineEdit(self)
        layout.addWidget(self.account_input)

        # 密码输入
        self.password_label = QLabel("密码:", self)
        self.password_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(self.password_label)

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        # 昵称输入
        self.nickname_label = QLabel("昵称:", self)
        self.nickname_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(self.nickname_label)

        self.nickname_input = QLineEdit(self)
        layout.addWidget(self.nickname_input)

        # 注册按钮
        self.register_button = QPushButton("注册", self)
        self.register_button.clicked.connect(self.handle_register)
        layout.addWidget(self.register_button)

        # 主窗口设置
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def handle_register(self):
        """通过 socket 将注册信息发送到服务器"""
        account = self.account_input.text()
        password = self.password_input.text()
        nickname = self.nickname_input.text()

        try:
            # 创建 socket 连接到服务器
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((SERVER_HOST, SERVER_PORT))

            # 构造包含注册信息的 JSON 数据
            registration_data = {
                "action": "register",  # 注册行为
                "account": account,
                "password": password,
                "nickname": nickname
            }

            # 发送数据到服务器
            client_socket.send(json.dumps(registration_data).encode('utf-8'))

            # 接收服务器的响应
            response = client_socket.recv(1024).decode('utf-8')
            result = json.loads(response)  # 解析服务器返回的数据

            # 根据服务器返回的结果处理注册逻辑
            if result["status"] == "success":
                print(result["message"])  # 注册成功
                self.close()  # 关闭注册窗口
            else:
                print(result["message"])  # 注册失败

        except Exception as e:
            print(f"连接服务器时出错: {e}")
        finally:
            client_socket.close()