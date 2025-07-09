import os
from google.genai import types

def get_files_info(working_dir, dir=None):

    target_path = os.path.abspath(os.path.join(working_dir, dir or "."))
    working_dir_abs = os.path.abspath(working_dir)
    
    if not target_path.startswith(working_dir_abs):
        return f'Error: Cannot list "{dir}" as it is outside the permitted working directory'
    elif not os.path.isdir(target_path):
        return f'Error: "{dir}" is not a directory'
    else:
        dir_content = []

        try:
            for item in os.listdir(target_path):
                item_path = os.path.join(target_path, item)
                is_dir = os.path.isdir(item_path)
                file_size = os.path.getsize(item_path)
                dir_content.append(f"- {item}: file_size={file_size}, is_dir={is_dir}")
        except Exception as e:
            return f"Error: {e}"
        
        s = "\n".join(dir_content)
        return s

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "dir": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)