#! /usr/bin/env python

import sys
import os
import datetime
import re
import string

import make.py.private.messages as messages
import make.py.private.metadata as metadata
from make.py.private.preliminaries import print_error, files_list
from make.py.private.exceptionclasses import CritError, SyntaxError

######################################################
# Set default options
######################################################


def set_option(**kwargs):
    """This function takes a dictionary as the input and overwrite the default
    values of the settings in metadata. The key identifies the setting to be
    changed, and the value will be the new default value of that setting."""

    try:
        dict((k.lower(), v) for k, v in kwargs.items())

        keylist = metadata.settings.keys()

        file_keylist = [k for k in keylist if k.endswith('file')]
        dir_keylist = [k for k in keylist if k.endswith('dir')]

        # filekey or filekey without "_file" should both work
        n = len("_file")
        for filekey in file_keylist:
            if filekey in kwargs.keys():
                metadata.settings[filekey] = kwargs[filekey]
                if filekey[:-n] in kwargs.keys():
                    raise SyntaxError(messages.syn_error_dupkeys % (filekey,
                                      filekey[:-n]))
            elif filekey[:-n] in kwargs.keys():
                metadata.settings[filekey] = kwargs[filekey[:-n]]

        # dirkey or dirkey without "_dir" should both work
        n = len("_dir")
        for dirkey in dir_keylist:
            if dirkey in kwargs.keys():
                metadata.settings[dirkey] = kwargs[dirkey]
                if dirkey[:-n] in kwargs.keys():
                    raise SyntaxError(messages.syn_error_dupkeys % (dirkey,
                                      dirkey[:-n]))
            elif dirkey[:-n] in kwargs.keys():
                metadata.settings[dirkey] = kwargs[dirkey[:-n]]
    except Exception as errmsg:
        print("Error with set_option: \n", errmsg)


######################################################
# Logging
######################################################

def start_make_logging(makelog='@DEFAULTVALUE@'):
    """Start "makelog" log file with time stamp."""

    # metadata.settings should not be part of argument defaults so that they
    # can be overwritten by make_log.set_option
    if makelog == '@DEFAULTVALUE@':
        makelog = metadata.settings['makelog_file']

    metadata.makelog_started = True

    print("\nStart log file: ", makelog)

    makelog = re.sub('\\\\', '/', makelog)

    try:
        LOGFILE = open(makelog, 'w')
    except Exception as errmsg:
        raise CritError((messages.crit_error_log % makelog) + '\n' +
                        str(errmsg))

    try:
        # Add time stamp
        time_begin = datetime.datetime.now().replace(microsecond=0)
        sys.stderr = LOGFILE
        working_dir = os.getcwd()
        print(messages.note_makelogstart, time_begin,
              working_dir, '\n\n', file=LOGFILE)
    except Exception as errmsg:
        print("Error with start_make_logging: \n", errmsg)

    LOGFILE.flush()


def end_make_logging(makelog='@DEFAULTVALUE@'):
    """End "makelog" log file with time stamp."""

    # metadata.settings should not be part of argument defaults so that they
    # can be overwritten by make_log.set_option
    if makelog == '@DEFAULTVALUE@':
        makelog = metadata.settings['makelog_file']

    if not (metadata.makelog_started and os.path.isfile(makelog)):
        raise CritError(messages.crit_error_nomakelog % makelog)

    print("\nEnd log file: ", makelog)

    makelog = re.sub('\\\\', '/', makelog)
    try:
        LOGFILE = open(makelog, 'a')
    except Exception as errmsg:
        raise CritError((messages.crit_error_log % makelog) + '\n' +
                        str(errmsg))
    time_end = datetime.datetime.now().replace(microsecond=0)
    print(messages.note_makelogend, time_end, file=LOGFILE)
    LOGFILE.flush()
    LOGFILE.close()

######################################################
# Add and Delete from Log
######################################################


def add_log(*args, **kwargs):
    """Add log files in "*arg" list to "makelog" log file."""

    # metadata.settings should not be part of argument defaults so that they
    # can be overwritten by make_log.set_option
    if 'makelog' in kwargs.keys():
        makelog = kwargs['makelog']
    else:
        makelog = metadata.settings['makelog_file']

    if not (metadata.makelog_started and os.path.isfile(makelog)):
        raise CritError(messages.crit_error_nomakelog % makelog)

    print("\nAdd log file(s) to: ", makelog)

    makelog = re.sub('\\\\', '/', makelog)
    try:
        LOGFILE = open(makelog, 'a')
    except Exception as errmsg:
        raise CritError((messages.crit_error_log % makelog) + '\n' +
                        str(errmsg))

    try:
        for log in args:
            log = re.sub('\\\\', '/', log)
            if not os.path.isfile(log):
                print(messages.note_nofile % log, file=LOGFILE)
            else:
                print(open(log, 'r').read(), file=LOGFILE)
    except:
        print_error(LOGFILE)

    LOGFILE.flush()
    LOGFILE.close()


def del_log(*args, **kwargs):
    """Delete each of the log files listed in "*arg" list.
    Errors are printed to "makelog" log file."""

    # metadata.settings should not be part of argument defaults so that they
    # can be overwritten by make_log.set_option
    if 'makelog' in kwargs.keys():
        makelog = kwargs['makelog']
    else:
        makelog = metadata.settings['makelog_file']

    if not (metadata.makelog_started and os.path.isfile(makelog)):
        raise CritError(messages.crit_error_nomakelog % makelog)

    print("\nDelete log file(s)")

    makelog = re.sub('\\\\', '/', makelog)
    try:
        LOGFILE = open(makelog, 'a')
    except Exception as errmsg:
        raise CritError((messages.crit_error_log % makelog) + '\n' +
                        str(errmsg))

    try:
        for log in args:
            log = re.sub('\\\\', '/', log)
            if os.path.isfile(log):
                os.remove(log)
            else:
                print(messages.note_nofile % log, file=LOGFILE)
    except:
        print_error(LOGFILE)

    LOGFILE.flush()
    LOGFILE.close()

######################################################
# Log file stats and file heads
######################################################


def make_output_local_logs(output_local_dir='@DEFAULTVALUE@',
                           output_dir='@DEFAULTVALUE@',
                           stats_file='@DEFAULTVALUE@',
                           heads_file='@DEFAULTVALUE@',
                           recur_lim=1):

    if output_local_dir == '@DEFAULTVALUE@':
        output_local_dir = metadata.settings['output_local_dir']
    if output_dir == '@DEFAULTVALUE@':
        output_dir = metadata.settings['output_dir']
    if stats_file == '@DEFAULTVALUE@':
        stats_file = metadata.settings['stats_file']
    if heads_file == '@DEFAULTVALUE@':
        heads_file = metadata.settings['heads_file']

    sorted_files = files_list(output_local_dir, recur_lim)

    make_stats_log(output_dir, stats_file, sorted_files)
    make_heads_log(output_dir, heads_file, sorted_files)


def make_stats_log(output_dir, stats_file, all_files):
    """Create a log file at "stats_file" in "output_dir" of statistics of the
    files listed in "all_files". The statistics are (in order): file name, date
    and time last modified, and file size."""

    if stats_file == '':
        return

    stats_path = os.path.join(output_dir, stats_file)
    stats_path = re.sub('\\\\', '/', stats_path)
    header = "file name\tlast modified\tfile size"

    if not os.path.isdir(os.path.dirname(stats_path)):
        os.makedirs(os.path.dirname(stats_path))
    STATSFILE = open(stats_path, 'w+')
    print(header, file=STATSFILE)

    for file_name in all_files:
        stats = os.stat(file_name)
        last_mod = datetime.datetime.utcfromtimestamp(round(stats.st_mtime))
        file_size = stats.st_size

        print("%s\t%s\t%s" % (file_name, last_mod, file_size), file=STATSFILE)
    STATSFILE.flush()
    STATSFILE.close()


def make_heads_log(output_dir, heads_file, all_files, head_lines=10):
    """Create a log file at "heads_file" in "output_dir" of the first
    "head_lines" lines of each file listed in "all_files"."""

    if heads_file == '':
        return

    heads_path = os.path.join(output_dir, heads_file)
    heads_path = re.sub('\\\\', '/', heads_path)
    header = "File headers"

    if not os.path.isdir(os.path.dirname(heads_path)):
        os.makedirs(os.path.dirname(heads_path))
    HEADSFILE = open(heads_path, 'w+')
    print(header, file=HEADSFILE)
    print("\n%s\n" % ("-" * 65), file=HEADSFILE)

    for file_name in all_files:
        print("%s\n" % file_name, file=HEADSFILE)
        try:
            f = open(file_name)
        except:
            f = False
            print("Head not readable", file=HEADSFILE)

        if f:
            for i in range(head_lines):
                try:
                    line = next(f).strip()
                    cleaned_line = filter(lambda x: x in string.printable,
                                          line)
                    print(cleaned_line, file=HEADSFILE)
                except:
                    break

        print("\n%s\n" % ("-" * 65), file=HEADSFILE)

    HEADSFILE.flush()
    HEADSFILE.close()
