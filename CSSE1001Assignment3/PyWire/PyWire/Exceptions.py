"""Module defines standard exceptions used throughtout pywire"""

import exceptions

class PURE_VIRTUAL_UNDEFINED(exceptions.Exception): pass;
class SYSTEM_INIT_FAIL(exceptions.Exception): pass;
class NO_SUCH_FILE(exceptions.Exception): pass;
class GENERAL_FILE_ERROR(exceptions.Exception): pass;
class INVALID_VALUE(exceptions.Exception): pass;

