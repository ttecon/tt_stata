#! /usr/bin/env python

import unittest
import sys
import os
import shutil
sys.path.insert(0, os.path.abspath("../.."))
from make.py.dir_mod import list_directory
from make.py.make_log import start_make_logging
from make.py.dir_mod import clear_output_dirs
from make.py.private.exceptionclasses import CritError
from nostderrout import nostderrout


class testListDirectory(unittest.TestCase):

    def setUp(self):
        if os.path.isdir('./input/externals_list_directory/'):
            shutil.rmtree('./input/externals_list_directory/')
        shutil.copytree('../py', './input/externals_list_directory')

    def test_default_log(self):
        makelog_file = '../output/make.log'
        output_dir = '../output/'
        with nostderrout():
            clear_output_dirs(output_dir, '')
            start_make_logging(makelog_file)
            list_directory('./input/externals_list_directory/')
        self.check_log('./input/externals_list_directory/', makelog_file)
        self.check_log('./input/externals_list_directory/private/',
                       makelog_file)

    def test_custom_log(self):
        makelog_file = '../output/custom_make.log'
        output_dir = '../output/'
        with nostderrout():
            clear_output_dirs(output_dir, '')
            start_make_logging(makelog_file)
            list_directory('./input/externals_list_directory/',
                           '../output/custom_make.log')
        self.check_log('./input/externals_list_directory/', makelog_file)
        self.check_log('./input/externals_list_directory/private/',
                       makelog_file)

    def check_log(self, directory, log_file):
        file_list = os.listdir(directory)
        if 'private' in file_list:
            file_list.remove('private')
        log_data = open(log_file, 'r').readlines()
        log_words = []
        for line in log_data:
            log_words = log_words + line.split(' ')
        for file in file_list:
            if os.path.isfile(file):
                self.assertIn(file, log_words)

    def test_no_makelog(self):
        with nostderrout():
            with self.assertRaises(CritError):
                list_directory('./input/externals_list_directory/')

    def tearDown(self):
        if os.path.isdir('../output/'):
            shutil.rmtree('../output/')
        if os.path.isdir('./input/externals_list_directory/'):
            shutil.rmtree('./input/externals_list_directory/')

if __name__ == '__main__':
    os.getcwd()
    unittest.main()
