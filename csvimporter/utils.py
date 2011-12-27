import unicodedata
import re
from StringIO import StringIO
import csv

#try:
#    all_chars = (unichr(i) for i in xrange(0x110000))
#except ValueError:

all_chars = (unichr(i) for i in xrange(0x10000))
control_chars = ''.join(
    c for c in all_chars if unicodedata.category(c) in ['Cc', 'Cf'])

# or equivalently and much more efficiently
#control_chars = ''.join(map(unichr, range(0,32) + range(127,160)))

control_char_re = re.compile('[%s]' % re.escape(control_chars))


def remove_control_chars(s):
    if type(s) is not unicode:
        s = s.decode("utf-8")
    return control_char_re.sub('', s).encode("utf-8")


def prepare_csv(csv_content):
#    csv_content.seek(0)
    csv_content = csv_content.readlines()
    # CVS bugfixes
    csv_content[0] = re.sub('\s*,\s+', ',', csv_content[0])
    csv_content[0] = re.sub('(?=.+),$', '\n', csv_content[0])

    csv_content = "".join(csv_content)
    return StringIO(csv_content)


def create_csv_reader(_file):
    _file = prepare_csv(_file)
    reader = csv.DictReader(_file)
    reader.fieldnames = [remove_control_chars(f) for f in reader.fieldnames]
    return reader
