from multiprocessing import freeze_support
import pickle
import socketserver
import rsa
import core
import threading


class MyTCPHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)

    def recv(self):
        size_byte = self.request.recv(4)
        size = pickle.unpack('i', size_byte)[0]
        # print(size)
        if size == 256:
            crypt_byte_msg = self.request.recv(256)
            msg = rsa.decrypt(crypt_byte_msg, self.private_key)
            return pickle.loads(msg)
        elif size == 257:
            package_number = self.request.recv(4)
            package_number = pickle.unpack('i', package_number)[0]
            result = b''
            for i in range(package_number):
                crypt_byte_msg = self.request.recv(256)
                msg = rsa.decrypt(crypt_byte_msg, self.private_key)
                result = result + msg
            return pickle.loads(result)

    def send(self, msg):
        msg_byte = pickle.dumps(msg)
        if len(msg_byte) > 245:
            self.request.sendall(pickle.pack('i', 257))
            package_number = (len(msg_byte) // 245) + 1
            self.request.sendall(pickle.pack('i', package_number))
            for i in range(package_number):
                msg_to_send = msg_byte[i * 245:i * 245 + 245]
                crypt_byte_msg = rsa.encrypt(msg_to_send, self.key_rec)
                self.request.sendall(crypt_byte_msg)
        elif len(msg_byte) <= 245:
            crypt_byte_msg = rsa.encrypt(msg_byte, self.key_rec)
            # pkg
            self.request.sendall(pickle.pack('i', 256))
            self.request.sendall(crypt_byte_msg)

    def login(self):
        hash_get = self.recv()
        if core.test_hash(hash_get[0], hash_get[1]):
            self.user = hash_get[0]
            print("test pass")
            self.send(True)
        else:
            self.send(False)

    def get_cell(self):
        cell = self.recv()
        for num in cell:
            length = len(cell[num][1])
            if (cell[num][0] != '无') or (length > 0):
                if num in work_book.sheet:
                    lock.acquire()
                    work_book.sheet[num] = cell[num]
                    lock.release()
                else:
                    lock.acquire()
                    work_book.sheet[num] = []
                    work_book.sheet[num] = cell[num]
                    lock.release()
        

    def reply(self):
        number = self.recv()
        if number in work_book.sheet:
            cell = work_book.sheet[number]
            self.send(cell)
        else:
            print('新号码')
            self.send(None)

    def reply_operate(self, operate):
        if operate is None:
            print("none")
        elif operate == 1:
            self.get_cell()
        elif operate == 2:
            self.reply()

    def server_operate(self, operate):
        if operate is None:
            print('none')
        elif operate == 3:
            file = self.recv()
            work_book.xl_write(file)
        elif operate == 4:
            file = self.recv()
            lock.acquire()
            work_book.xl_read(file)
            lock.release()
        elif operate == 5:
            file = self.recv()
            day = self.recv()
            temp_book = core.Book()
            temp_book.sheet = work_book.search_day(day)
            temp_book.xl_write(file)
        elif operate == 6:
            user = self.recv()
            password = self.recv()
            core.add_user(user, password)
        elif operate == 7:
            user = self.recv()
            core.del_user(user)

    def setup(self):
        lock.acquire()
        work_book.record_read()
        lock.release()
        print("before handle,连接建立：", self.client_address)
        (self.pub_key, self.private_key) = rsa.newkeys(2048, poolsize=2)
        self.request.sendall(pickle.dumps(self.pub_key))
        key = self.request.recv(309)
        self.key_rec = pickle.loads(key)
        print(self.key_rec)
        try:
            self.login()
        except ConnectionError as e:
            print('登录失败')
            self.server.shutdown_request(self.request)
            self.server.close_request(self.request)
            print(e)

    def handle(self):
        try:
            while True:
                operate = self.recv()
                if self.client_address[0] == host[0]:
                    self.server_operate(operate)
                    self.reply_operate(operate)
                else:
                    self.reply_operate(operate)
                print(operate)
                work_book.record_write()
        except Exception as e:
            print(self.client_address, "连接断开", e)
        finally:
            work_book.record_write()
            self.server.shutdown_request(self.request)
            self.server.close_request(self.request)

    def finish(self):
        work_book.record_write()


if __name__ == '__main__':
    freeze_support()
    lock = threading.Lock()
    work_book = core.Book()
    host = core.get_host()
    server = socketserver.ThreadingTCPServer(host, MyTCPHandler)  # 多线程版
    server.serve_forever()
