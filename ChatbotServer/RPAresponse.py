#-*- coding:utf-8 -*-
import time, json, requests
from threading import Thread
from orchestrator import Orchestrator

# ********************************
# Line Notify를 사용해 RPA수행결과를 전송.
# ********************************
class RPAresponse():
    orch = None
    q = None
    thrd = None
    def __init__(self, orch : Orchestrator):
        self.orch = orch
        self.q = []  #큐에는 대화 intent, sessionID, orchestrator jobID 가 tuple로 저장됨.
        self.thrd = None

    def worker(self):
        while self.q:
            intent, sessionID, jobID = self.q.pop(0)
            timeout = 0
            response = self.orch.request('get', self.orch.Jobs + '(%s)' % jobID)
            while (response['State'] == 'Pending' or response['State'] == 'Running') and timeout < 5:
                response = self.orch.request('get', self.orch.Jobs + '(%s)' % jobID)
                time.sleep(1)
                timeout = timeout + 1

            if response['State'] == 'Successful':
                if 'KoreanAir' in intent:
                    self.send_notify_message(intent, 'iIjdgCijlxF1LHtymrTjPOUzK1Wy5fXycDN3R1Vq9Lb', response)
                elif 'street11' in intent:
                    self.send_notify_message(intent, 'YmgRx8faPRdTcolTnRm3NcLYCW5gR2bxXPODM3n3zGw', response)
            elif response['State'] == 'Faulted':
                if 'KoreanAir' in intent:
                    self.send_notify_message('fail', 'iIjdgCijlxF1LHtymrTjPOUzK1Wy5fXycDN3R1Vq9Lb', response)
                elif 'street11' in intent:
                    self.send_notify_message(intent, 'YmgRx8faPRdTcolTnRm3NcLYCW5gR2bxXPODM3n3zGw', response)
            else:
                self.q.append((intent, sessionID, jobID))

    def pushQ(self, intent, sessionID, jobID):
        self.q.append((intent, sessionID, jobID))
        print(self.q)
        if self.q:
            self.thrd = Thread(target=self.worker(), daemon=True)
            self.thrd.start()

    def send_notify_message(self, intent, token, datas):
        response = None

        if intent == 'fail':
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': 'Bearer ' + token
            }

            response = requests.request(method='POST',
                                        url='https://notify-api.line.me/api/notify',
                                        data='실패했습니다',
                                        header=headers
                                        )

        if intent == 'KoreanAirSearch':
            input = json.loads(datas["InputArguments"])
            output = json.loads(datas["OutputArguments"])
            departure_data = output["Departure_Data"]
            arrival_data = output["Arrival_Data"]
            location = [input['start'], input['finish']]
            result_string = location[0] + '->' + location[1] + '\n\r'

            for i in range(len(departure_data)):
                result_string = result_string + str(i) + ':' + departure_data[i] + '\n\r'
            result_string = {'message': result_string}
            response = requests.request(method='POST',
                                        url='https://notify-api.line.me/api/notify',
                                        data=result_string,
                                        headers=headers
                                        )
            result_string = location[1] + '->' + location[0] + '\n\r'
            for i in range(len(arrival_data)):
                result_string = result_string + str(i) + ':' + arrival_data[i] + '\n\r'
            result_string = {'message': result_string}
            response = requests.request(method='POST',
                                        url='https://notify-api.line.me/api/notify',
                                        data=result_string,
                                        headers=headers
                                        )
            response = requests.request(method='POST',
                                        url='https://notify-api.line.me/api/notify',
                                        data={'message': '출국편과 귀국편 항공권 번호를 입력해 주세요'},
                                        headers=headers
                                        )
        elif intent == 'street11_searching':
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': 'Bearer ' + token
            }

            output = json.loads(datas["OutputArguments"])
            product_data = output["Product_option"]
            product_image = output["item_url"]

            print(product_data)
            string = '\n'
            for i in range(len(product_data)):
                string = string + str(i) + product_data[i].replace('\r\n', ' ') + '\n'

            result_string = {
                'message': string,
                'imageThumbnail': product_image,
                'imageFullsize': product_image
            }
            response = requests.request(method='POST',
                                        url='https://notify-api.line.me/api/notify',
                                        data=result_string,
                                        headers=headers
                                        )
        else:
            None # 추가로 기능이 확장될 경우 사용~

        print(response)