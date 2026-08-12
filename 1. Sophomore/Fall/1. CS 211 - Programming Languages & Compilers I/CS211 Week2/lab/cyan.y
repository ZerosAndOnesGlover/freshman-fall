%{
#include <stdio.h>
int yylex(void); void yyerror(const char *s){ fprintf(stderr,"%s\n",s); }
%}
%token IDENT INT STRING
%token FN LET IF ELSE WHILE RETURN STRUCT NEW TRUE FALSE
%token T_INT T_BOOL T_STRING
%token EQ NE LE GE ANDAND OROR ARROW
%%
program : /* empty */ | program decl ;

decl : fn_decl | struct_decl | let_stmt ;

fn_decl : FN IDENT '(' params ')' ARROW type block
        | FN IDENT '(' ')' ARROW type block
        | FN IDENT '(' params ')' block
        | FN IDENT '(' ')' block
        ;

struct_decl : STRUCT IDENT '{' fields '}' ;
fields : field | fields field ;
field  : IDENT ':' type ';' ;

params : param | params ',' param ;
param  : IDENT ':' type ;

type : T_INT | T_BOOL | T_STRING | IDENT
     | '[' type ']'
     | FN '(' typelist ')' ARROW type
     | FN '(' ')' ARROW type
     ;
typelist : type | typelist ',' type ;

block : '{' '}' | '{' stmts '}' ;
stmts : stmt | stmts stmt ;

stmt : let_stmt | assign_stmt | if_stmt | while_stmt | return_stmt | expr_stmt ;

let_stmt    : LET IDENT '=' expr ';' | LET IDENT ':' type '=' expr ';' ;
assign_stmt : lvalue '=' expr ';' ;
lvalue      : IDENT | lvalue '[' expr ']' | lvalue '.' IDENT ;
if_stmt     : IF expr block | IF expr block ELSE block | IF expr block ELSE if_stmt ;
while_stmt  : WHILE expr block ;
return_stmt : RETURN ';' | RETURN expr ';' ;
expr_stmt   : expr ';' ;

expr : or_e ;
or_e : or_e OROR and_e | and_e ;
and_e: and_e ANDAND cmp_e | cmp_e ;
cmp_e: add_e cmpop add_e | add_e ;
cmpop: EQ | NE | '<' | LE | '>' | GE ;
add_e: add_e '+' mul_e | add_e '-' mul_e | mul_e ;
mul_e: mul_e '*' un_e | mul_e '/' un_e | mul_e '%' un_e | un_e ;
un_e : '-' un_e | '!' un_e | post_e ;
post_e: prim | post_e '(' args ')' | post_e '(' ')'
      | post_e '[' expr ']' | post_e '.' IDENT ;
args : expr | args ',' expr ;
prim : INT | STRING | IDENT | TRUE | FALSE | '(' expr ')'
     | '[' args ']' | '[' ']'
     | NEW IDENT '{' inits '}' | NEW IDENT '{' '}'
     ;
inits: init | inits ',' init ;
init : IDENT ':' expr ;
%%
int main(void){ return 0; }
