from flask import Flask, render_template, request
from model import load_data, train_model, predict_sentiment

app = Flask(__name__)

# Load data and train model
data = load_data('labeled_tweets.csv')
model, vectorizer = train_model(data)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    user_input = request.form['user_input']
    prediction = predict_sentiment(model, vectorizer, user_input)
    return render_template('result.html', prediction=prediction, user_input=user_input)

if __name__ == '__main__':
    app.run(debug=True)
