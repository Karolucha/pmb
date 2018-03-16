from datetime import date, timedelta


class ChurchYear:
    WEEKDAY = {
        0: "poniedziałek",
        1: "wtorek",
        2: "środa",
        3: "czwartek",
        4: "piątek",
        5: "sobota",
        6: "niedziela"
    }

    def __init__(self, easter_sunday):
        if not isinstance(easter_sunday, date):
            raise ValueError("easter_sunday not a datetime.date type")
        self.easter_sunday = easter_sunday

    def _first_standard_sunday(self):
        """
       first day of I normal period
       """
        for day in range(7, 14):
            if date(self.easter_sunday.year, 1, day).weekday() == 6:
                return date(self.easter_sunday.year, 1, day)

    def _ash_wednesday(self):
        return self.easter_sunday - timedelta(days=46)

    def _length_of_first_standard_weeks(self):
        """
       returns number length in weeks of first standard week
       """
        return self._calculate_week(self._ash_wednesday(), self._first_standard_sunday())

    def _first_great_lent_sunday(self):
        return self._ash_wednesday() + timedelta(days=4)

    def _second_standard_sunday(self):
        return self.easter_sunday + timedelta(days=49)

    def _first_advent_sunday(self):
        for day in range(18, 25):
            if date(self.easter_sunday.year, 12, day).weekday() == 6:
                return date(self.easter_sunday.year, 12, day) - timedelta(days=21)

    def _calculate_week(self, day, previous_period_sunday, first_standard_length=0):
        for week in range(1, 40):
            if day < previous_period_sunday + timedelta(days=week * 7):
                return week + first_standard_length

    def get_week(self, day):
        """
       params: date
       return Nth week of advent, standard, great lent, easter
       """
        if day < self._first_standard_sunday():
            return ChurchYear.WEEKDAY[day.weekday()], "2 tydzień Bożego Narodzenia"

        if day < self._first_great_lent_sunday():
            week_number = self._calculate_week(day, self._first_standard_sunday())
            return ChurchYear.WEEKDAY[day.weekday()], "{}. Tydzień Zwykły".format(week_number)

        if day < self.easter_sunday:
            week_number = self._calculate_week(day, self._first_great_lent_sunday())
            return ChurchYear.WEEKDAY[day.weekday()], "{}. Tydzień Wielkiego Postu".format(week_number)

        if day < self._second_standard_sunday():
            week_number = self._calculate_week(day, self.easter_sunday)
            return ChurchYear.WEEKDAY[day.weekday()], "{}. Tydzień Wielkanocy".format(week_number)

        if day < self._first_advent_sunday():
            week_number = self._calculate_week(day, self._second_standard_sunday(),
                                               self._length_of_first_standard_weeks())
            return ChurchYear.WEEKDAY[day.weekday()], "{}. Tydzień Zwykły".format(week_number)


if __name__ == "__main__":
    church_year = ChurchYear(date(2018, 4, 1))
    print("Pierwszy tydzień zwykły")
    print(church_year.get_week(date(2018, 1, 7)))
    print("Drugi tydzień zwykły, środa")
    print(church_year.get_week(date(2018, 1, 17)))
    print("Cwarty tydzień wielkiego Postu, Czwartek")
    print(church_year.get_week(date(2018, 3, 15)))
    print("Piąty tydzień Wielkanocy, Czwartek")
    print(church_year.get_week(date(2018, 5, 3)))
    print("34 tydzień Zwykły, Poniedziałek")
    print(church_year.get_week(date(2018, 11, 26)))
