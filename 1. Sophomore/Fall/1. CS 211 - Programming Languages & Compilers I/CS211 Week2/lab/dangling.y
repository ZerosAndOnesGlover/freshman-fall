%{
#include <stdio.h>
int yylex(void); void yyerror(const char*s){fprintf(stderr,"%s\n",s);}
%}
%token IF E S ELSE
%%
stmt : IF E stmt
     | IF E stmt ELSE stmt
     | S
     ;
%%
int main(void){return 0;}
