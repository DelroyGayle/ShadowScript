from lexer import Error


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.idx = 0
        self.token = self.tokens[self.idx]

    def factor(self):
        if self.token.type == 'INT' or self.token.type == 'FLT':
            return self.token

        elif self.token.value == '(':
            self.move()
            expression = self.boolean_expression()
            return expression

        # not <expr>
        elif self.token.value == 'not':
            operator = self.token
            self.move()
            output = [operator, self.factor()]
            return output

        # Variables
        elif self.token.type.startswith('VAR'):
            print(self.token)
            return self.token

        # Unary Operators + <expr> | - <expr>
        elif self.token.value == '+' or self.token.value == '-':
            operator = self.token
            self.move()
            operand = self.factor()
            return [operator, operand]

    def term(self):
        left_node = self.factor()
        self.move()

        # <expr> * <expr> ... | <expr> / <expr> ...
        while self.token.value == '*' or self.token.value == '/':
            operator = self.token
            self.move()
            right_node = self.factor()
            self.move()

            left_node = [left_node, operator, right_node]

        return left_node

    def plus_sub_expression(self):
        left_node = self.term()
        # <expr> + <expr> | <expr> - <expr>
        while self.token.value == '+' or self.token.value == '-':
            operator = self.token
            self.move()
            right_node = self.term()
            left_node = [left_node, operator, right_node]

        return left_node

    def comp_expression(self):
        left_node = self.plus_sub_expression()
        # <expr> ?= <expr> ... | <expr> '>' <expr> ... |
        # <expr> '<' <expr> ... |
        # <expr> <= <expr> ... | <expr> '>=' <expr> ...
        while self.token.type == 'COMP':
            operator = self.token
            self.move()
            right_node = self.plus_sub_expression()
            left_node = [left_node, operator, right_node]

        return left_node

    def boolean_expression(self):
        left_node = self.comp_expression()

        while self.token.value == 'and' or self.token.value == 'or':
            operator = self.token
            self.move()
            right_node = self.comp_expression()
            left_node = [left_node, operator, right_node]

        return left_node

    def variable(self):
        if self.token.type.startswith('VAR'):
            return self.token

    def if_statement(self):
        self.move()
        condition = self.boolean_expression()

        if self.token.value == 'do':
            self.move()
            action = self.statement()

            return condition, action
        elif self.tokens[self.idx-1].value == 'do':
            action = self.statement()
            return condition, action

    def if_statements(self):
        conditions = []
        actions = []
        if_statement = self.if_statement()

        conditions.append(if_statement[0])
        actions.append(if_statement[1])

        while self.token.value == 'elif':
            if_statement = self.if_statement()
            conditions.append(if_statement[0])
            actions.append(if_statement[1])

        if self.token.value == 'else':
            self.move()
            self.move()
            else_action = self.statement()

            return [conditions, actions, else_action]

        return [conditions, actions]

    def while_statement(self):
        self.move()
        condition = self.boolean_expression()

        if self.token.value == 'do':
            self.move()
            action = self.statement()
            return [condition, action]

        elif self.tokens[self.idx-1].value == 'do':
            action = self.statement()
            return [condition, action]

    def statement(self):
        print(self.token.type, self.token.value)
        if self.token.type == 'DECL':
            self.move()
            left_node = self.variable()
            self.move()
            if self.token.value == '=':
                operation = self.token
                self.move()
                right_node = self.boolean_expression()

                return [left_node, operation, right_node]

        elif (self.token.type == 'INT' or self.token.type == 'FLT' or
              self.token.type == 'OP' or self.token.value == 'not'):
            return self.boolean_expression()

        elif self.token.value == 'if':
            return [self.token, self.if_statements()]

        elif self.token.value == 'while':
            return [self.token, self.while_statement()]

        # Add error handling
        else:
            raise TypeError('I do not understand this statement',
                            f"{self.token.value}")

    def parse(self):
        return self.statement()

    def move(self):
        self.idx += 1
        if self.idx < len(self.tokens):
            self.token = self.tokens[self.idx]
