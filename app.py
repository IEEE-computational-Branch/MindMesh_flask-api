from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import pickle

model = pickle.load(open("Model/finalized_model.sav", 'rb'))

NUM = pickle.load(open("Model/Numeric_model.sav", 'rb'))

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def prediction(Value):
    y_pred = model.predict([Value])
    Predicted_error = y_pred.tolist()[0]
    return int(Predicted_error)

@app.route('/',methods=['GET'])
@cross_origin()
def index():
    return "Flask is up and running"    

@app.route('/api', methods=['POST'])
@cross_origin()
def predict():
    region = {'southwest': 3, 'southeast': 2, 'northwest': 1, 'northeast': 0}
    smoker = {'Yes': 1, 'No': 0}
    Gen = {'Male': 1, 'Female': 0}
    data = request.get_json()
    Age = data['age']
    Gender = data['gender']
    BMI = data['bmi']
    Child = data['children']
    Smoker = data['smoker']
    Region = data['region']
    bmi = NUM.transform([[BMI]])
    print(type(Age), type(Gender), type(BMI), type(Child), type(Smoker), type(Region))
    Value = [Gen[Gender], smoker[Smoker], region[Region], Age, float(bmi[0]), Child ]
    try:
        cost = prediction(Value)
        return str(cost)
    except Exception as e:
        return e         