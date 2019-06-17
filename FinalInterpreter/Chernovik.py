from AST import *
from langParser import *


def aexp():
    return precedence(aexp_term(),
                      aexp_precedence_levels,
                      process_binop)


def aexp_term():
    return aexp_value() | aexp_group()


def aexp_group():
    return keyword('(') + Lazy(aexp) + keyword(')') ^ process_group


def aexp_value():
    return (num ^ (lambda i: IntAexp(i))) | \
           (id ^ (lambda v: VarAexp(v)))


### Старшинство операторов ###
# формирование триплета (оператор, лП, рП)
def process_binop(op):
    return lambda l, r: BinopAexp(op, l, r)

aexp_precedence_levels = [
    ['*', '/'],
    ['+', '-'],
]

def process_group(parsed):
    ((_, p), _) = parsed
    return p

# вернет конкатенацию наших парсеров
def any_operator_in_list(ops):
    op_parsers = [keyword(op) for op in ops]
    parser = reduce(lambda l, r: l | r, op_parsers)
    return parser

#Проходимся по каждому уровню старшинства операторов, нулевой уровень - все; далее - происходит комбинация
def precedence(value_parser, precedence_levels, combine):
    def op_parser(precedence_level):
        returnValue = any_operator_in_list(precedence_level) ^ combine
        print(returnValue)
        return returnValue
    parser = value_parser * op_parser(precedence_levels[0])
    for precedence_level in precedence_levels[1:]:
        parser = parser * op_parser(precedence_level)
    return parser