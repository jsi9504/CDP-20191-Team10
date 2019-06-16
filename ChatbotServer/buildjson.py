import json

# --------------------------------------
# searching json data 생성
# --------------------------------------
def KoreanAir_searching(param):
    inputArgs = {
        "start": param['source'][0],
        "finish": param['destination'][0],
        "y1": str(int(param['startDate'][0:4])),
        "m1": str(int(param['startDate'][5:7])),
        "d1": str(int(param['startDate'][8:10])),
        "y2": str(int(param['endDate'][0:4])),
        "m2": str(int(param['endDate'][5:7])),
        "d2": str(int(param['endDate'][8:10])),
    }
    print(inputArgs)
    startInfo = {
        'startInfo': {
            "ReleaseKey": "f1543e67-32ce-48d2-b529-6fb6f4af1fc3",
            "Strategy": "Specific",
            "RobotIds": [
                138109
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
def KoreanAir_reservation(param):
    inputArgs = {
        "start": param['source'],
        "finish": param['destination'],
        "y1": str(int(param['startDate'][0:4])),
        "m1": str(int(param['startDate'][5:7])),
        "d1": str(int(param['startDate'][8:10])),
        "y2": str(int(param['endDate'][0:4])),
        "m2": str(int(param['endDate'][5:7])),
        "d2": str(int(param['endDate'][8:10])),
        "depart_time": param['depart'],
        "arrival_time": param['arrive'],
        "lastName": param['lastName'],
        "firstName": param['firstName'],
        "sex": param['sex'],
        "email": param['email'],
        "phnum": param['phnum'],
        "pwd": param['pwd']
    }
    startInfo = {
        'startInfo': {
            "ReleaseKey": "cc7741fd-7a39-4dde-84ac-245dcc445a55",
            "Strategy": "Specific",
            "RobotIds": [
                138109
            ],
            "NoOfRobots": 0,
            "Source": "Manual",
            "InputArguments": json.dumps(inputArgs)
        }
    }

    return json.dumps(startInfo)

def street11_searching(param):
    inputArgs = {
        'Product': param['Product'],
        'max_price': str(int(param['max_price'])),
        'ID': 'qkrrjsdn5000',
        'password': 'testaccount1',
        'Choose_option': 0,
        'Choose_option2': 0,
        'name': '',
        'ph1': '',
        'ph2': '',
        'address': '',
        'address_detail': '',
        'email': ''
    }
    startInfo = {
        'startInfo': {
            "ReleaseKey": "9dffd9ef-9d47-49e7-b8e2-79c1880c0553",
            "Strategy": "Specific",
            "RobotIds": [
                138109
            ],
            "NoOfRobots": 0,
            "Source": "Manual",
            "InputArguments": json.dumps(inputArgs)
        }
    }

    return json.dumps(startInfo)

def street11_purchase(param):
    inputArgs = {
        'Product': param['Product'],
        'max_price': str(int(param['max_price'])),
        'ID': 'qkrrjsdn5000',
        'password': 'testaccount1',
        'Choose_option': param['option'],
        'Choose_option2': 0,
        'name': param['name'],
        'ph1': param['phnum1'],
        'ph2': param['phnum2'],
        'address': param['address'],
        'address_detail': param['address_detail'],
        'email': param['email']
    }
    startInfo = {
        'startInfo': {
            "ReleaseKey": "a298ecae-537d-4d05-ac0e-40a776bb5413",
            "Strategy": "Specific",
            "RobotIds": [
                138109
            ],
            "NoOfRobots": 0,
            "Source": "Manual",
            "InputArguments": json.dumps(inputArgs)
        }
    }

    return json.dumps(startInfo)