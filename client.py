import rsa
import pickle
import socket
import core


class Client:
    def __init__(self):
        self.work_book = core.Book()
        self.socket = socket.socket()
        self.host = core.get_host()

    def recv(self):
        size_byte = self.socket.recv(4)
        # print(size_byte)
        size = pickle.unpack('i', size_byte)[0]
        if size == 256:
            crypt_byte_msg = self.socket.recv(256)
            msg = rsa.decrypt(crypt_byte_msg, self.private_key)
            return pickle.loads(msg)
        elif size == 257:
            package_number = self.socket.recv(4)
            package_number = pickle.unpack('i', package_number)[0]
            result = b''
            for i in range(package_number):
                crypt_byte_msg = self.socket.recv(256)
                msg = rsa.decrypt(crypt_byte_msg, self.private_key)
                result = result + msg
            return pickle.loads(result)

    def send(self, msg):
        msg_byte = pickle.dumps(msg)
        if len(msg_byte) > 245:
            self.socket.sendall(pickle.pack('i', 257))
            package_number = (len(msg_byte) // 245) + 1
            self.socket.sendall(pickle.pack('i', package_number))
            for i in range(package_number):
                msg_to_send = msg_byte[i * 245:i * 245 + 245]
                crypt_byte_msg = rsa.encrypt(msg_to_send, self.key_rec)
                self.socket.sendall(crypt_byte_msg)
        elif len(msg_byte) <= 245:
            crypt_byte_msg = rsa.encrypt(msg_byte, self.key_rec)
            # pkg
            self.socket.sendall(pickle.pack('i', 256))
            self.socket.sendall(crypt_byte_msg)

    def setup(self):
        try:
            self.socket.connect(self.host)
            (self.pub_key, self.private_key) = rsa.newkeys(2048, poolsize=2)
            key = self.socket.recv(309)
            self.key_rec = pickle.loads(key)
            self.socket.sendall(pickle.dumps(self.pub_key))
            print(self.key_rec)
            return True
        except ConnectionRefusedError as e:
            print(e)
            print('连接失败')
            return False

    def send_cell(self, cell):
        self.send(1)
        self.send(cell)

    def ask(self, number):
        self.send(2)
        self.send(number)
        reply = self.recv()
        return reply

    def login(self, username, password):
        self.send((username,password))
        return self.recv()
