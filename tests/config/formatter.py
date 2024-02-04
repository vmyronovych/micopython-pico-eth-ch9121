import unittest
from pico_ch9121.config.formatter import ConfigFormatter

class ConfigFormatterTests(unittest.TestCase):
    def test_ip(self):
        fmt = ConfigFormatter()
        actualIp = fmt.ip(b'\xc0\xa8\x01\xc8')
        self.assertEqual('192.168.1.200', actualIp)