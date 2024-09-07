from lexer import Lexer
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

    parser = Parser(tokens)
    tree = parser.parse()
    print(tree)

    interpreter = Interpreter(tree, base)
    result = interpreter.interpret()
    if result is not None:
        print(result)
