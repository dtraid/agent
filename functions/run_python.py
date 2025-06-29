import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the specified Python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the Python file to run, relative to the working directory.",
            ),
        },
    ),
)


def run_python_file(working_directory, file_path):
    working_directory_path = os.path.abspath(working_directory)
    absolute_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not absolute_file_path.startswith(working_directory_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(absolute_file_path):
        return f'Error: File "{file_path}" not found.'

    if not absolute_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        completed_process = subprocess.run(
            ["python3", absolute_file_path],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=working_directory_path,
        )

        stdout = (
            completed_process.stdout
            if completed_process.stdout != b""
            else "No output produced."
        )

        stderr = (
            completed_process.stderr
            if completed_process.stderr != b""
            else "No output produced."
        )

        print(f"STDOUT: {stdout}")
        print(f"STDERR: {stderr}")
        if completed_process.returncode != 0:
            print(f"Process exited with code {completed_process.returncode}")

    except Exception as e:
        return f"Error: executing Python file: {e}"
