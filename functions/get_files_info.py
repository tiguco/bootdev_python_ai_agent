import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        tmp_full_path = os.path.join(working_directory, directory)
        full_path = os.path.abspath(tmp_full_path)
        full_wd = os.path.abspath(working_directory)
        if full_path.startswith(full_wd) is False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if os.path.isdir(full_path) is False:
            return f'Error: "{directory}" is not a directory'
        #print(full_path)
        lstentries = []
        for entry in os.listdir(full_path):
            full_entry = os.path.join(full_path, entry)
            fsize = os.path.getsize(full_entry)
            resp = ""
            if os.path.isfile(full_entry):
                resp = f"- {entry}: file_size={fsize} bytes, is_dir=False"
            elif os.path.isdir(full_entry):
                resp = f"- {entry}: file_size={fsize} bytes, is_dir=True"
            lstentries.append(resp)
        resp = "\n".join(lstentries)
        return resp
    except Exception as e:
        ret = f"Error: {e}"
        return ret
    


