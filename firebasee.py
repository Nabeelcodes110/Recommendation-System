import pyrebase

config ={
        'apiKey': "AIzaSyA1l8z2Ykz4aBcAt9-vjXKK6DBGzqoBX4Y",
        'authDomain': "aqsa-recommend.firebaseapp.com",
        'projectId': "aqsa-recommend",
        'storageBucket': "aqsa-recommend.appspot.com",
        'messagingSenderId': "783852311498",
        'appId': "1:783852311498:web:c88764d7cf044b31953533",
        'measurementId': "G-NL2VWLZLNK",
        'databaseURL': "https://aqsa-recommend-default-rtdb.firebaseio.com"
} 

firebase=pyrebase.initialize_app(config)

# ********************************************AUTHENTICATION*****************************

# auth = firebase.auth()

# email = 'test@gmail.com'
# password ='123456' #password has to be 6 didgit

# # user=auth.create_user_with_email_and_password(email,password)
# # print(user)

# user = auth.sign_in_with_email_and_password(email,password)

# # info = auth.get_account_info(user['idToken'])
# # print(info)

# auth.send_email_verification(user['idToken'])

# auth.send_password_reset_email(email)

# *********************************************AUTHENTICATION*****************************



# *********************************************DATABASE***********************************
db = firebase.database()
db.child("names").push({"username":"paddy"})
# db.child("names").child("username").update({"username":"PArry"})
# users = db.child("names").child("username").get()
# print (users.val())

# db.child("names").remove()

# *********************************************DATABASE***********************************
