#! /usr/bin/env python

import unittest
import sys
import os
import shutil
sys.path.insert(0, os.path.abspath("../.."))
from make.py.make_log import start_make_logging
from make.py.dir_mod import clear_output_dirs
from make.py.private.exceptionclasses import CritError
from nostderrout import nostderrout


class testStartMakeLogging(unittest.TestCase):

    def test_default_directories(self):
        self.assertFalse(os.path.isdir('../output/'))
        self.assertFalse(os.path.isdir('../temp/'))
        with nostderrout():
            clear_output_dirs()
            start_make_logging()
        self.assertTrue(os.path.isdir('../output/'))
        self.assertTrue(os.path.isdir('../temp/'))
        self.assertTrue(os.path.isfile('../output/make.log'))

    def test_custom_directories(self):
        self.assertFalse(os.path.isdir('../customoutput/'))
        self.assertFalse(os.path.isdir('../customtemp/'))
        with nostderrout():
            clear_output_dirs('../customoutput/', '../customtemp/')
            start_make_logging('../customoutput/make.log')
        self.assertTrue(os.path.isdir('../customoutput/'))
        self.assertTrue(os.path.isdir('../customtemp/'))
        self.assertTrue(os.path.isfile('../customoutput/make.log'))

    def test_not_create_directories(self):
        with nostderrout():
            start_make_logging('../make.log')
        self.assertFalse(os.path.isdir('../output/'))
        self.assertFalse(os.path.isdir('../temp/'))
        self.assertTrue(os.path.isfile('../make.log'))

    def test_not_create_directories_failure(self):
        self.assertFalse(os.path.isdir('../output/'))
        with nostderrout():
            with self.assertRaises(CritError):
                start_make_logging('../output/make.log')

    def tearDown(self):
        if os.path.isdir('../output/'):
            shutil.rmtree('../output/')
        if os.path.isdir('../temp/'):
            shutil.rmtree('../temp/')
        if os.path.isdir('../customoutput/'):
            shutil.rmtree('../customoutput/')
        if os.path.isdir('../customtemp/'):
            shutil.rmtree('../customtemp/')
        if os.path.isfile('../make.log'):
            os.remove('../make.log')

if __name__ == '__main__':
    os.getcwd()
    unittest.main()
