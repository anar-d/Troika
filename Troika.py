from datetime import datetime


class CardTroika(object):
    def __init__(self, AmountOfMoney, DateOfActivation={'day': 1, 'month': 1,'year': 2010, 'hour': 8, 'minute': 0, 'second': 0}, Replenishmenthistory={}, PaymentHistory={}, ActivityLog = []):
        self.AmountOfMoney = AmountOfMoney
        self.DateOfActivation = DateOfActivation
        self.ReplenishmentHistory = Replenishmenthistory # Словарь, в котором значениями являются списки с int значениями вида [день, месяц, год, час, минута, секунда, начисление]
        self.PaymentHistory = PaymentHistory # Словарь, в котором значениями являются списки с int значениями вида [день, месяц, год, час, минута, секунда, счисление, вид транспорта]
        self.ActivityLog = ActivityLog
        self.CountForDictReplenishment = 0
        self.CountForDictPayment = 0

    def FarePayment(self, transport):
        day = datetime.now().day
        month = datetime.now().month
        year = datetime.now().year
        hour = datetime.now().hour
        minute = datetime.now().minute
        second = datetime.now().second

        if len(self.PaymentHistory) > 0:
            if (self.PaymentHistory[self.CountForDictPayment][0] == day) and (self.PaymentHistory[self.CountForDictPayment][1] == month) and (self.PaymentHistory[self.CountForDictPayment][2] == year):
                conditionToday = True

            if (conditionToday == True) and (self.PaymentHistory[self.CountForDictPayment][3] == hour) and (minute * 60 + second - 300 >= self.PaymentHistory[self.CountForDictPayment][4] * 60 + self.PaymentHistory[self.CountForDictPayment][5]):
                if transport == 'Metro':
                    self.AmountOfMoney -= 27
                    self.PaymentHistory[self.CountForDictPayment] = [day, month, year, hour, minute, second, 27, 'Metro']
                elif transport == 'Ground':
                    if self.PaymentHistory[self.CountForDictPayment][3] * 3600 + self.PaymentHistory[self.CountForDictPayment][4] * 60 + self.PaymentHistory[self.CountForDictPayment][5] - hour * 3600 - minute * 60 - second > 3600:
                        self.AmountOfMoney -= 27
                        self.PaymentHistory[self.CountForDictPayment] = [day, month, year, hour, minute, second, 27, 'Ground']
                    else:
                        self.AmountOfMoney -= 15
                        self.PaymentHistory[self.CountForDictPayment] = [day, month, year, hour, minute, second, 27, 'Ground']
            else:
                print(f'У Вас задержка {(self.PaymentHistory[self.CountForDictPayment][4] * 60 + self.PaymentHistory[self.CountForDictPayment][5] + 300 - minute * 60 - second) // 60} мин. и {(self.PaymentHistory[self.CountForDictPayment][4] * 60 + self.PaymentHistory[self.CountForDictPayment][5] + 300 - minute * 60 - second) % 60} сек.')
            self.CountForDictPayment += 1
        else:
            if transport == 'Metro':
                self.AmountOfMoney -= 27
                self.PaymentHistory[0] = [day, month, year, hour, minute, second, 27, 'Metro']
            elif transport == 'Ground':
                if self.DateOfActivation['hour'] * 3600 + self.DateOfActivation['minute'] * 60 + self.DateOfActivation['second'] - hour * 3600 - minute * 60 - second > 3600:
                    self.AmountOfMoney -= 27
                    self.PaymentHistory[0] = [day, month, year, hour, minute, second, 27, 'Ground']
                else:
                    self.AmountOfMoney -= 15
                    self.PaymentHistory[0] = [day, month, year, hour, minute, second, 27, 'Ground']

    def AccountReplenishment(self, number):
        day = datetime.now().day
        month = datetime.now().month
        year = datetime.now().year
        hour = datetime.now().hour
        minute = datetime.now().minute
        second = datetime.now().second

        self.AmountOfMoney += number
        self.ReplenishmentHistory[self.CountForDictReplenishment] = [day, month, year, hour, minute, second, number]
        self.CountForDictReplenishment += 1

    def Activity(self):
        self.ActivityLog.append(datetime.now())

    def __str__(self):
        self.Activity()
        return f'Остаток на счете: {self.AmountOfMoney} руб. \nДействительно до {list(self.DateOfActivation.values())[0]}.{list(self.DateOfActivation.values())[1]}.{list(self.DateOfActivation.values())[2] + 5}'


class TurnstileOfMetro(CardTroika):

    def __init__(self, AmountOfMoney, DateOfActivation={'day': 1, 'month': 1,'year': 2010, 'hour': 8, 'minute': 0, 'second': 0}, Replenishmenthistory={}, PaymentHistory={}):
        super().__init__(AmountOfMoney, DateOfActivation, Replenishmenthistory, PaymentHistory)
        self.condition = True

    def Condition(self):
        self.condition = True if self.AmountOfMoney >= 15 else False

    def __str__(self):
        self.Condition()
        if self.condition:
            return f'Проход разрешен. \nОстаток на счете: {self.AmountOfMoney} руб. \nДействительно до {list(self.DateOfActivation.values())[0]}.{list(self.DateOfActivation.values())[1]}.{list(self.DateOfActivation.values())[2] + 5}'
        else:
            return f'Проход запрещен. \nОстаток на счете: {self.AmountOfMoney} руб. \nДействительно до {list(self.DateOfActivation.values())[0]}.{list(self.DateOfActivation.values())[1]}.{list(self.DateOfActivation.values())[2] + 5}'


class TroikaWithPhone(CardTroika):

    def __init__(self, AmountOfMoney, PhoneNumber, transport, DateOfActivation={'day': 1, 'month': 1,'year': 2010, 'hour': 8, 'minute': 0, 'second': 0}, Replenishmenthistory={}, PaymentHistory={}, ActivityLog = []):
        super().__init__(AmountOfMoney, DateOfActivation, Replenishmenthistory, PaymentHistory)
        self.PhoneNumber = PhoneNumber
        self.transport = transport
        self.ActivityLog = ActivityLog

    def Activity(self):
        self.ActivityLog.append(datetime.now())

    def __str__(self):
        self.Activity()
        COT = CardTroika(self.AmountOfMoney)
        COT.FarePayment(self.transport)
        return str(COT)[:27] + '\nСрок действия неограничен.' + f'\nНомер телефона {self.PhoneNumber}'


class TerminalOfController(object):

    def __init__(self, *cards):
        self.cards = cards

    def get(self):
        for i in self.cards:
            print(f'{i.ActivityLog[-1].hour}:{i.ActivityLog[-1].minute}:{i.ActivityLog[-1].second}')


# COT = CardTroika(1000)
# COT.FarePayment('Ground')
# COT.FarePayment('Ground')
# print(COT.AmountOfMoney)

if __name__ == '__main__':
    TOM1 = TurnstileOfMetro(26)
    # TOM1.FarePayment('Ground')
    # print(TOM1)
    TOM1.Activity()
    TOM1

    TOM2 = TurnstileOfMetro(29)
    # TOM2.FarePayment('Ground')
    # print(TOM2)
    TOM2.Activity()

    # TWP = TroikaWithPhone(500, '8-909-970-05-32', 'Metro')
    # print(TWP)

    TOC = TerminalOfController(TOM1, TOM2)
    TOC.get()