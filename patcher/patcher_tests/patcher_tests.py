import unittest
from patcher.GDrive import DriveUtil

class TestPatcher(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_upload_to_drive(self):
        gDrive = DriveUtil()
        gDrive.upload_to_drive()
        self.assertEqual(0, 0)


class TestPatcher2(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_upload_to_drive(self):
        gDrive = DriveUtil()
        gDrive.upload_to_drive()
        self.assertEqual(0, 0)

if __name__ == '__main__':
    unittest.main()