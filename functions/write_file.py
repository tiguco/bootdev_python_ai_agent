import os

def write_file(working_directory, file_path, content):
    try:
        curr_dir = os.getcwd()
        tmp_full_path1 = os.path.join(curr_dir, working_directory)
        tmp_full_path2 = os.path.join(tmp_full_path1, file_path)
        full_path = os.path.abspath(tmp_full_path2)
        full_wd = os.path.abspath(curr_dir)
        if full_path.startswith(full_wd) is False:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        directory_path = os.path.dirname(full_path)
        if os.path.exists(directory_path) is False:
            os.makedirs(directory_path)
        with open(full_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        ret = f"Error: {e}"
        return ret
    



