import client


class SClient(client.Client):
    def xl_write(self,file):
        self.send(3)
        self.send(file)

    def xl_read(self,file):
        self.send(4)
        self.send(file)

    def xl_search_day(self,file,day):
        self.send(5)
        self.send(file)
        self.send(day)

    def add_user(self,user,password):
        self.send(6)
        self.send(user)
        self.send(password)

    def del_user(self,user):
        self.send(7)
        self.send(user)
