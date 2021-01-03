from flask import Flask, request, jsonify, render_template
import pickle
import json
import numpy as np


__locations = None
__data_columns = None
__model = None

app = Flask(__name__)


@app.route('/')
def home():
    #return render_template('app.html', output=f)
    return render_template('app.html')


@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    global __locations
    global __data_columns
    with open("artifacts/columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]  # first 3 columns are sqft, bath, bhk

    response = jsonify({
        'locations': __locations
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    #return render_template('app.html', output=__status)
    return response


@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    total_sqft = float(request.form['total_sqft'])
    location = request.form['location']
    bhk = int(request.form['bhk'])
    bath = int(request.form['bath'])

    global __model
    if __model is None:
        with open('artifacts/bangalore_home_prices.pickle', 'rb') as f:
            __model = pickle.load(f)


    response = jsonify({
        'estimated_price': get_estimated_price(location, total_sqft, bhk, bath)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

def get_estimated_price(location, sqft, bhk, bath):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    print(x)


    if loc_index >= 0:
        x[loc_index] = 1

    return round(__model.predict([x])[0], 2)


def load_saved_artifacts():
    print("loading saved artifacts...start")
    '''global __data_columns
    global __locations
    global __status

    with open("artifacts/columns.json", "r") as f:
        __status = f
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]  # first 3 columns are sqft, bath, bhk

    global __model
    if __model is None:
        with open('artifacts/bangalore_home_prices.pickle', 'rb') as f:
            __model = pickle.load(f)
    print("loading saved artifacts...done")'''

def get_location_names1():
    return __locations


def get_data_columns():
    return __data_columns


if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    load_saved_artifacts()
    app.run()