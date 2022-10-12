import json
from flask import Flask, render_template, redirect, url_for, request
import mysql.connector as sql
from cryptography.fernet import Fernet
app = Flask(__name__)

log = False
UserName = ""
Passwd = ""

def Key():
    """Returns the Key to be used"""
    return open("Encryption.key","rb").read()

def Encrypt(String,Key=Key()):
    """Encrypts a string \nReturns Encrypted string"""
    return Fernet(Key).encrypt(String.encode())

def Decrypt(String,Key=Key()):
    """Decrypts a string \nReturns Decrypted string"""
    return Fernet(Key).decrypt(String).decode()


# Variable containing the Mode of the website if dark ('dark') if light ('')
BodyMode = ""
SideBar = ""

# Display : Msg1 displayed if UserName and Passwd is incorrect
Display = ""

# Display : Msg2 displayed if UserName and Passwd is incorrect
Display1 = ""

# Msg Displayed when redirected from Signup page to Login Page
SingupDisplay=""
SingupDisplay1=""


@app.route("/Mode", methods=['POST', 'GET'])
def UpdateMode():
    """Checks if User has toggled dark mode add 'dark' in BodyMode if DARK MODE is enabled else blank"""

    global BodyMode
    # If the Toggle Mode Button is pressed
    # JS generates a Post request with the ITS DATA = CLASS OF THE BODY
    if request.method == "POST":

        # Variable containg the Class of the Body
        RequestContent = json.loads(request.data)

        # print(f"Theme of the Website : {RequestContent}")

        # Setting the BodyMode
        BodyMode = RequestContent
        return f"Website Mode changed to {'Dark' if BodyMode == 'dark' else 'Light'} Successfully"

    # To set the Mode of the website JS automatically
    # Sends a GET request to get the Current mode of the body
    # Returns the Mode of the body to JS
    elif request.method == "GET":
        return BodyMode

@app.route("/Sidebar", methods=['POST', 'GET'])
def Sidebar():
    """Checks if User has toggled dark mode add 'dark' in BodyMode if DARK MODE is enabled else blank"""

    global SideBar
    # If the Toggle Sidebar Button is pressed
    # JS generates a POST request with containing DATA = CLASS OF THE BODY
    if request.method == "POST":

        # Variable containg the Class of the Body
        RequestContent = json.loads(request.data)

        # print(f"Sidebar Folding : {RequestContent}")

        # Setting the BodyMode
        SideBar = RequestContent
        return f"SideBar folding changed to {'close' if Sidebar == 'close' else 'open'} Successfully"

    # To set the Sidebar of the website, JS automatically
    # Sends a GET request for Current folding state of Sidebar
    # Returns the Folding of Sidbar to JS
    elif request.method == "GET":
        return SideBar


""" Index PAGE """


@app.route("/")
def Index():
    # If the user has logged in to the WEBSITE
    if log == True:
        return render_template("Index.html", Content=f"Logged in Successfully !!")
    # If the user has not yet Logged in to the WEBSITE
    return render_template("Index.html", Content="Welcome to Home Page !!")


""" About PAGE """


@app.route("/About")
def About():
    return render_template("About.html", Content="This is About Page")


""" Memories PAGE """


@app.route("/Memories")
def Memories():
    return render_template("Memories.html", Content="This is Memories Page")


""" Projects PAGE """


@app.route("/Projects")
def Projects():
    return render_template("Projects.html", Content="This is Projects Page")


""" Gallery PAGE """


@app.route("/Gallery")
def Gallery():
    return render_template("Gallery.html", Content="This is Gallery Page")


""" Contact PAGE """


@app.route("/Contact")
def Contact():
    return render_template("Contact.html", Content="This is Contact Page")


""" Login OR Not"""

@app.route("/Loginornot", methods=["GET"])
def LoginOrNot():
    global log
    return json.dumps(log)


""" Login PAGE """

@app.route("/Login", methods=["POST", "GET"])
def Login():
    """Saves UserName and Password in the Globle Variables and changes log = True"""
    global log
    global Display
    global Display1
    global SingupDisplay
    global SingupDisplay1

    # Style of the Warning
    Style = 'style="font-size: 19px; color: red; text-align: center;"'
    
     #   If the Form   is Submitted
    if request.method == "POST":


        # Try except if UserName and Passwd is not in the DATABASE
        try:
            
            # Gets the data from server and stores in UserInfo dict (Username:Passwd)
            cr.execute("SELECT USERNAME,PASSWD,EMAIL FROM FLASK;")
            UserInfo = {i[0]: [Decrypt(i[2]),Decrypt(i[1])] for i in cr.fetchall()}
            for i,j in UserInfo.items():
                print(f"UserName : {i}")
                print(f"Email : {j[0]}")
                print(f"Passwd : {j[1]}")
            # UserName taken from the FORM
            UserName = request.form["Usr"]
            # Passwd taken from the FORM
            Passwd = request.form['Passwd']
            # If Credentials in the database does not match the User Input
            # Raises an Exception
            if UserInfo[UserName][1] != Passwd:

                raise Exception("Wrong UserName")

            # If Credentials matches Sets log varaible = true
            # Means user is now Loged in the Website
            else:
                log = True
                return redirect(url_for("Index"))

        # If Exception Occur Changes Display and Displa1 varaible
        # And Renders the Login page again but with the Msg of Display and Display1
        except Exception as e:
            Display = "Wrong UserName or Password"
            Display1 = "!! TRY AGAIN !!"

            return render_template("Login.html",Style=Style, Msg1=Display, Msg2=Display1)
            

    # If User has not yet Loged in to the website GET request
    else:

        # If user has clicked login button
        if log == False and SingupDisplay == "" and SingupDisplay1 == "":

            # Style of the Warning
            Style = 'style="font-size: 19px; color: red; text-align: center; display: none; "'

            return render_template("Login.html",Style = Style, Msg1 = Display, Msg2 = Display1)


        # If user has been redirected to Login from Signup Page
        elif log == False and  SingupDisplay != "" and SingupDisplay1 != "":
            a = SingupDisplay
            b = SingupDisplay1
            SingupDisplay = ""
            SingupDisplay1 = ""

            # Changeing the Warning color to orange
            Style = Style.replace("red","orange")
            return render_template("Login.html",Style = Style, Msg1 = a, Msg2 = b)

        # If User has logged in 
        else:
            log = False
            
            # Clearing the Variables after the logout
            # Because if user fails to login once before successfully loggin in
            # the Variables values doesn't get cleared 
            # Showing the error msg again even after logout
            Display = ""
            Display1 = ""
            return redirect(url_for("Index"))


""" Signup Page"""

@app.route("/Signup", methods=["POST","GET"])
def Signup():
    global Display
    global Display1
    global SingupDisplay
    global SingupDisplay1
    Msg1 = ""
    Msg2 = ""
    Style = 'style="font-size: 20px; color: red; text-align: center; display: none;"'
    
    
    # If users submits the form
    if request.method =="POST":


        # Storing the form input to variables
        UserName = request.form["Usr"]
        Email = request.form["Email"].lower()
        Passwd = Encrypt(request.form["Passwd"])

        # Check if the Email and UserName already exist in the database or not
        # If exist throws an error 
        # If not exist adds the new user to database
        try:

            # Executing mysql quiery
            cr.execute("select email from flask;")

            # List of all emails on the server 
            l = [Decrypt(j) for i in cr.fetchall() for j in i]
            print(l)

            # IF email is in Database Throws and error
            if (Email in l) is True:
                raise Exception("Email already used !!")

            # Else Adds new user to Database
            else:
                # Encrypting the Email before sending to Database
                Email = Encrypt(Email)

                cr.execute("INSERT INTO flask(UserName,Passwd,Email) values(%s,%s,%s)",(UserName,Passwd,Email))

                # Commiting the changes
                Db.commit()
                
                # List of all emails on the server
                l = [Decrypt(j) for i in cr.fetchall() for j in i]
                print(l)

                SingupDisplay="!!! Successfully Signed Up !!!"
                SingupDisplay1="You Can Login Now"
                return redirect(url_for("Login"))

        except :
            Msg1 = "UserName or Email already Taken"
            Msg2 = "!! Use another UserName or Email !!"    
            Style = Style.replace("display: none;","")
            redirect(url_for("Signup"))
    
    return render_template("SignUp.html",Style = Style,Msg1= Msg1, Msg2= Msg2)


""" Forgot Page"""

@app.route("/Forgotpasswd",methods=["POST","GET"])
def Forgot():

    Style = 'style="font-size: 19px; color: red; text-align: center;"'
    # If the request is POST 
    if request.method == "POST":

        # Email Entered by the user
        Email = request.form["Email"]
        
        try:
            # SQL Quiery to retrieve UserName Email and Password fromt he database
            cr.execute("select Username,Email,Passwd from flask;")

            # List containing the data of the user in Decrypted form
            Lst = [[i[0],Decrypt(i[1]),Decrypt(i[2])] for i in cr.fetchall() ]
            for i in Lst:

                # If the Email is in database
                if i[1] == Email:
                
                    # Changes the style color to orange 
                    Style = Style.replace("red","orange")

                    # Renders the forget.html with UserName and Password of the Associated Email
                    return render_template("Forgot.html",Style = Style,Msg1=f"UserName : {i[0]}", Msg2=f"Password : {i[2]}")
            
            raise Exception("Email Not Associated with any Account")
        except Exception as e:
            return render_template("Forgot.html", Style=Style, Msg1=f"No Account Found Associated With", Msg2=f"{Email}")

    # Changes the style Display : none; to avoid unnecessary spacing if no warning is displayed
    Style = 'style="font-size: 19px; color: red; text-align: center; display : none ;"'
    return render_template("Forgot.html",Style = Style)

@app.route("/ChangeCredentials",methods=["POST","GET"])
def ChangeCredentials():
    global cr
    global Db

    # Style for the Msg
    Style = 'style="font-size: 18px; color: red; text-align: center; display: none;"'

    # If the request is POST 
    if request.method == "POST":

        
        # Storing the form input to variables
        Email = request.form["Email"].lower()
        UserName = request.form["Usr"]
        Passwd = Encrypt(request.form["Passwd"])


        # SQL Quiery to retrieve UserName Email and Password fromt he database
        cr.execute("select Username,Email,Passwd from flask;")

        # List containing the data of the user in Decrypted form
        Lst = [[i[0],i[1],i[2]] for i in cr.fetchall()]


        for i in Lst:

            # If the UserName and Email matches
            if i[0] == UserName and Decrypt(i[1]) == Email:

                # Style for the Message
                Style = Style.replace("display: none;","")
                Style = Style.replace("red","orange")

                # Updates the Username Email and Password 
                cr.execute("UPDATE FLASK SET USERNAME = %s, EMAIL = %s, PASSWD = %s WHERE USERNAME = %s and EMAIL = %s;", (UserName,Encrypt(Email), Passwd, UserName,i[1]))
                return render_template("ChangeCredentials.html", Style = Style, Msg0 = f"New Credentials !!", Msg1 = f"Username : {UserName}", Msg2 = f"Email : {Email}", Msg3 = f"Password : {Decrypt(Passwd)}")
            
            # elif Decrypt(i[1]) == Email:
            #     cr.execute("UPDATE FLASK SET USERNAME= %s, PASSWD= %s WHERE EMAIL= %s;",(UserName,Passwd,i[1]))
                # return render_template("ChangeCredentials.html",Warning="orange",Msg0=f"New Credentials !!", Msg1=f"Username : {UserName}", Msg2=f"Email : {Email}", Msg3=f"Password : {Decrypt(Passwd)}")
        

        # Style for the Msg
        Style = Style.replace("display: none;","")

        # After for loop if Username and Email doesn't matches Throwes an error on the page
        return render_template("ChangeCredentials.html", Style = Style, Msg0=f"Credentials Doesn't Match", Msg1=f"!! Enter Email or UserName Correctly !!")
    
    # If the request is GET
    else:
        return render_template("ChangeCredentials.html", Style=Style)


@app.route("/<i>/")
def ReRoute(i=str):
    return render_template("PageNotFound.html")


if __name__ == "__main__":

    # Connecting to the DATABASE
    Db = sql.connect(host="localhost", user="root",passwd="19780000", database="flask", autocommit=True)

    # Cursor on the DATABASE
    cr = Db.cursor()
    app.run(debug=True) 
