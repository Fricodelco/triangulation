import unittest
from triangulation.localization import Localizer
from math import pi, sin, cos


class TestLocalizer(unittest.TestCase):
    def test_values_localization(self):
        localizer = Localizer()
        with self.assertRaises(ValueError):
            localizer.find_camera(1,2,3,4,5,6,-1,-1, 0)
        with self.assertRaises(ValueError):
            localizer.find_camera(1,2,3,4,5,6, 0, 0, 0)
    
    def test_localization(self):
        localizer = Localizer()
        x, y, alpha = localizer.find_camera(cos(2*pi/3), sin(2*pi/3), 0, 1, cos(pi/3), sin(pi/3), pi/6, pi/6, pi/6)
        self.assertAlmostEqual(x, 0)
        self.assertAlmostEqual(y, 0)
        self.assertAlmostEqual(alpha, pi/2)