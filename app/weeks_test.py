import unittest
from app.weeks import ChurchYear
from datetime import date

EASTER_SUNDAY = date(2018, 4, 1)


class TestChurchYear(unittest.TestCase):
    def test_ash_sunday(self):
        church_year = ChurchYear(EASTER_SUNDAY)
        ash_sunday = date(2018, 2, 14)
        self.assertEqual(church_year._ash_wednesday(), ash_sunday)

    def test_first_standard_sunday(self):
        church_year = ChurchYear(EASTER_SUNDAY)
        standard_sunday = date(2018, 1, 7)
        self.assertEqual(church_year._first_standard_sunday(), standard_sunday)

    def test_first_lent_sunday(self):
        church_year = ChurchYear(EASTER_SUNDAY)
        first_lent_sunday = date(2018, 2, 18)
        self.assertEqual(church_year._first_great_lent_sunday(), first_lent_sunday)

    def test_second_first_standard_sunday(self):
        church_year = ChurchYear(EASTER_SUNDAY)
        second_forst_standard_sunday = date(2018, 5, 20)
        self.assertEqual(church_year._second_standard_sunday(), second_forst_standard_sunday)

    def test_first_advent_sunday(self):
        church_year = ChurchYear(EASTER_SUNDAY)
        first_advent_sunday = date(2018, 12, 2)
        self.assertEqual(church_year._first_advent_sunday(), first_advent_sunday)


if __name__ == "__main__":
    unittest.main()