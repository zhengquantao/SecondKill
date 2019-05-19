from django.test import TestCase

# Create your tests here.
mstr = "[\"1838\", \"13735\", \"8285\", \"35386\"]"
from ast import literal_eval
mlist = literal_eval(mstr)
print(type(mlist))
print(mlist)