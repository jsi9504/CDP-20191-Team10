#-*- coding:utf-8 -*-
import json, buildjson, RPAresponse

from flask import Flask, jsonify, request, make_response

from orchestrator import Orchestrator
from userFlightData import FlightData

# --------------------------------------
# flask app 초기화
# --------------------------------------
app = Flask(__name__)

# --------------------------------------
# 사용자 항공권예매 정보
# --------------------------------------
flightData = FlightData()

# --------------------------------------
# Orchestrator, RPAresponse 생성
# --------------------------------------
orch = Orchestrator('jsi9504', 'tnsdlr10000@gmail.com', 'qlalfqjsgh!1')
RPAres = RPAresponse.RPAresponse(orch)

# --------------------------------------
# 응답처리
# --------------------------------------
def results():
    req = request.get_json(force=True)
    action = req.get('queryResult').get('action')
    if 'flight' in action:
        return koreanAir()

    elif 'street11' in action:
        return purchase_11st()

def koreanAir():
    req = request.get_json(force=True)
    action = req.get('queryResult').get('action')
    global flightData, orch, RPAres
    result = {}

    print(req)

    # --------------------------------------
    # 항공권 조회
    # --------------------------------------
    if action == 'flight.dateInfo':
        sessionID = req.get('session')
        param = req.get('queryResult').get('outputContexts')
        for i in range(len(param)):
            if param[i]['name'] == sessionID + 'contexts/flight-city-followup':
                param = param[i]

        startInfo = buildjson.KoreanAir_searching(param[0]['parameters'])
        response = orch.request('post', orch.startJobs, body=startInfo)
        #print(response)
        ID = response["value"][0]["Id"]

        RPAres.pushQ('KoreanAirSearch', sessionID, ID)

        result["fulfillmentText"] = '항공권 조회중입니다. 잠시만 기다려주세요'

    # --------------------------------------
    # 항공권 예매
    # --------------------------------------
    if action == 'flight.phnum':
        sessionID = req.get('session')
        param = req.get('queryResult').get('outputContexts')
        for i in range(len(param)):
            if param[i]['name'] == sessionID + 'contexts/flight-city-date-followup':
                param = param[i]

        print(param)
        startInfo = buildjson.KoreanAir_reservation((param[0])['parameters'])
        response = orch.request('post', orch.startJobs, body=startInfo)
        print(response)

        result["fulfillmentText"] = '항공권이 이메일로 발송됩니다.'


    # jsonify the result dictionary
    # this will make the response mime type th application/json
    result = jsonify(result)

    # return a result json
    return make_response(result)

def purchase_11st():
    req = request.get_json(force=True)
    action = req.get('queryResult').get('action')
    global flightData, orch, RPAres
    result = {}

    print(req)

    if action == 'street11.price':
        sessionID = req.get('session')
        param = req.get('queryResult').get('outputContexts')
        for i in range(len(param)):
            if param[i]['name'] == sessionID + 'contexts/buy_item-followup':
                param = param[i]

        print(param)
        startInfo = buildjson.street11_searching((param[0])['parameters'])
        response = orch.request('post', orch.startJobs, body=startInfo)
        print(response)
        ID = response["value"][0]["Id"]

        RPAres.pushQ('street11_searching', sessionID, ID)

        result["fulfillmentText"] = '지나갑니당~'

    if action == 'street11.email':
        sessionID = req.get('session')
        param = req.get('queryResult').get('outputContexts')
        for i in range(len(param)):
            if param[i]['name'] == sessionID + 'contexts/buy_item-followup':
                param = param[i]

        print(param)
        startInfo = buildjson.street11_purchase((param[0])['parameters'])
        response = orch.request('post', orch.startJobs, body=startInfo)
        print(response)
        result["fulfillmentText"] = ''


    result = jsonify(result)
    return make_response(result)
# --------------------------------------
# dialogflow webhook
# --------------------------------------
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    return results()


# --------------------------------------
# 메인함수
# --------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
