import os
import subprocess
from google.genai import types

def run_python_file(working_dir, file_path):
    target_path = os.path.abspath(os.path.join(working_dir, file_path or "."))
    working_dir_abs = os.path.abspath(working_dir)

    if not target_path.startswith(working_dir_abs):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    elif not os.path.exists(target_path):
        return f'Error: File "{file_path}" not found.'
    elif not target_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    else:
        try:
            process = subprocess.run(["python3", target_path],capture_output=True, timeout=30, cwd=working_dir_abs, check=False, text=True)
            if not process.stdout and not process.stderr:
                return f'No output produced' 
            
            elif process.returncode != 0:
                return f'STDOUT:{process.stdout}\nSTDERR:{process.stderr}\nProcess exited with code {process.returncode}'
            
            else:
                return f'STDOUT:{process.stdout}\nSTDERR:{process.stderr}'
            
        except Exception as e:
            return f'Error: executing Python file: {e}'
        
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a python file via subprocess.run() given the working directory and file path. Checks the extension of the file is really '.py' before running.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path that indicates which file to run, relative to the working directory."
            )
        },
    ),
)