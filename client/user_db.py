import sqlite3
class db:
    def __init__(self):
        self.conn=sqlite3.connect('A:/trash/CPISfiles/usersDB.db')
        self.cur=self.conn.cursor()

    def __del__(self):
        self.conn.close()


    def checkUser(self, login, password):
        #check user existense in table
        self.cur.execute("SELECT EXISTS(SELECT 1 FROM userInfo WHERE userLogin=? and userPassw=?)", (login, password,))
        res=self.cur.fetchone()
        if res[0]==0:
            #insert new user
            self.cur.execute("INSERT INTO userInfo(userLogin, userPassw) VALUES(?,?)", (login, password))
            self.conn.commit()
        self.cur.execute("SELECT userId FROM userInfo where userLogin=? and userPassw=?",(login, password,))
        self.curUserId=self.cur.fetchone()


    def insertPrivateKeyRSA(self, privateKeyRSA):
        data=(self.curUserId+privateKeyRSA)
        self.cur.execute("INSERT INTO private_keysRSA(id_user, private_keyRSA,date ) VALUES(?,?,?)",data)
        self.conn.commit()

    def insertPrivateKeySign(self, privateKeySign):
        data=(self.curUserId+privateKeySign)
        self.cur.execute("INSERT INTO private_keysSign(id_user, private_keySign, date) VALUES(?,?,?)",data)
        self.conn.commit()

    def getPrivateKeyRSA(self):
        self.cur.execute("select *  from private_keysRSA where id_user=? order by id desc limit 1", self.curUserId)
        res=self.cur.fetchone()
        return res

    def getPrivateKeySign(self):
        self.cur.execute(" select * from private_keysSign where id_user=? order by id desc limit 1", self.curUserId)
        return self.cur.fetchone()

    