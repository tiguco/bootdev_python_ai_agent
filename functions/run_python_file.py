import os
import functions.config
import subprocess

def run_python_file(working_directory, file_path, args=[]):

    try:
        curr_dir = os.getcwd()
        tmp_full_path1 = os.path.join(curr_dir, working_directory)
        tmp_full_path2 = os.path.join(tmp_full_path1, file_path)
        full_path = os.path.abspath(tmp_full_path2)
        full_wd = os.path.abspath(curr_dir)
        full_path = os.path.normpath(full_path)
        full_wd = os.path.normpath(full_wd)
        path2verif = os.path.dirname(full_path)
        path_limit = os.path.normpath(tmp_full_path1)

        ##if full_path.startswith(full_wd) is False:
        if path2verif.startswith(path_limit) is False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if os.path.isfile(full_path) is False or os.path.exists(full_path) is False:
            return f'Error: File "{file_path}" not found.'

        if file_path.endswith(".py") is False:
            return f'Error: "{file_path}" is not a Python file.'

        work_dir = os.path.dirname(full_path)

        runcmd = ["python"]
        runcmd.append(file_path)
        if len(args) > 0:
            for it in args:
                runcmd.append(str(it))
        #runcmd.append(file_path)


        result = subprocess.run(runcmd, cwd=work_dir, timeout=30, capture_output=True, text=True)
        ret = ""
        if len(result.stdout) == 0 and len(result.stderr) == 0:
            ret = "No output produced."
            return ret

        ret = "STDOUT:" + result.stdout
        ret += "STDERR:" + result.stderr
        if result.returncode != 0:
            ret += f"Process exited with code {result.returncode}"
        return ret

    except Exception as e:
        ret = f"Error: executing Python file: {e}"
        return ret
 

