from multiprocessing import freeze_support
import server_c
from tkinter import *
import tkinter.messagebox

from ui_c import login_window


def main_window(cl):
    def add_xl():
        file = file_name_r.get().strip()
        cl.xl_read(file)

    def save_xl_all():
        file = file_name_w.get().strip()
        cl.xl_write(file)

    def save_xl_day():
        time = day.get().strip()
        file = file_name_w.get().strip()
        cl.xl_search_day(file, time)

    def add_user():
        cl.add_user(username.get().strip(), password.get().strip())

    def del_user():
        cl.del_user(username.get())

    root = Tk()
    root.title("管理系统主机端")

    # 录入 按时间导出 全部导出 用户管理

    record_frame = LabelFrame(root, text="导入", labelanchor="w")
    Label(record_frame, text='文件名（本目录）').grid(row=0)
    Button(record_frame, text='录入', command=add_xl).grid(column=1, row=1)
    file_name_r = StringVar()
    Entry(record_frame, textvariable=file_name_r).grid(column=0, row=1)

    get_frame = LabelFrame(root, text="导出", labelanchor="w")
    file_name_w = StringVar()
    Label(get_frame, text='文件名（本目录）').grid(row=0, column=0)
    Entry(get_frame, textvariable=file_name_w).grid(row=1, column=0, columnspan=2)
    Button(get_frame, text='全部导出', command=save_xl_all).grid(row=2, columnspan=2)
    day = StringVar()
    Entry(get_frame, textvariable=day, width=6).grid(row=3, column=0)
    Button(get_frame, text="按时间导出", command=save_xl_day).grid(row=3, column=1)

    user_manager = LabelFrame(root, text="账户管理", labelanchor='w')
    username = StringVar()
    Label(user_manager, text="用户名").grid(row=0, column=0)
    Entry(user_manager, textvariable=username).grid(row=0, column=1)
    password = StringVar()
    Label(user_manager, text="密码").grid(row=1, column=0)
    Entry(user_manager, textvariable=password).grid(row=1, column=1)
    Button(user_manager, text="注册", command=add_user).grid(row=2, column=0)
    Button(user_manager, text="删除", command=del_user).grid(row=2, column=1)

    get_frame.grid(row=0)
    record_frame.grid(row=1)
    user_manager.grid(row=2)

    root.mainloop()


if __name__ == '__main__':
    freeze_support()
    cl = server_c.SClient()
    try:
        if cl.setup():
            login_window(cl)
            main_window(cl)
    except ConnectionError:
        tkinter.messagebox.showerror("出错", "服务器未开启")
