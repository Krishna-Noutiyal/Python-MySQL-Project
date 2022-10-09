
Db.commit()
fnet = Fernet("ugAAJqBSpXQQcPZC_AC-A6zjqdxaYoYAh5-vtKhiW_g==")
cr.execute("select * from flask;")

Lst = [[i[0],Decrypt(i[1]),Decrypt(i[2])] for i in cr.fetchall()]

for i in Lst:
    print(f"{i[0]} : {i[1]} : {i[2]}")
