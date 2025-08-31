import os
import functions.config

##MAX_CHARS=10000

def get_file_content(working_directory, file_path):
    try:
        curr_dir = os.getcwd()
        tmp_full_path1 = os.path.join(curr_dir, working_directory)
        tmp_full_path2 = os.path.join(tmp_full_path1, file_path)
        full_path = os.path.abspath(tmp_full_path2)
        full_wd = os.path.abspath(curr_dir)
        if full_path.startswith(full_wd) is False:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if os.path.isfile(full_path) is False:
            return f'Error: "{file_path}" is not a file'

        file_content_string = ""
        flagsize = False

            
        if os.path.getsize(full_path) > functions.config.MAX_CHARS:
            flagsize = True

        with open(full_path, "r") as f:
            file_content_string = f.read(functions.config.MAX_CHARS)
            if flagsize is True:
                file_content_string += f'[...File "{file_path}" truncated at {functions.config.MAX_CHARS} characters]'

            return file_content_string 

    except Exception as e:
        ret = f"Error: {e}"
        return ret
    



