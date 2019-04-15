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

    def set_location(self, start, finish):
        self.start = start
        self.finish = finish

    def set_date(self, startDate, endDate):
        self.y1 = startDate[0:4]
        self.m1 = startDate[5:7]
        self.d1 = startDate[8:10]

        self.y2 = endDate[0:4]
        self.m2 = endDate[5:7]
        self.d2 = endDate[8:10]

    def get_location(self):
        return self.start, self.finish

    def get_date(self):
        return [self.y1, self.m1, self.d1], [self.y2, self.m2, self.d2]