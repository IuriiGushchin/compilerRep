import lexer

RESERVED = 'RESERVED'
INT = 'INT'
ID = 'ID'

token_exprs = [
    (r'[ \n\t]+', None),                # One or more tabulation pointers
    (r'#[^\n]*', None),                 # Comments
    (r'\:=', RESERVED),                 # Reserved identifiers....
    (r'\(', RESERVED),
    (r'\)', RESERVED),
    (r';', RESERVED),
    (r'\+', RESERVED),
    (r'-', RESERVED),
    (r'\*', RESERVED),
    (r'/', RESERVED),
    (r'<=', RESERVED),
    (r'<', RESERVED),
    (r'>=', RESERVED),
    (r'>', RESERVED),
    (r'!=', RESERVED),
    (r'=', RESERVED),
    (r'and', RESERVED),
    (r'or', RESERVED),
    (r'not', RESERVED),
    (r'if', RESERVED),
    (r'then', RESERVED),
    (r'else', RESERVED),
    (r'while', RESERVED),
    (r'do', RESERVED),
    (r'end', RESERVED),                  # .... end of reserved identifiers
    (r'[0-9]+', INT),                    # Int
    (r'[A-Za-z][A-Za-z0-9_]*', ID),      # ID for tokens
]


def startLexing(characters):
    return lexer.lex(characters, token_exprs)
