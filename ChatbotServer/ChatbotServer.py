import json
import requests

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
# Orchestrator 객체 생성
# --------------------------------------
orch = Orchestrator('')
ID = None # job ID

# --------------------------------------
# 응답처리
# --------------------------------------
def results():
    req = request.get_json(force=True)
    action = req.get('queryResult').get('action')
    global flightData, orch, ID
    result = {}

    # --------------------------------------
    # 항공기 예매 intent
    # --------------------------------------
    if action == 'flight':
        # action statement here
        result["fulfillmentText"] = "출발지와 목적지를 알려주세요"

    # --------------------------------------
    # 출발지, 도착지 정보 처리
    # --------------------------------------
    if action == 'flight.flight-custom':
        param = req.get('queryResult').get('parameters')
        start = param["source"][0]
        finish = param["destination"][0]
        flightData.set_location(start, finish)
        result["fulfillmentText"] = start + "에서 " + finish + "으로 가시는군요! \n출국날짜와 귀국날짜를 알려주세요"

    # --------------------------------------
    # 시간정보 처리
    # --------------------------------------
    if action == 'flight.flight-custom.flight-city-custom':
        param = req.get('queryResult').get('parameters')
        startDate = param["startDate"]
        endDate = param["endDate"][0]
        flightData.set_date(startDate, endDate)

        location = flightData.get_location()
        date1, date2 = flightData.get_date()
        startInfo = build_json_startjobs(location, date1, date2)
        response = orch.request('post', orch.startJobs, body=startInfo)
        print(response)
        ID = response["value"][0]["Id"]

        result["fulfillmentText"] = '항공권 조회중입니다. 잠시만 기다려주세요'

    # --------------------------------------
    # 항공권 목록
    # --------------------------------------
    if action == 'flight.flight-custom.flight-city-custom.flight-city-date-custom':
        response = orch.request('get', orch.Jobs + '(%s)' % ID)
        if response['State'] == 'Pending' or response['State'] == 'Running':
            result["fulfillmentText"] = '아직 조회 중입니다. 조금만 더 기다려 주시겠어요?'

        if response['State'] == 'Successful':
            response = json.loads(response["OutputArguments"])

            departure_data = response["Departure_Data"]
            arrival_data = response["Arrival_Data"]

            result["fulfillmentText"] = '출국편 : ' + str(departure_data) + '귀국편 : ' + str(arrival_data)

    # jsonify the result dictionary
    # this will make the response mime type th application/json
    result = jsonify(result)

    # return a result json
    return make_response(result)


# --------------------------------------
# startjobs 요청을 위한 json data 생성
# --------------------------------------
def build_json_startjobs(location, date1, date2):
    inputArgs = {
        "start": location[0],
        "finish": location[1],
        "y1": date1[0],
        "m1": date1[1],
        "d1": date1[2],
        "y2": date2[0],
        "m2": date2[1],
        "d2": date2[2]
    }
    startInfo = {
        'startInfo': {
            "ReleaseKey": "1c18060d-7df3-4f80-8fe3-9ba0ea141faf",
            "Strategy": "Specific",
            "RobotIds": [
                138009
            ],
            "NoOfRobots": 0,
            "Source": "Manual",
            "InputArguments": json.dumps(inputArgs)
        }
    }

    return json.dumps(startInfo)


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
    app.run(host='0.0.0.0')
