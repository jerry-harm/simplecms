import hashlib
import pickle
import xlrd
import xlwt


class Book:

    def __init__(self):
        self.sheet = {}

    def __add__(self, other):
        if other != None:
            for number in other:
                for task in other[number][1]:
                    self.change(number, other[number][0], task, other[number][1][task])
        else:
            pass

    # 删除无用号码
    # def del_useless_number(self):
    #     for number in self.sheet:
    #         if self.sheet[number][0] == '无' and len(self.sheet[number][1]) == 0:
    #             del self.sheet[number]

    # 增加
    def change(self, number: str, password: str, task: str, day: str) -> None:
        if number not in self.sheet:
            self.sheet[number] = []
            self.sheet[number].append(password)
            self.sheet[number].append(dict())
        else:
            self.sheet[number][0] = password
        self.sheet[number][1][task] = day

    # 查找时间
    def search_day(self, day: str) -> dict:
        result = {}
        for number in self.sheet:
            for task in self.sheet[number][1]:
                if self.sheet[number][1][task] == day:
                    result[number][0] = self.sheet[number][0]
                    result[number][1][task] = day
        return result

    # 存档
    def record_write(self, file='data'):
        with open(file, 'wb') as f:
            f.write(pickle.dumps(self.sheet))

    # 读档
    def record_read(self, file='data'):
        with open(file, 'rb') as f:
            byte = f.read()
            if byte != b'':
                data = pickle.loads(byte)
                self.__add__(data)

    # 存表
    def xl_write(self, file='data'):
        book_write = xlwt.Workbook()
        table = book_write.add_sheet('Sheet1')
        table.write(0, 0, "号码")
        table.write(0, 1, "备注")
        table.write(0, 2, "名称")
        table.write(0, 3, "日期")
        row = 1
        for number in self.sheet:
            password = self.sheet[number][0]
            for task in self.sheet[number][1]:
                table.write(row, 0, number)
                table.write(row, 1, password)
                table.write(row, 2, task)
                table.write(row, 3, self.sheet[number][1][task])
                row += 1
        book_write.save(file)

    # 读表
    def xl_read(self, file='data'):
        workbook = xlrd.open_workbook_xls(file)
        table = workbook.sheets()[0]
        rows = table.nrows
        for i in range(1, rows):
            row = table.row_values(i)
            self.change(str(row[0]), str(row[1]), str(row[2]), str(row[3]))


def get_md5(data):
    obj = hashlib.md5("a".encode('utf-8'))
    obj.update(data.encode('utf-8'))
    result = obj.hexdigest()
    return result


def test_hash(username, password):
    with open("hash", mode='r') as file:
        for txt in file.readlines():
            if txt.strip() == username + ":" + get_md5(password):
                return True


def get_host(file='host'):
    with open(file, mode='r', encoding='utf-8') as f:
        data = f.readlines()
        return tuple((str(data[0]).strip(), int(data[1])))


def search_user(username, data):
    for i in range(len(data)):
        if username == data[i].split(':')[0]:
            return i
    return None


def add_user(username, password, file='hash'):
    with open(file, mode='r+') as f:
        data = f.readlines()
        f.seek(0)
        f.truncate(0)
        i = search_user(username, data)
        if i is not None:
            line = data[i].strip().split(':')
            line[1] = get_md5(password)
            data[i] = ':'.join(line) + '\n'
            f.write(''.join(data))
        else:
            data.append(username + ':' + get_md5(password)+'\n')
            f.write(''.join(data))


def del_user(username, file='hash'):
    with open(file, mode='r+') as f:
        data = f.readlines()
        f.seek(0)
        f.truncate(0)
        i = search_user(username, data)
        if i is not None:
            del data[i]
            f.write(''.join(data))
        else:
            f.write(''.join(data))


if __name__ == '__main__':
    a = test_hash('1', '1')
