import json
import os
from dotenv import load_dotenv
from firebase_admin import db
import pyrebase

load_dotenv()


serviceAccountKey = json.loads(os.getenv("SERVICE_ACCOUNT_KEY"))
firebaseConfig = json.loads(os.getenv("FIREBASE_CONFIG"))
firebaseConfig ["serviceAccount"] = serviceAccountKey



firebase = pyrebase.initialize_app(firebaseConfig)

pyrDB = firebase.database()

User_data = [{
    "email" : '',
    "name" : '' ,
    "links" : {}
}]

User_idToken = ''
links = {}

def reomve_special_char(s):
    spcl = "!@$%^&()}{][';:-+=_.//\\?>.`~"
    ans =''
    for i in list(s):
        if i in spcl:
            pass
        else:
            ans+=i
    return ans

def update_user_data(name , email , links={} ):
    global User_idToken
    for i in links:
        User_data[0]['links'][i] = links[i]
    User_data[0]['email'] = email
    User_data[0]['name'] = name
    User_idToken = reomve_special_char(email)



def resetUserData():
    global User_data,User_idToken,links
    User_data = [{
        "email" : "",
        "name" : "",
        "links" : {}
    }]
    User_idToken = ''
    links = {}

def clear_Screen():
    for i in range(20):
        print()

def give_space():
    print()
    print('-'*20)
    print()

def remove_spaces_from_string(s):
    a = list(s)
    s=''
    for i in a:
        s+=i
    return s



def get_data():
    global User_email,User_idToken,User_name,User_data
    User_data = pyrDB.child(User_idToken).get()
    return User_data.key(),User_data.val()

def get_links():
    global User_data
    give_space()
    for i in User_data[0]['links'].keys():
        print(f'{i}  :  {User_data[0]["links"][i]}')
    give_space()
    input()


def commit_database():
    global  User_data,User_idToken
    try:
        pyrDB.child(User_idToken).set(User_data)
        return True
    except Exception as e:
        print(e)
        return False


def SignIn():
    global User_idToken,User_data
    Uemail = input("Email : ")
    Upass = input("Password : ")
    try:
        u = firebase.auth().sign_in_with_email_and_password(Uemail.strip(),Upass)
        User_idToken = reomve_special_char(u['email'])
        User_data = get_data()[1]
    except Exception as e: 
        if(str(type(e)) == "<class 'requests.exceptions.HTTPError'>"):
            give_space()
            print("Invalid Cradentials! Try Again")
            input()
        else:
            give_space()
            print(e,type(e))
            input()

def SignUp():
    global User_idToken,User_data
    give_space()
    while True:
        name = input("Full Name : ").strip()
        email = input("Email : ").strip()
        passwd = input("Password : ")
        cpasswd = input("Confirm Password : ")
        try:
            if len(email) and passwd == cpasswd and len(passwd)>7:
                res =firebase.auth().create_user_with_email_and_password(email,passwd)
                update_user_data(name,email)
                commit_database()
                print(User_data)
                return res
            else:
                give_space()
                print("Enter the cradentials prperly !!")
                continue
        except Exception as e:
            if str(type(e)) == "<class 'requests.exceptions.HTTPError'>":
                give_space()
                print("User already exists with the mail !!\nTry using another mail or Choose Reset password from main menue !!")
        input()


def passwrdReset(email):
    try:
        firebase.auth().send_password_reset_email(email.strip())
        return "Password reset link has been sent to the given email address !!"
    except Exception as e:
        if str(type(e)) == "<class 'requests.exceptions.HTTPError'>":
                return "Email doesn't exist in the database, Try again !!"


def save_link():
    global User_data
    while True:
        give_space()
        link = input("Enter the link : ")
        name = input("Give it a name : ")
        User_data[0]['links'][name] = link
        ch = input("want to add more ? (y for yes) >>> ")
        if ch != 'y' and ch != 'Y':
            break
    if(commit_database()):
        give_space()
        print("Link added successfully !!")
    else:
        give_space()
        print("Something went wrong whiling saving the data !! (Try again by using another name of the link)")
    give_space()
    input()
def delete_data():
    global User_data
    get_links()
    key = input("Enter the name of the website : ")
    give_space()
    try : 
        u = User_data[0]['links'].pop(key)
        if commit_database():
            print(u,"deleted ")
            give_space()
        else:
            print("Something went wrong while deliting from the database !!")
    except Exception as e:
        if e:
            print("Given name doesn't exist !")

def change_details():
    global User_data
    passwd = input("Enter password to verify : ")
    try: 
        firebase.auth().sign_in_with_email_and_password(User_data[0]["email"],passwd)
        name = input("Enter your name : ")
        email = input("Enter you Email : ")
        update_user_data(name,email)
        commit_database()
    except Exception as e:
        if(str(type(e)) == "<class 'requests.exceptions.HTTPError'>"):
            give_space()
            print("Incorrent password !")
            input()
        else:
            give_space()
            print(e,type(e))
            input()

def clear_all_link():
    global User_data,links
    give_space()
    links = {}
    User_data[0]['links'] = links
    if commit_database():
        print("Deleted all saved linkes successfully !!")
    else:
        print("Something went wrong while deleting the links !!")
    give_space()

def init():
    while True:
        if User_idToken != '':
            print("User Name : ",User_data[0]['name'],"\n")
            print("1 - Save link")
            print("2 - Get link")
            print("3 - Delete link")
            print("4 - Clear all saved links")
            print("5 - SignOut corrent user")
            ch = input(">>> ")
            if ch=='1':
                save_link()
            elif ch=='2':
                get_links()
            elif ch=='3':
                delete_data()
            elif ch=='4':
                clear_all_link()
            elif ch=='5':
                resetUserData()
            else:
                continue
        else:
            clear_Screen()
            print("1 - SignIn")
            print("2 - SignUn")
            print("3 - Reset Password")
            print("or any other to exit!")
            ch = input(">>> ")
            if ch == '1':
                give_space()
                SignIn()
                give_space()
            elif ch == '2':
                SignUp()
                give_space()
            elif ch == '3':
                give_space()
                toast = passwrdReset(input("Enter email address, we will send you password reset link\n>>> "))
                print(toast)
                input()
                if toast == "Email doesn't exist in the database, Try again !!":
                    continue
            else:
                give_space()
                print("Bye 👋")
                print('\n'*4)
                break
if __name__ == "__main__":
    init()
