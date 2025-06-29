import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)


def get_files_info(working_directory, directory=None):
    working_directory_path = os.path.abspath(working_directory)
    directory_path = os.path.abspath(os.path.join(working_directory, directory))

    if not os.path.isdir(directory_path):
        return f'Error: "{directory}" is not a directory'

    if not directory_path.startswith(working_directory_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    try:
        ls = os.listdir(path=directory_path)
    except OSError:
        raise Exception("Error: couldnt list directory")

    formatted_string = "\n".join(
        list(map(lambda file_name: format_file(file_name, directory_path), ls))
    )

    return formatted_string


def format_file(file_name, path):
    file_path = os.path.join(path, file_name)
    file_size = os.path.getsize(file_path)
    is_dir = os.path.isdir(file_path)

    return f"- {file_name}: file_size={file_size} bytes, is_dir={is_dir}"
