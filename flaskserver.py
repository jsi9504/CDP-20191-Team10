# import flask dependencies
import json
from flask import Flask, jsonify
from flask import request
from flask import make_response

# initialize the flask app
app = Flask(__name__)


# user flight data
source = ''
destination = ''
startDate = ''
endDate = ''


# function for responses
def results():
    # build a request object
    req = request.get_json(force=True)
    action = req.get('queryResult').get('action')
    global source, destination, startDate, endDate
    result = {}

    if action == 'flight':
        # action statement here
        # fulfillment text is the default response that is returned to the dialogflow request
        result["fulfillmentText"] = "출발지와 목적지를 알려주세요"

    if action == 'flight.flight-custom' :
        param = req.get('queryResult').get('parameters')
        source = param["source"]
        destination = param["destination"]
        result["fulfillmentText"] = source + "에서 " + destination + "으로 가시는군요! \n출발날짜와 도착날짜를 알려주세요"

    if action == 'flight.flight-custom.flight-city-custom' :
        param = req.get('queryResult').get('parameters')
        startDate = param["startDate"]
        endDate = param["endDate"][0]
        result["fulfillmentText"] = source + "에서 " + destination + "으로 " + startDate + " ~ " + endDate + "비행기 맞으신가요?"



    # jsonify the result dictionary
    # this will make the response mime type th application/json
    result = jsonify(result)

    # return a result json
    return make_response(result)


# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    return results()


# run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='9090')
