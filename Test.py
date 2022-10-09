from base64 import decode
from cryptography.fernet import Fernet
import mysql.connector as sql

# Connecting to the DATABASE
Db = sql.connect(host="localhost", user="root",
                 passwd="19780000", database="flask", autocommit=True)
# Cursor on the DATABASE
cr = Db.cursor()

def Key():
    """Returns the Key to be used"""
    return open("Encryption.key","rb").read()

def Encrypt(String,Key=Key()):
    """Encrypts a string \nReturns Encrypted string"""
    return Fernet(Key).encrypt(String.encode())

def Decrypt(String,Key=Key()):
    """Decrypts a string \nReturns Decrypted string"""
    return Fernet(Key).decrypt(String).decode()

Email = Encrypt("dummy@email")
Passwd = Encrypt("4444")
UserName = "Ishika"

# print(f"UPDATE FLASK SET EMAIL="+ Email +", PASSWD= "+ Passwd +" WHERE USERNAME="+ UserName +";")
cr.execute("UPDATE FLASK SET USERNAME= %s, PASSWD= %s WHERE EMAIL= %s;",(UserName, Passwd, Decrypt(Email)))
# Db.commit()
# fnet = Fernet("ugAAJqBSpXQQcPZC_AC-A6zjqdxaYoYAh5-vtKhiW_g==")
# cr.execute("select * from flask;")

# Lst = [[i[0],Decrypt(i[1]),Decrypt(i[2])] for i in cr.fetchall()]

# for i in Lst:
#     print(f"{i[0]} : {i[1]} : {i[2]}")
