from flask import Flask,render_template,request, redirect, url_for, session
import pyrebase
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl','rb'))
X = pickle.load(open('X.pkl','rb'))
ratings = pickle.load(open('ratings1.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))
correlation_matrix = pickle.load(open('correlation_matrix.pkl','rb'))

product = list(popular_df['product_id'].values)
rating = list(popular_df['rating_x'].values)
image = list(popular_df['image_url'].values)
price = list(popular_df['price'].values)
print(similarity_scores.shape)
app = Flask(__name__)

#FIREBASE AUTHENTICATION **********************************
config ={
        'apiKey': "AIzaSyA1l8z2Ykz4aBcAt9-vjXKK6DBGzqoBX4Y",
        'authDomain': "aqsa-recommend.firebaseapp.com",
        'projectId': "aqsa-recommend",
        'storageBucket': "aqsa-recommend.appspot.com",
        'messagingSenderId': "783852311498",
        'appId': "1:783852311498:web:c88764d7cf044b31953533",
        'measurementId': "G-NL2VWLZLNK",
        'databaseURL':''
} 

firebase=pyrebase.initialize_app(config)
auth = firebase.auth()

app.secret_key='secret'




@app.route('/')
def index():
    return render_template('index.html',
                            product = product[0:12],
                           rating = np.round_(rating, decimals = 1)[0:12],
                           image = image[0:12],
                           price = price[0:12]
                           )


@app.route('/signup', methods=['GET', 'POST'])
def signup():
             
        if request.method == 'POST':
            # Handle form data here
            email = request.form['username']
            password = request.form['password']
            # Save the user data to a database, file, or other storage method
            # For this example, we'll just print the data to the console
            # user=auth.create_user_with_email_and_password(email,password)
            print(f"New user: {email}, password: {password}")
            
        # If the request method is GET, show the signup form
        return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
        if ('user' in session):
            #  return 'HI, {}'.format(session['user'])
            return render_template('index.html',
                          product = product[12:],
                           rating = np.round_(rating, decimals = 1)[12:],
                           image = image[12:],
                           price = price[12:]
                           )

        if request.method == 'POST':
            # Handle form data here
            email = request.form['username']
            password = request.form['password']
            # Check the user's credentials against the database, file, or other storage method
            # For this example, we'll just print the data to the console
            print(f"User login: {email}, password: {password}")
            try:
                user = auth.sign_in_with_email_and_password(email,password)
                session['user'] = email
            except:
                 return 'Failed to login'
            return redirect(url_for('login'))
        # If the request method is GET, show the login form
        return render_template('login.html')


@app.route('/profile')
def profile():
    user = session['user']
    if (user != ""):
        return render_template('profile.html', user=user)
    else:
         return render_template('login.html')
        


@app.route('/logout')
def logout():
    session.pop('user')
    return render_template('index.html',
                           product = list(popular_df['product_id'].values)[0:12],
                           rating = list(popular_df['rating_x'].values)[0:12],
                           image = list(popular_df['image_url'].values)[0:12],
                           price = list(popular_df['price'].values)[0:12]
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html',
                           product = list(popular_df['product_id'].values)[12:],
                           rating = list(popular_df['rating_x'].values)[12:],
                           image = list(popular_df['image_url'].values)[12:],
                           price = list(popular_df['price'].values)[12:]
                           )



@app.route('/recommend_kurtis', methods=['post'] )
def recommend():
    user_input = request.form.get('user_input')
    product_names = list(X.index)

    #model 1:
    index = product_names.index(user_input)
    similar_items= sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)
    
    data = []
    for i in similar_items[0:8]:
        item = [] 
        temp_df = ratings[ratings['product_id']==X.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('product_id')['product_id'].values))
        item.extend(list(temp_df.drop_duplicates('product_id')['image_url'].values))
        item.extend(list(temp_df.drop_duplicates('product_id')['price'].values))
        
        data.append(item)

        # print(data)

    #model 2
    # correlation_product_ID = sorted(enumerate(correlation_matrix[index]) ,key=lambda x:x[1], reverse = True)
    # mean = np.mean(correlation_product_ID)
    # data1 = []
    # for i in correlation_product_ID:
    #     item = [] 
    #     temp_df = ratings[ratings['product_id']==X.index[i[0]]]
    # #     print(temp_df)
    #     item.extend(list(temp_df.drop_duplicates('product_id')['product_id'].values))
    #     item.extend(list(temp_df.drop_duplicates('product_id')['image_url'].values))
    #     item.extend(list(temp_df.drop_duplicates('product_id')['price'].values))
    #     data1.append(item)
    # data1[0:10]

    # final_data = [value for value in data if value in data1] 

    return render_template('recommend.html',data=data)


#***************************************************************************************************************
# firebase authentication

        

if __name__ == '__main__':
    app.run(debug=True)