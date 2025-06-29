import os


def write_file(working_directory, file_path, content):
    working_directory_path = os.path.abspath(working_directory)
    absolute_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    directory_path = os.path.dirname(file_path)

    if not absolute_file_path.startswith(working_directory_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(directory_path):
        try:
            os.makedirs(directory_path)
        except Exception as e:
            return f"Error: {e}"

    with open(absolute_file_path, "w") as f:
        f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
