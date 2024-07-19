import re
import regex
from typing import Union


class PushDownAutomata:
    """
        Class for Push Down Automata
    """

    # precedence level of supported operators.
    PRECEDENCE = {
        '*': 3,  # highest precedence level
        '/': 3,
        '+': 2,
        '-': 2,
        '(': 1,
    }

    # stack
    stack = ''
    postfix = []

    def insert(self, value: Union[str, list]) -> None:
        """
            method to insert a value to stack,

            Parameters:
                value: The value to insert to stack
        """

        if type(value) == str and type(self.stack) == str:
            self.stack += value

        else:
            self.stack.append(value)

    def replace(self, value: str) -> Union[str, list]:
        """
            method to replace a value in stack,

            Parameters:
                value: The value to replace in stack
        """

        return self.stack[:-1] + value

    def pop(self) -> Union[str, list]:
        """
            method to pop the stack and return it,
        """

        top = self.stack[-1]
        self.stack = self.stack[:-1]
        return top

    def is_accepted(self, expression: str, current_state: str, transition: dict) -> bool:
        """
            method to check correctness of the math expression with balanced parentheses

            Parameters:
                expression (str): The math expression
                current_state (str): The first state
                transition (dict): The transitions
        """

        self.stack = '$'

        for i in expression:
            # find the right state and conditions
            selected = [j for j in transition if j[0] == current_state and j[1] == i and j[2] == self.stack[-1]]

            if not selected:
                continue

            selected = selected[0]

            # change the current state with the new state
            current_state = transition[selected][0]

            # if the entry is not λ
            if transition[selected][1] != "λ":
                self.stack = self.replace(transition[selected][1])

            else:
                self.pop()

        return self.stack == "$"

    def to_postfix(self, tokens: list) -> str:
        """
            method to convert infix tokens to postfix

            Parameters:
                tokens (str): The infix tokens list
        """

        self.stack = []
        self.postfix = []

        for token in tokens:
            # If the token is an operand pass it to the postfix.
            if token.isalnum():
                self.postfix.append(token)

            # If your current token is a right parenthesis push it on to the stack
            elif token == '(':
                self.insert(token)

            # If your current token is a right parenthesis, pop the stack until after the first left parenthesis.
            # Output all the symbols except the parentheses.
            elif token == ')':
                top = self.pop()

                while top != '(':
                    self.postfix.append(top)
                    top = self.pop()

            # Before we can push the operator onto the stack, we have to pop the stack until you find an operator
            # with a lower priority than the current operator.
            else:
                while self.stack and (self.PRECEDENCE[self.stack[-1]] >= self.PRECEDENCE[token]):
                    self.postfix.append(self.pop())

                self.insert(token)

        # After the entire expression is scanned, pop the rest of the stack
        # and write the operators in the stack to the output.
        while self.stack:
            self.postfix.append(self.pop())

        return ' '.join(self.postfix)

    def to_infix(self, postfix_list: list) -> str:
        """
            method to convert postfix tokens to infix

            Parameters:
                postfix_list (list): The postfix list
        """

        self.stack = []

        for j in range(len(postfix_list)):
            # append the alphabet and numbers to stack
            if postfix_list[j].isalnum():
                self.insert(postfix_list[j])

            else:
                # get the operators and add them to stack with value
                operator1 = self.pop()
                operator2 = self.pop()

                self.insert("(" + operator2 + postfix_list[j] + operator1 + ")")

        return self.pop()

    def evaluate(self, string: str) -> Union[int, str]:
        """
            method to evaluate the infix

            Parameters:
                string (str): The infix string
        """

        try:
            return eval(string)

        except NameError:
            return string


class Main:
    def checker1(self, expression: str) -> bool:
        """
            method 1 to check correctness of the math expression with balanced parentheses

            Parameters:
                expression (str): The math expression
        """

        current_state = 'q0'

        transition = {
            ('q0', '(', '$'): ['q1', '$('],
            ('q0', ')', '$'): ['qf', 'λ'],

            ('q1', '(', '$'): ['q1', '$('],
            ('q1', '(', '('): ['q1', '(('],
            ('q1', '(', ')'): ['q1', 'λ'],

            ('q1', ')', '$'): ['q1', '$)'],
            ('q1', ')', '('): ['q1', 'λ'],
            ('q1', ')', ')'): ['q1', '))'],

            ('q1', 'λ', '$'): ['qf', 'λ'],
        }

        pda = PushDownAutomata()
        return pda.is_accepted(expression, current_state, transition)

    def checker2(self, expression: str) -> bool:
        """
            method 2 to check correctness of the math expression with balanced parentheses

            Parameters:
                expression (str): The math expression
        """

        tokens = regex.search('^(\((?1)*\))(?1)*$', "".join([i for i in expression if i in "()"]))

        if tokens:
            return True

        return False

    def phase1(self, expression: str) -> Union[list, bool]:
        """
            Phase 1 method

            Parameters:
                expression (str): The math expression
        """

        if self.checker1(expression) or self.checker2(expression):
            return re.findall(r"(\b\w*[\.]?\w+\b|[\(\)\^\+\*\-\/])", expression)

        print("-" * 10 + " Wrong Math Expression " + "-" * 10 + "\n")
        print(f' >>> {expression}\n')
        return False

    def phase2(self, tokens: list) -> str:
        """
            Phase 2 method

            Parameters:
                tokens (list): The infix tokens list
        """

        return pda.to_postfix(tokens)

    def phase3(self, postfix_list: list) -> int:
        return pda.evaluate(pda.to_infix(postfix_list))


if __name__ == "__main__":
    main = Main()
    pda = PushDownAutomata()

    get_input = False

    # # Let's convert infix to postfix
    expressions = ['41*2+5*(2+1)/2', '2+5*(2+1)/2', 'A*(B+C)/D', '21*(32+12)']

    if get_input:
        inputer = ''
        while inputer.lower() != "exit":
            inputer = input("Please enter math expression (close: exit)\n > ").replace(" ", "")

            tokens = main.phase1(inputer)

            if not tokens:
                continue

            postfix = main.phase2(tokens)
            results = main.phase3(postfix.split(" "))

            print('expression >', inputer)
            print('Tokens >', tokens)
            print('postfix >', postfix)
            print('results >', results)
            print('\n' + "-" * 10 + "-" * 10 + "\n")

    else:
        for expression in expressions:
            tokens = main.phase1(expression)

            if not tokens:
                continue

            postfix = main.phase2(tokens)
            results = main.phase3(postfix.split(" "))

            print('expression >', expression)
            print('Tokens >', tokens)
            print('postfix >', postfix)
            print('results >', results)
            print('\n' + "-" * 10 + "-" * 10 + "\n")
