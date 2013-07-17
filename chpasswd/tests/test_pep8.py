import os
import subprocess
import unittest


class PackagePep8TestCase(unittest.TestCase):

    def test_all_code(self):
        res = 0
        py_dir = os.path.join(os.path.dirname(__file__), "..")
        res += subprocess.call(
            ["pep8",
             "--ignore=E121,E123,E124,E125,E126,E127,E128",
             "--exclude", "static,tastypie_test_v0912.py",
             "--repeat", os.path.abspath(py_dir)])
        self.assertEqual(res, 0)


if __name__ == "__main__":
    unittest.main()
