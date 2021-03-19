import unittest
from COM2021.MyDatabase import Database
import time


class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = Database()
        cls.data = {'node_ip': '1.2.3.4', 't_stamp': time.time(),
                    'util': {'cpu': 10, 'mem': 20, 'net': 30, 'sto': 40, 'bat': 50}}

    def test_add(self):
        self.assertEqual(self.db.add_data(self.data), True)

    def test_fetch(self):
        data = self.db.fetch_data('1.2.3.4')
        self.assertEqual(data[0].cpu, self.data['util']['cpu'])


if __name__ == '__main__':
    unittest.main()
