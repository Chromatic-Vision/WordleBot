import enum
from datetime import datetime

import os
import io
import traceback
import re

class Logger:

    def __init__(self, colored: bool, write_to_file: bool, format_: str, color_mappings=None, filename="latest.log"):
        if color_mappings is None:
            color_mappings = [
                "\033[34m", # 0, timestamp
                "\033[36m", # 1, traceback
                "\033[32m", # info
                "\033[33m", # warn
                "\033[31m" # error
            ]
        self.colored = colored
        self.write_to_file = write_to_file
        self.format = format_
        self.color_mappings = color_mappings
        self.filename = filename

    def _write(self, args, type_: int):

        message = ' '.join(map(str, args))

        print(self.parse(self.format, message, self.colored, type_))

        if self.write_to_file:
            self.write(self.parse(self.format, message, False, type_))

    def log(self, *args):
        self._write(args, InfoType.INFO)

    def warn(self, *args):
        self._write(args, InfoType.WARN)

    def error(self, *args):
        self._write(args, InfoType.ERROR)

    def write(self, content):
        with open(self.filename, 'a', encoding="UTF-8") as f:
            f.write(content + "\n")
            f.close()

    def reset_log(self):

        if not self.write_to_file:
            return

        if self.filename not in os.listdir('.'):
            with open(self.filename, 'w', encoding="UTF-8") as f:
                f.close()
                return

        with open(self.filename, 'w', encoding="UTF-8") as f:
            f.truncate()
            f.close()

    def parse(self, format: str, message: str, colors: bool, type: int):

        if type > 3:
            raise ValueError(f"Unknown type: {type}")

        res = ""

        if colors:
            res += "\033[0m" # reset all colors, if needed

        res += datetime.now().strftime(format)
        res = res.replace("$info", str(InfoType(type).name)) # string based on type, e.g. WARN, ERROR...

        if colors:
            res = res.replace("$reset", "\033[0m")  # reset color
            res = res.replace("$color", self.color_mappings[type + 1]) # color based on type, e.g. "\033[33m" (represents yellow), here its +2 because indexes 0, 1 is used for other color
            res = res.replace("$timecolor", self.color_mappings[0])
            res = res.replace("$tracecolor", self.color_mappings[1])
        else:
            res = res.replace("$color", "")
            res = res.replace("$reset", "")
            res = res.replace("$timecolor", "")
            res = res.replace("$tracecolor", "")

        filename, func, line = self.trace()
        res = res.replace("$filename", filename) # filename of function
        res = res.replace("$funcname", func) # name of function
        res = res.replace("$line", line) # line of function
        res = res.replace("$message", message) # message

        return res

    def trace(self) -> tuple[str, str, str]:

        _filename = []
        _func = []
        _line = []

        trace = io.StringIO()
        traceback.print_stack(file=trace)
        trace_string = trace.getvalue()
        # print(trace_string)
        trace.close()

        split = trace_string.split('\n')
        for line in split[:-1:2]:
            # print(line)
            m = re.search('\\s{2}File "(.+?)", line ([0-9]+), in (.+)$', line)
            # print(m)
            assert m is not None, str(m)

            _filename.append(os.path.basename(m.group(1)))
            _line.append(m.group(2))
            _func.append(m.group(3))

        # return _filename, _func, _line
        return _filename[-4], _func[-4], _line[-4]

class InfoType(enum.IntEnum):
    INFO = enum.auto()
    WARN = enum.auto()
    ERROR = enum.auto()
    INVALID = enum.auto()