#include <stdlib.h>
#include <string.h>
int main(int argc,char**argv){
    char *p = malloc(32);
    strcpy(p, "hello");
    free(p);
    if(argc>1 && argv[1][0]=='u') return p[0];     /* use-after-free */
    if(argc>1 && argv[1][0]=='d') { free(p); return 0; }  /* double free */
    return 0;
}
