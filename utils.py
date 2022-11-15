import json
import subprocess
import traceback


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
            try:
                lines.append(line.strip())
            except Exception as e:
                print("** exception occurred during Popen callback")
                print(traceback.format_exc())

    retcode = proc.poll()

    stdout, stderr = proc.communicate()

    return retcode, callable_formatter("".join(lines))
