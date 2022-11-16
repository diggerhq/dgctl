import json
import os
import re
import subprocess

RE_BUNDLE_ID = re.compile(r"^environment-(.*)-\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}")


def get_bundle_id():
    """
    Parse bundle id from current working directory name.
    "/home/digger/environment-abc-987-2022-11-16-12-50-15" -> "abc-987"
    """
    cwd = os.path.split(os.getcwd())[-1]
    r = re.match(RE_BUNDLE_ID, cwd)
    return r.groups()[0]


def popen_to_object(exec_array, callable_formatter, **kwargs):
    # proc = subprocess.run(["ping", "google.com"])
    stdout = kwargs.pop("stdout", subprocess.PIPE)
    stderr = kwargs.pop("stderr", subprocess.STDOUT)
    proc = subprocess.Popen(
        exec_array, stdout=stdout, stderr=stderr, encoding="utf-8", **kwargs
    )

    lines = []
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        if line:
            lines.append(line.strip())

    retcode = proc.poll()
    proc.communicate()

    return retcode, callable_formatter("".join(lines))
