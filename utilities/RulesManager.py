import datetime
import calendar
import uuid
import math


class Rule(object):

    def __init__(self, device, state, run_time, repeat, guid, rule_time):
        self.device = device
        self.state = state
        self.time = run_time
        self.repeat = repeat
        self.uuid = guid
        self.rule_time = rule_time

    def __cmp__(self, other):
        return cmp(self.time, other.time)

    def restart(self):
        if self.repeat == 0:
            return None

        return Rule.create(self.device, self.rule_time, self.state, self.repeat, self.uuid)

    @staticmethod
    def create(device, rule_time, state, repeat, guid=None):
        if rule_time < 0 or rule_time > 2359:
            raise Exception("Wrong time value: {}".format(rule_time))

        if (not repeat and repeat != 0) or repeat > 255 or repeat < -1:
            raise Exception("Wrong repeat value: {}".format(repeat))

        if repeat == 0:
            return Rule._create_single(device, rule_time, state, guid)

        if repeat >= 128:
            return Rule._create_minutes(device, rule_time, state, guid)

        today = datetime.datetime.utcnow()
        today_weekday = today.weekday()

        hour = rule_time // 100
        minute = rule_time % 100
        rule_date = today.replace(hour=hour, minute=minute)

        flag = 1
        min_diff = 10
        for i in range(7):
            if i > 0:
                flag *= 2

            # get current weekday by testing flag
            day = repeat & flag
            if day == 0:
                continue

            day = i

            # calculate day difference
            diff = day - today_weekday
            # add extra week if needed
            if diff < 0:
                diff += 7
            elif diff == 0:
                if rule_date < today:
                    diff = 7

            if diff < min_diff:
                min_diff = diff

        if min_diff > 0:
            rule_date = rule_date + datetime.timedelta(days=min_diff)

        if not guid:
            guid = uuid.uuid4()

        return Rule(device, int(state), calendar.timegm(rule_date.timetuple()), int(repeat), guid, rule_time)

    @staticmethod
    def _create_single(device, rule_time, state, guid=None):
        today = datetime.datetime.utcnow()

        hour = rule_time // 100
        minute = rule_time % 100
        rule_date = today.replace(hour=hour, minute=minute)

        if rule_date < today:
            rule_date = rule_date + datetime.timedelta(days=1)

        if not guid:
            guid = uuid.uuid4()

        return Rule(device, int(state), calendar.timegm(rule_date.timetuple()), 0, guid, rule_time)

    @staticmethod
    def _create_minutes(device, rule_time, state, guid=None):
        today = datetime.datetime.utcnow()

        minute = rule_time % 10
        diff = minute - today.minute % 10
        if diff < 0:
            diff += 10

        rule_date = today + datetime.timedelta(minutes=diff)

        if not guid:
            guid = uuid.uuid4()

        return Rule(device, int(state), calendar.timegm(rule_date.timetuple()), 0, guid, rule_time)
