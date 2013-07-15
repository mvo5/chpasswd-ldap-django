#!/usr/bin/python3
# -*- Mode: Python; indent-tabs-mode: nil; tab-width: 4; coding: utf-8 -*-

# Partly based on a script from Review Board, MIT license; but modified to
# act as a unit test.

from __future__ import print_function

import os
import subprocess
import unittest

CURDIR = os.path.dirname(os.path.abspath(__file__))


# this can go once we do no longer support py2.6, then
# we can simply use subprocess.check_output()
def check_output(*args, **kwargs):
    kwargs["stdout"] = subprocess.PIPE
    p = subprocess.Popen(*args, **kwargs)
    stdout, stderr = p.communicate()
    ret_code = p.wait()
    if ret_code != 0:
        raise subprocess.CalledProcessError(ret_code, args[0], stdout)
    return stdout


class TestPyflakesClean(unittest.TestCase):

    def test_pyflakes_clean(self):
        # gather all py files we care about
        cmd = ["find", os.path.abspath(os.path.join(CURDIR, "..")),
               "-type", "f",
               "!", "-path", "*/components/*",
               "-and",
               "-name", "*.py"]
        files = check_output(cmd)
        # canary
        self.assertTrue("chpasswd/views.py" in files)
        # run them through pyflakes
        cmd = ["pyflakes"] + files.splitlines()
        try:
            check_output(cmd).splitlines()
        except subprocess.CalledProcessError as e:
            self.fail("pyflakes failed with:\n%s" % e.output)


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
