from multiprocessing import freeze_support
from tkinter import *
import tkinter.messagebox
import client
from sys import exit

def login_window(cl):
    root = Tk()
    root.title('登录')

    def login():
        username = name.get()
        password = pwd.get()
        if cl.login(username, password):
            root.destroy()
        else:
            tkinter.messagebox.showwarning('错误','登录失败')
            root.destroy()
            exit()

    frame1 = Frame(root)

    Label(frame1, text="姓名").grid(row=0, column=0)
    Label(frame1, text="密码").grid(row=1, column=0)

    name = StringVar()
    pwd = StringVar()

    Entry(frame1, textvariable=name).grid(row=0, column=1)
    Entry(frame1, textvariable=pwd, show="*").grid(row=1, column=1)

    Button(frame1, text="登录", command=login).grid(row=2, columnspan=2)

    frame1.pack()
    root.attributes("-topmost", 1)
    root.mainloop()

def main_window(cl):
    root = Tk()
    root.title("管理系统客户端")

    def ask_number(event):
        ask = number.get().strip()
        if len(ask) == 11 and event is not None:
            try:
                cell = cl.ask(ask)
                if cell is not None:
                    password.set(cell[0])
                    text.delete('0.0', END)
                    for task in cell[1]:
                        msg = task + ' ' + cell[1][task] + '\n'
                        text.insert(END, msg)
                else:
                    text.delete('0.0', END)
                    password.set('')
            except Exception as e:
                print(e)
                tkinter.messagebox.showerror("出错", "重新登录")
        else:
            pass

    def send():
        string = text.get('0.0', 'end')
        num = number.get()
        pwd = password.get().strip()
        if pwd == '':
            pwd = '无'
        if len(num) == 11:
            cell = {num:[pwd,{}]}
            for i in string.strip().split("\n"):
                if i != '\n':
                    active = i.split(' ')
                    if len(active) == 2:
                        if active[0] not in cell[num][1]:
                            cell[num][1][active[0]]=active[1]
            try:
                cl.send_cell(cell)
                text.delete('0.0', END)
                # tkinter.messagebox.showinfo('成功','录入成功')
            except ConnectionError as e:
                tkinter.messagebox.showerror("出错", "重新登录")
        else:
            return None

    # prepare
    number = StringVar()
    number_label = Label(root, text="号码")
    number_entry = Entry(root, textvariable=number)
    number_entry.bind('<FocusOut>', ask_number)
    number_entry.bind('<Return>', ask_number)

    password = StringVar()
    password_label = Label(root, text="备注")
    password_entry = Entry(root, textvariable=password)

    text = Text(root, width=30, height=20, undo=True, autoseparators=False)

    send_button = Button(root, text="提交", command=send)

    # place
    number_label.grid(column=0)
    password_label.grid(row=0, column=1)
    number_entry.grid(row=1, column=0)
    password_entry.grid(row=1, column=1)
    text.grid(row=2, columnspan=2)
    send_button.grid(row=3, columnspan=2)

    root.attributes("-topmost", 1)
    root.mainloop()


if __name__ == '__main__':
    freeze_support()
    cl = client.Client()
    try:
        if cl.setup():
            login_window(cl)
            main_window(cl)
    except ConnectionError:
        tkinter.messagebox.showerror("出错", "服务器未开启")
        exit()
