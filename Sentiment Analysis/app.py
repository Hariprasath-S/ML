from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)
__model = None
__vectoriser = None

@app.route('/')
def hello():
    return ("Hello, World!")


@app.route('/predict', methods=['POST'])
def predict_sentiment():
    text = str(request.form['input_text'])
    #text = 'hate you'
    response = jsonify({
        'sentiment': str(get_sentiment(text))
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


def load_model():
    global __model
    global __vectoriser
    if __model is None:
        with open('sentiment.pickle', 'rb') as f:
            __model = pickle.load(f)
    print("Model loaded")
    if __vectoriser is None:
        with open('vectorisor.pickle', 'rb') as w:
            __vectoriser = pickle.load(w)
    print("Vectorisor loaded")


def get_sentiment(text2):
    text = [text2]
    return __model.predict(__vectoriser.transform(text))[0]


if __name__ == "__main__":
    load_model()
    app.run()
