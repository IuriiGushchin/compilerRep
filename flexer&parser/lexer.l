
%{
    #include <string>
    #include <iostream>

    using namespace std;

    #define YYSTYPE string
    #include "pyparser.tab.h"
    %}

identifier      [_a-zA-Z][_a-zA-Z0-9]*
defined         "and"|"elif"|"global"|"or"|"assert"|"else"|"if"|"except"|"pass"|"break"|"print"|"exec"|"in"|"raise"|"continue"|"finally"|"is"|"return"|"for"|"lambda"|"try"|"del"|"not"|"while"
quote1          "\'"[^'\\]*"\'"
quote2          "\""[^"\\]*"\""

%%
\n\r|\r\n|\n|\r {
                    /* skip empty line */
                }
"#"             {
                    /* skip comment */
                }
{defined}       {
                    yylval = yytext;
                    return DEFINED;
                }
class           {
                    yylval = yytext;
                    return CLASS;
                }
def             {
                    yylval = yytext;
                    return DEF;
                }

":"             yylval = yytext; return COLON;
"."             yylval = yytext; return DOT;
","             yylval = yytext; return COMMA;
"("             yylval = yytext; return LBRACE;
")"             yylval = yytext; return RBRACE;
"*"             yylval = yytext; return STAR;

{identifier}    {
                    yylval = yytext;
                    return ID;
                }
{quote1}        {
                    yylval = yytext;
                    return MESSAGE;
                }
{quote2}        {
                    yylval = yytext;
                    return MESSAGE;
                }

[ \t]+          ; /* skip whitespaces */
.               {
                    yylval = yytext;
                    return OTHER;
                }
%%
