#! /usr/bin/env python
# -*- coding: utf-8 -*-
from functools import reduce
from langLexer import *
from AST import *
from combinator import *

# поиск ключевого слова в ресервд словах
def keyword(kw):
    return Reserved(kw, RESERVED)

#Достать тупл, где первое значение - первый элемент из pos'того элемента из массива tokens, а вротой - pos+1
id = Tag(ID)

# достать инт по подобию ID и применить к нему функцию по переводу значение в инт. что будет с pos - пока хуй знает
num = Tag(INT) ^ (lambda i: int(i))

# Арифметика

# создать значение AST, которое будет арифметическим числом или значением
# оператор | - alternate для parser позволяет нам искать сначала цифры, а потом имена переменных
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


#Логика
#составляем выражение из парсеров
def process_relop(parsed):
    ((left, op), right) = parsed
    return RelopBexp(op, left, right)
#обертка для process_relop
def bexp_relop():
    relops = ['<', '<=', '>', '>=', '=', '!=']
    return aexp() + any_operator_in_list(relops) + aexp() ^ process_relop
# логическое НЕ
def bexp_not():
    return keyword('not') + Lazy(bexp_term) ^ (lambda parsed: NotBexp(parsed[1]))
# Группировка
def bexp_group():
    return keyword('(') + Lazy(bexp) + keyword(')') ^ process_group

#примитив: либо отрицание, либо сравнение, либо булево выражение
def bexp_term():
    return bexp_not()   | \
           bexp_relop() | \
           bexp_group()

bexp_precedence_levels = [
    ['and'],
    ['or'],
]

def process_logic(op):
    if op == 'and':
        return lambda l, r: AndBexp(l, r)
    elif op == 'or':
        return lambda l, r: OrBexp(l, r)
    else:
        raise RuntimeError('unknown logic operator: ' + op)

def bexp():
    return precedence(bexp_term(),
                      bexp_precedence_levels,
                      process_logic)





#Утверждения
#Объявление переменной
def assign_stmt():
    def process(parsed):
        ((name, _), exp) = parsed
        return AssignStatement(name, exp)
    return id + keyword(':=') + aexp() ^ process

def stmt_list():
    separator = keyword(';') ^ (lambda x: lambda l, r: CompoundStatement(l, r))
    return Exp(stmt(), separator)


# построение комбинатора для оператора условия
def if_stmt():
    def process(parsed):
        (((((_, condition), _), true_stmt), false_parsed), _) = parsed
        if false_parsed:
            (_, false_stmt) = false_parsed
        else:
            false_stmt = None
        return IfStatement(condition, true_stmt, false_stmt)

    return keyword('if') + bexp() + \
           keyword('then') + Lazy(stmt_list) + \
           Opt(keyword('else') + Lazy(stmt_list)) + \
           keyword('end') ^ process

#Построение комбинатора для цикла While
def while_stmt():
    def process(parsed):
        ((((_, condition), _), body), _) = parsed
        return WhileStatement(condition, body)
    return keyword('while') + bexp() + \
           keyword('do') + Lazy(stmt_list) + \
           keyword('end') ^ process

#Сами нпепосредственно утверждения
def stmt():
    return assign_stmt() | \
           if_stmt()     | \
           while_stmt()




#общая обертка

def parser():
    return Phrase(stmt_list())

def imp_parse(tokens):
    ast = parser()(tokens, 0)
    return ast

#универсальное решение для логики арифметики и утверждений:


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
        print(returnValue.parser)
        return returnValue
    parser = value_parser * op_parser(precedence_levels[0])
    print(parser)
    for precedence_level in precedence_levels[1:]:
        parser = parser * op_parser(precedence_level)
        print(parser)
    return parser