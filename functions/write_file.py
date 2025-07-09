import os
from google.genai import types

def write_file(working_dir, file_path, content):
    target_path = os.path.abspath(os.path.join(working_dir, file_path or "."))
    working_dir_abs = os.path.abspath(working_dir)

    if not target_path.startswith(working_dir_abs):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    try:
        if not os.path.exists(target_path):
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
    except Exception as e:
        return f'Error: {e}'
    
    with open(target_path, "w") as f:
        f.write(content)
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content to a file given the working directory and file path.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path that indicates which to write the content to. relative to the working directory. If the file does not exist it should be created in the working directory"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written into the file defined thorugh file_path parameter"
            ),
        },
    ),
)