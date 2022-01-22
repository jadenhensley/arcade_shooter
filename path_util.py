import os
import re
import pathlib

def get_project_directory():
    SCRIPTPATH = os.path.realpath(__file__)
    # print(os.name)
    # print(SCRIPTPATH)
    # print("Script path: ", SCRIPTPATH)

    path = [""]
    i = 0

    if os.name == 'nt':
        backslash_count = SCRIPTPATH.count("\\")
        # print(backslash_count)

        for char in SCRIPTPATH:
            if "\\" == char:
                i += 1
            # print(path)
            if i != backslash_count:
                path[0] += char

        # print(path)

        before = pathlib.PureWindowsPath(rf'{path}')
        # print(before)
        before = pathlib.PurePosixPath(rf'{path}')
        # print(before)
        after_path = before.as_posix().replace('[','').replace(']', '').replace("'",'')
        # .pop(']').pop('[')
        

        # print(after_path)
    elif os.name == "posix":
        forwardslash_count = SCRIPTPATH.count("/")
        print(forwardslash_count)

        for char in SCRIPTPATH:
            if "/" == char:
                i += 1
            if i != forwardslash_count:
                path[0] += char
        after_path = path[0].replace('[','').replace(']', '').replace("'",'')
        print(after_path)
    return after_path

get_project_directory()