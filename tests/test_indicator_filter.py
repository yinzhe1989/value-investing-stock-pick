import unittest
import filte.indicator_filter as indicator_filter


class TestIndicatorFilter(unittest.TestCase):
    def test_make_previous_quarter(self):
        this_quarter = '20190331'
        pre_quarter = indicator_filter.make_previous_quarter(
            this_quarter)
        self.assertEqual(pre_quarter, '20181231')

        this_quarter = '20190630'
        pre_quarter = indicator_filter.make_previous_quarter(
            this_quarter)
        self.assertEqual(pre_quarter, '20190331')

        this_quarter = '20190930'
        pre_quarter = indicator_filter.make_previous_quarter(
            this_quarter)
        self.assertEqual(pre_quarter, '20190630')

        this_quarter = '20191231'
        pre_quarter = indicator_filter.make_previous_quarter(
            this_quarter)
        self.assertEqual(pre_quarter, '20190930')

        this_quarter = '20190531'
        with self.assertRaises(AssertionError):
            indicator_filter.make_previous_quarter(this_quarter)

    def test_make_last_eight_quarter(self):
        real_quarters = [
            '20171231',
            '20180331',
            '20180630',
            '20180930',
            '20181231',
            '20190331',
            '20190630',
            '20190930'
        ]
        last_eight_quarter = indicator_filter.make_last_eight_quarter()
        for i, quarter in enumerate(last_eight_quarter):
            self.assertEqual(real_quarters[i], quarter)

    def test_make_last_five_year(self):
        real_years = [
            '20141231',
            '20151231',
            '20161231',
            '20171231',
            '20181231'
        ]
        last_five_year = indicator_filter.make_last_five_year()
        for i, year in enumerate(last_five_year):
            self.assertEqual(real_years[i], year)
