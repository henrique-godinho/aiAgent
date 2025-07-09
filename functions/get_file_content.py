import os
from google.genai import types

def get_file_content(working_dir, file_path):
    target_path = os.path.abspath(os.path.join(working_dir, file_path or "."))
    working_dir_abs = os.path.abspath(working_dir)

    if not target_path.startswith(working_dir_abs):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    elif not os.path.isfile(target_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    else:
        MAX_CHARS = 10000
        TRUNCATED_MESSAGE = f'[...File "{file_path}" truncated at 10000 characters]'
        try:
            with open(target_path, "r") as f:
                full_content = f.read()
                if len(full_content) > MAX_CHARS:
                    file_content = full_content[:MAX_CHARS] + TRUNCATED_MESSAGE
                else:
                    file_content = full_content
        except Exception as e:
            return f"Error: {e}"
        
        return file_content
        
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Fetches the file content for the given working directory & file path. Checks if the file content and truncates it to a max of 10000 characters if over that limit.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path that indicates which file to get the content from, relative to the working directory."
            ),
        },
    ),
)