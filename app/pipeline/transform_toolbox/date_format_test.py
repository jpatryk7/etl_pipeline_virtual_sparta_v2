import unittest
import pandas as pd


def date_format_test(date_ser: pd.Series) -> None:
    """
    Small helper function that checks if the given column contains only dates the format: [dd, mm, yyyy].
    :param pd.Series date_ser: pandas' column of lists
    """
    utest = unittest.TestCase()
    utest.assertTrue(all([[isinstance(num, int) for num in ls] for ls in date_ser if not pd.isnull(ls)]))
    utest.assertTrue(all([len(d) == 3 for d in date_ser if not pd.isnull(d)]))
    utest.assertTrue(all([0 < d[0] <= 31 for d in date_ser if not pd.isnull(d)]))
    utest.assertTrue(all([0 < d[1] <= 12 for d in date_ser if not pd.isnull(d)]))
    utest.assertTrue(all([2000 < d[2] < 2022 for d in date_ser if not pd.isnull(d)]))