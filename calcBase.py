from lark import Lark, Transformer, v_args


calc_grammar = """
    ?start: sum
          | NAME "=" sum    -> assign_var

          

    ?sum: product
        | sum "+" product   -> add
        | sum "-" product   -> sub

    ?product: atom
        | product "*" atom  -> mul
        | product "/" atom  -> div

    ?atom: NUMBER           -> number
         | "-" atom         -> neg
         | NAME             -> var
         | "(" sum ")"
         | "mid" "(" atom "," atom ")" -> mid_expr


    %import common.CNAME -> NAME
    %import common.NUMBER
    %import common.WS_INLINE

    %ignore WS_INLINE
"""


@v_args(inline=True)    # Affects the signatures of the methods
class CalculateTree(Transformer):
    from operator import add, sub, mul, truediv as div, neg
    number = float

    def __init__(self):
        self.vars = {}

    def assign_var(self, name, value):
        self.vars[name] = value
        return value

    def var(self, name):
        try:
            return self.vars[name]
        except KeyError:
            raise Exception("Variable not found: %s" % name)

    def mid_expr(self, val1, val2):
        return (int(val1) + int(val2)) * 0.5

calc_parser = Lark(calc_grammar, parser='lalr', transformer=CalculateTree())
calc = calc_parser.parse


def main():
    while True:
        try:
            s = input('> ')
        except EOFError:
            break
        print(calc(s))


def test():
    print(calc("bidspot = 99"))
    print(calc("spreadspot = 2"))
    print(calc("askspot = spreadspot + bidspot"))
    print(calc("midspot = mid(bidspot,askspot)"))

    print(calc("bidfut = 101"))
    print(calc("spreadfut = 1"))
    print(calc("askfut = spreadfut + bidfut"))
    print(calc("midfut = mid(bidfut,askfut)"))

    print(calc("base = midfut- midspot"))




if __name__ == '__main__':
    test()
