from datetime import date, timedelta, datetime


def weekdayDatesInAYear(year, day):
    d = date(year, 1, 1)
    d += timedelta(days = (day - d.weekday() if d.weekday() <= day else 7 + day - d.weekday()))
    while d.year == year:
        yield d
    d += timedelta(days=7)

def get_all_sundays():
    dt = [d for d in weekdayDatesInAYear(datetime.now().year, 6)]  # For getting sunday dates
    return dt