"""Contains functions for logging user input and program output to file"""

import os
import sys

#The logs are represented by arrays of strings, probably
#the easiest way to represent an array lines of input.
SYSTEM_LOG = []
CMD_LOG = []


def PrintAndLogGExcept(indent_level = 1):
    """PrintAndLogGExcept -> int -> none

prints any curretn exception description"""

    print MakeIndent(indent_level) +"ERROR: " + str(sys.exc_info()[1])
    SYSTEM_LOG.append("ERROR: " + str(sys.exc_info()[1]))

def MakeIndent(indent_level):
    """MakeIndent -> int -> int

Make the indest string, which is just a string of leading spaces."""

    indent_str = ""

    for i in range(0, indent_level):

        indent_str = indent_str + "    "

    return indent_str

def PrintAndLogG(a, indent_level = 1):
    """PrintAndLogG -> string, int -> none

print string 'a' to the console, and log this into the system log."""

    print MakeIndent(indent_level) + a
    SYSTEM_LOG.append(a)

def LogGWriteSeperator():
    """LogGWriteSeperator -> none -> none

write a seperating bar to the general log."""
    PrintAndLogG("--------------------------------------------------------------------------------", 0)

def LogC(a):

    print a
    CMD_LOG.append(a)    


def WriteLogs(fns, fnc):
    """WriteLogs -> str, str -> none

Write the system and comman logs to file under the respectively given filenames."""

    __WriteLog(SYSTEM_LOG, fns)
    __WriteLog(CMD_LOG, fnc)

def DumpLogs(fns, fnc):
    """DumpLogs -> str, str -> none

Write both logs to file, and then clear both in memory."""

    WriteLogs(fns, fnc)

    ClearLogs()

def ClearLogs():
    """ClearLogs -> none -> none

CLear the system and command logs."""

    del SYSTEM_LOG[:]
    del CMD_LOG[:]

def __WriteLog(a, fn):
    """__WriteLog -> list, str -> none

Write the supplied log to file, at the filename fn."""

    File = open(fn, "w")
    File.writelines(a)
    File.close()
