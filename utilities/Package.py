import os
import json

is_local_server = False

if 'IS_CLOUD' in os.environ:
    is_local_server = False
else:
    dirName = "Joulie"

    workDir = os.path.dirname(os.path.realpath(__file__))
    index = workDir.rfind(dirName)
    if index == -1:
        raise Exception("Unknown workng directory: " + workDir)

    workDir = workDir[:index + len(dirName)]

    try:
        with open(os.path.join(workDir, 'package.json')) as data_file:
            data = json.load(data_file)

            is_local_server = data["is_local"] in ['true', 'True', 'TRUE']
            if is_local_server:
                print "Running in local server mode"
            else:
                print "Running in remote server mode"
    except Exception:
        print "Running in remote server mode"


def is_local():
    return is_local_server
