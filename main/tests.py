from django.test import TestCase
import unittest
# Create your tests here.
import time
from main.templatetags.inclusion_tags import *
from main.models import *
from main.views import *


def time_it(function):
    t0= time.clock()
    print("Hello")
    t1 = time.clock() - t0
    print("Time elapsed: ", t1)

class calc_testing_time(unittest.TestCase):
    desde='2010-03-04'
    hasta='2024-07-24'
    actualtype='Pan_normado'

    def setUp(self):
        desde='2020-10-16'
        hasta='2024-10-31'
        actualtype='Pan_normado'

    def test_mov_materias_primas(self):
        t0= time.clock()
        make_mov_materias_primas(self.desde, self.hasta)
        t1 = time.clock() - t0
        print("Time elapsed mov_materias_primas: ", t1)