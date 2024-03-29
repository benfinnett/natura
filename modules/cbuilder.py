import os
import openai

def generate_c(token_stream: list[dict[str, str]], api_key: str, persist_console: bool = False) -> str:
    """Creates C code from a token stream using the OpenAI API.

    Args:
        token_stream (list[dict[str, str]]): A list of tokens generated by the tokeniser.
        api_key (str): The OpenAI API key.
        persist_console (bool, optional): Whether to inject code to keep the console open after the program has completed executing. Defaults to False.

    Raises:
        ValueError: If the OpenAI API returns an error.

    Returns:
        str: The generated C code.
    """
    openai.api_key = api_key

    response = openai.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': 'Create C code from the following token stream:\n' + str(token_stream)}],
        temperature=0.0
    )

    response_content = response.choices[0].message.content

    if not response_content:
        raise ValueError(f'Unable to generate C code: {response.choices[0].message.content}')

    if persist_console:
        code_lines = response_content.split('\n')

        code_lines.insert(1, '#include <stdlib.h>')
        code_lines.insert(len(code_lines) - 2, '    system("pause");')
        code_lines.insert(len(code_lines) - 2, '    printf("\\n");')

        response_content = '\n'.join(code_lines)
    
    return response_content    

def build_executabe(c_code: str, file_path: str) -> None:
    """Builds a C executable from C code using gcc.

    Args:
        c_code (str): The textual C code to compile.
        file_name (str): The file name of the executable.
    """
    root, filename = os.path.split(file_path)
    filename = os.path.splitext(filename)[0]
    output_directory = os.path.join(root, 'out')

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    file_path = os.path.join(output_directory, filename)

    with open(file_path + '.c', 'w') as file:
        file.write(c_code)

    os.system(f'gcc -o "{file_path}.exe" "{file_path}.c"')
    os.remove(file_path + '.c')
