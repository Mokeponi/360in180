import unittest
import os
from nose.tools import eq_, raises

import threesixtyinoneeighty as dut

class TestTwitter(unittest.TestCase):
    def test_envvars_good(self):
        os.environ['TWITTER_ACCESS_KEY'] = "test123"
        os.environ['TWITTER_SECRET_KEY'] = "derpherpserp"
        duc = dut.TwitterOAuth()

    @raises(Exception)
    def test_vars_bad(self):
        del os.environ['TWITTER_ACCESS_KEY']
        del os.environ['TWITTER_SECRET_KEY']
        duc = dut.TwitterOAuth()
