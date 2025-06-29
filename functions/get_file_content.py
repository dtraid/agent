import os
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the content from the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to read for content, relative to the working directory.",
            ),
        },
    ),
)


def get_file_content(working_directory, file_path):
    working_directory_path = os.path.abspath(working_directory)
    absolute_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not absolute_file_path.startswith(working_directory_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(absolute_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    MAX_CHARS = 10000

    with open(absolute_file_path, "r") as f:
        file_content_string = f.read(MAX_CHARS)
        if f.tell() == MAX_CHARS:
            file_content_string += (
                f'[...File "{absolute_file_path}" truncated at 10000 characters]'
            )

    return file_content_string
