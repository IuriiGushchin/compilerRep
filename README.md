# compilerRep
compiler with python
vi kto takie, ya vas ne zval, eto moi repositoriy


command to use Flex&Bison for creating lexer.l file : 

```bash
% bison -d pyparser.y --verbose && flex lexer.l && g++ -c lex.yy.c pyparser.tab.c && g++ -o parser lex.yy.o pyparser.tab.o -ll -ly
```
