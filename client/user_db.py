import sqlite3
import pickle
class db:
    def __init__(self):
        self.conn=sqlite3.connect('A:/trash/CPISfiles/usersDB.db')
        self.cur=self.conn.cursor()

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


    def getAllUserLogin(self):
        self.cur.execute("select userLogin from userInfo")
        return self.cur.fetchall()

    def getUserDataByLogin(self, login):
        self.cur.execute("select userLogin, userPassw from userInfo where userLogin=?", (login, ))
        return self.cur.fetchone()
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

    def getByIdPrivateKeyRSA(self, id):
        self.cur.execute("select private_keyRSA from private_keysRSA where id=?", (id, ))
        return self.cur.fetchone()

    def getPrivateKeySign(self):
        self.cur.execute(" select * from private_keysSign where id_user=? order by id desc limit 1", self.curUserId)
        return self.cur.fetchone()

    def getByIdPrivateKeySign(self, id):
        self.cur.execute("select private_keySign from private_keysSign where id=?", (id, ))
        return self.cur.fetchone()

    def getPrivateKeysId(self):
        self.cur.execute(
            "select private_keysRSA.id, private_keysSign.id from private_keysRSA, private_keysSign where private_keysRSA.id_user=? and private_keysSign.id_user=? order by private_keysRSA.id desc,private_keysSign.id desc limit 1",
            (self.curUserId[0], self.curUserId[0]))
        return self.cur.fetchone()

    def insertPublicKeys(self, public_data):
        self.cur.execute("insert into public_keys(id_user,user_login,id_keyRSA, public_keyRSA,id_keySign, public_keySign) values(?,?,?,?,?,?)", (self.curUserId+public_data))
        self.conn.commit()

    def getPublicKeysByLogin(self, login):
        self.cur.execute("select id_keyRSA,public_keyRSA, id_keySign, public_keySign from public_keys where id_user=? and user_login=? order by id desc limit 1", (self.curUserId[0],login))
        return self.cur.fetchone()

    def getByIdPublicKeySign(self, login, id):
        self.cur.execute("select public_keySign from public_keys where user_login=? and id_keySign=?", (login, id))
        return self.cur.fetchone()

    def checkPublicKeys(self, login):
        self.cur.execute("SELECT EXISTS(SELECT 1 FROM public_keys WHERE id_user=? and user_login=?)", (self.curUserId[0],login))
        res=self.cur.fetchone()
        if res[0]==1:
            return True
        else:
            return False

    def checkPublicKeysByIds(self, login, id_keyRSA, id_keySign):
        self.cur.execute("select exists(select 1 from public_keys where id_user=? and user_login=? and id_keyRSA=? and id_keySign=?)", (self.curUserId[0], login, id_keyRSA, id_keySign))
        res=self.cur.fetchone()
        if res[0]==1:
            return True
        else:
            return False
    def getSendersList(self):
        self.cur.execute("select user_login from public_keys where id_user=?", self.curUserId)
        return self.cur.fetchall()

    def getPublicKeyRSA(self, login):
        self.cur.execute(" select id_keyRSA, public_keyRSA from public_keys where id_user=? and user_login=? order by id desc limit 1",(self.curUserId[0], login))
        return self.cur.fetchone()

    def insertLetter(self,folder_name, letter):
        data=pickle.dumps(letter,0)
        self.cur.execute("insert into letters(id_user, folder_name, letter) values(?,?,?)", (self.curUserId[0], folder_name, data))
        self.conn.commit()

    def deleteAllLetters(self):
        self.cur.execute("delete from letters where id_user=?", self.curUserId)
        self.conn.commit()

    def getAllLetters(self):
        self.cur.execute("select folder_name, letter from letters where id_user=?", self.curUserId)
        return self.cur.fetchall()




