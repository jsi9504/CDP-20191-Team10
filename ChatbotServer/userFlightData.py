# --------------------------------------
# 항공권 예매를 위한 필수 정보를 저장
# --------------------------------------
class FlightData:
    def __init__(self):
        self.start = None
        self.finish = None
        self.y1 = None
        self.y2 = None
        self.m1 = None
        self.m2 = None
        self.d1 = None
        self.d2 = None
        self.depart_time = None
        self.arrival_time = None
        self.lastName = None
        self.firstName = None
        self.sex = None
        self.phnum = None
        self.email = None
        self.pwd = None


    def set_location(self, start, finish):
        self.start = start
        self.finish = finish

    def set_date(self, startDate, endDate):
        self.y1 = str(int(startDate[0:4]))
        self.m1 = str(int(startDate[5:7]))
        self.d1 = str(int(startDate[8:10]))

        self.y2 = str(int(endDate[0:4]))
        self.m2 = str(int(endDate[5:7]))
        self.d2 = str(int(endDate[8:10]))

    def set_flight(self, depart, arrival):
        self.depart_time = depart
        self.arrival_time = arrival

    def set_userInfo(self, lastName, firstName, sex):
        self.lastName = lastName
        self.firstName = firstName
        self.sex = sex

    def set_email(self, email):
        self.email = email

    def set_phnum(self, phnum):
        self.phnum = phnum

    def set_pwd(self, pwd):
        self.pwd = pwd

    def get_location(self):
        return self.start, self.finish

    def get_date(self):
        return [self.y1, self.m1, self.d1], [self.y2, self.m2, self.d2]

    def get_flight(self):
        return self.depart_time, self.arrival_time

    def get_userInfo(self):
        return self.lastName, self.firstName, self.sex, self.email, self.phnum, self.pwd