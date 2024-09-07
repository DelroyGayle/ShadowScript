from lexer import Lexer, Error
from parse import Parser
from interpreter import Interpreter
from data import Data

base = Data()

"""
'exit' added to end the running of the script
"""

while True:
    text = input('ShadowScript: ').strip()

    if text == '':
        continue
    elif text == 'exit':
        break

    tokenizer = Lexer(text)
    tokens = tokenizer.tokenize()

    # Check for a syntax error
    if isinstance(tokens, Error):
        message = tokens.error_name
        if (tokens.error_details):
            message += f': {tokens.error_details}'
        print(message)
        continue

    parser = Parser(tokens)
    try:
        tree = parser.parse()
    except TypeError as an_error:
        # Syntax Error Handling
        message, error_details = an_error.args
        if error_details:
            message += f': {error_details}'
        print(message)
        continue

    print(tree)

    interpreter = Interpreter(tree, base)
    result = interpreter.interpret()
    if result is not None:
        print(result)
