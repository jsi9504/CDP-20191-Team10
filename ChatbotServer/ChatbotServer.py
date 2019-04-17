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
orch = Orchestrator('jsi9504', 'admin', 'qlalfqjsgh!1')
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
    if action == 'flight.cityInfo':
        param = req.get('queryResult').get('parameters')
        start = param["source"][0]
        finish = param["destination"][0]
        flightData.set_location(start, finish)
        result["fulfillmentText"] = start + "에서 " + finish + "으로 가시는군요! \n출국날짜와 귀국날짜를 알려주세요"

    # --------------------------------------
    # 시간정보 처리
    # --------------------------------------
    if action == 'flight.dateInfo':
        param = req.get('queryResult').get('parameters')
        startDate = param["startDate"]
        endDate = param["endDate"]
        flightData.set_date(startDate, endDate)

        location = flightData.get_location()
        date1, date2 = flightData.get_date()
        startInfo = build_json_searching(location, date1, date2)
        response = orch.request('post', orch.startJobs, body=startInfo)
        print(response)
        ID = response["value"][0]["Id"]

        result["fulfillmentText"] = '항공권 조회중입니다. 잠시만 기다려주세요'

    # --------------------------------------
    # 항공권 목록
    # --------------------------------------
    if action == 'flight.searching':
        response = orch.request('get', orch.Jobs + '(%s)' % ID)
        if response['State'] == 'Pending' or response['State'] == 'Running':
            result["fulfillmentText"] = '아직 조회 중입니다. 조금만 더 기다려 주시겠어요?'

        if response['State'] == 'Successful':
            response = json.loads(response["OutputArguments"])

            departure_data = response["Departure_Data"]
            arrival_data = response["Arrival_Data"]
            location = flightData.get_location()
            result_string = location[0] + '->' + location[1] + '\n\r'

            for i in range(len(departure_data)):
                result_string = result_string + str(i) + ':' + departure_data[i] + '\n\r'
            result_string = result_string + location[1] + '->' + location[0] + '\n\r'
            for i in range(len(arrival_data)):
                result_string = result_string + str(i) + ':' + arrival_data[i] + '\n\r'

            result["fulfillmentText"] = result_string + '\n\r원하시는 항공권의 번호를 적어주세요'

    # --------------------------------------
    # 예약 필수정보
    # --------------------------------------
    if action == 'flight.reservation1':
        param = req.get('queryResult').get('parameters')
        depart = param["depart"]
        arrival = param["arrival"]
        flightData.set_flight(depart, arrival)

        result["fulfillmentText"] = '항공권 예매를 위한 필수정보가 필요합니다.\n\r이름, 성별을 입력해 주세요'

    if action == 'flight.name_sex':
        param = req.get('queryResult').get('parameters')
        flightData.set_userInfo(firstName=param["firstName"], lastName=param["lastName"], sex=param['sex'])

        result["fulfillmentText"] = 'email을 정확하게 입력해 주세요'

    if action == 'flight.email':
        param = req.get('queryResult').get('parameters')
        flightData.set_email(param["email"])

        result["fulfillmentText"] = '휴대전화 번호를 입력해 주세요'

    if action == 'flight.phnum':
        param = req.get('queryResult').get('parameters')
        flightData.set_phnum(param["phnum"])

        result["fulfillmentText"] = '항공권 확인용 비밀번호를 입력해 주세요'

    if action == 'flight.pwd':
        param = req.get('queryResult').get('parameters')
        flightData.set_phnum(param["pwd"])
        location = flightData.get_location()
        date1, date2 = flightData.get_date()
        userInfo = flightData.get_userInfo()
        flight = flightData.get_flight()

        startInfo = build_json_reservation(location, date1, date2, userInfo, flight)
        orch.request('post', orch.startJobs, body=startInfo)

        result["fulfillmentText"] = '예약 정보가 이메일로 발송됩니다.'


    # jsonify the result dictionary
    # this will make the response mime type th application/json
    result = jsonify(result)

    # return a result json
    return make_response(result)


# --------------------------------------
# searching json data 생성
# --------------------------------------
def build_json_searching(location, date1, date2):
    inputArgs = {
        "start": location[0],
        "finish": location[1],
        "y1": date1[0],
        "m1": date1[1],
        "d1": date1[2],
        "y2": date2[0],
        "m2": date2[1],
        "d2": date2[2],
    }
    startInfo = {
        'startInfo': {
            "ReleaseKey": "63a59045-374f-48d2-891d-4e3005780e50",
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
# reservation json data 생성
# --------------------------------------
def build_json_reservation(location, date1, date2, userInfo, flight):
    inputArgs = {
        "start": location[0],
        "finish": location[1],
        "y1": date1[0],
        "m1": date1[1],
        "d1": date1[2],
        "y2": date2[0],
        "m2": date2[1],
        "d2": date2[2],
        "depart_time": flight[0],
        "arrival_time": flight[1],
        "lastName": userInfo[0],
        "firstName": userInfo[1],
        "sex": userInfo[2],
        "email": userInfo[3],
        "phnum": userInfo[4],
        "pwd": userInfo[5]
    }
    startInfo = {
        'startInfo': {
            "ReleaseKey": "74a23540-f9d9-409a-95c0-ced62676442c",
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
