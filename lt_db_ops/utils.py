import time
import datetime


def get_current_date_string()->str:
    t = time.localtime(time.time())

    d_t = datetime.datetime(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)
    return d_t.__str__()

