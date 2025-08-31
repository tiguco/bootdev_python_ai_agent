import os
import sys
import argparse
from dotenv import load_dotenv
from google.genai import types
from google import genai
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file

verbose_mode = False

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    DEFAULT_WORKING_DIRECTORY = "calculator"

    function_dict = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }

    if not function_call_part.name in function_dict:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

    function_result = function_dict.get(function_call_part.name)(working_directory=DEFAULT_WORKING_DIRECTORY, **function_call_part.args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_result},
            )
        ],
    )




def get_declared_functions():
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
    
    schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="Lists the contents of a file, constrained to the working directory. This function truncates the output to 10000 characters to large files.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to read the files from, relative to the working directory. If not provided, the function will return an error.",
                ),
            },
        ),
    )

    schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Overwrites the contents of the given file with the given content, constrained to the working directory. If the file does not exists, it will be created.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The file path for the file, relative to the working directory. If not provided, the function will return an error.",
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="The content to put into the file."
                ),
            },
        ),
    )

    schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Executes the given python file with optional arguments, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The file path for the file, relative to the working directory. If not provided, the function will return an error.",
                ),
            },
        ),
    )

    return [
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ]

def main():

    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description="A chatgpt-like program.")
    parser.add_argument("query", help="The query to the AI system.")
    # Add an optional argument with a default value
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output.")
    # Parse the command-line arguments
    args = parser.parse_args()
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    if len(sys.argv) > 1:
        pergunta = args.query
    else:
        print("Error: no arguments provided")
        sys.exit(1)

    verbose_mode = False
    if args.verbose:
        verbose_mode = True
    else:
        verbose_mode = False

    available_functions = types.Tool(
            function_declarations=get_declared_functions()
        )

    messages = [
        types.Content(role="user", parts=[types.Part(text=pergunta)]),
    ]

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons. The calculator is a directory where the project's source code is stored.
    """

    model_name = 'gemini-2.0-flash-001'

    done = False
    MAX_ITERATIONS = 20
    iterations = 1

    while not done or iterations > MAX_ITERATIONS:

        config_resp=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)

        response = client.models.generate_content(
            model=model_name,
            contents=messages,
            config=config_resp,
        )

        candidates = response.candidates

        for candidate in candidates:
            messages.append(candidate.content)

        function_calls_made = response.function_calls

        if function_calls_made is not None:
            for function_call in function_calls_made:
                function_result = call_function(function_call, verbose=verbose_mode)
                
                if function_result.parts[0].function_response.response is None:
                    raise RuntimeError("Function response missing")
                
                messages.append(function_result)

                if verbose_mode:
                    print(f"-> {function_result.parts[0].function_response.response}")
        
        else:
            done = True

        iterations += 1

    print(response.text)

    if verbose_mode:
        print(f"User prompt: {pergunta}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()

