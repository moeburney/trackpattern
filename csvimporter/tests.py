from unittest import TestCase
from StringIO import StringIO

from csvimporter.utils import remove_control_chars, prepare_csv

class TestRemoveControlChars(TestCase):
    def test_clean_string(self):
        s = u"qwertyuiop[];'\/.,"
        self.assertEqual(remove_control_chars(s), s)

    def test_bad_string(self):
        bad = '\xef\xbb\xbfDate'.decode("utf-8")
        good = u'Date'
        self.assertEqual(remove_control_chars(bad), good)

    def test_not_unicode(self):
        self.assertRaises(ValueError, remove_control_chars, 'sss')


class TestPrepare(TestCase):
    def test_prepare_csv(self):
        bad_cvs_file = StringIO('\xef\xbb\xbfDate bla , bla bla')
        good_cvs_file = StringIO('Date bla, bla bla')
        self.assertEqual(
            prepare_csv(bad_cvs_file).read(), good_cvs_file.read())
