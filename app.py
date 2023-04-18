from flask import Flask,render_template,request
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl','rb'))
X = pickle.load(open('X.pkl','rb'))
ratings = pickle.load(open('ratings1.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))
correlation_matrix = pickle.load(open('correlation_matrix.pkl','rb'))
# print(similarity_scores.shape)
app = Flask(__name__)

@app.route('/')
def index():
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
if __name__ == '__main__':
    app.run(debug=True)