#include <stdio.h>
#include <string.h>
int main(int argc, char **argv){
    char secret[16]; strcpy(secret, "TOPSECRET");
    long canary_like = 0xdeadbeef;
    char buf[128];
    strncpy(buf, argv[1], sizeof buf - 1); buf[sizeof buf-1]=0;
    printf(buf);            /* BUG: user string as the format */
    printf("\n(secret at %p, val at %p)\n", (void*)secret, (void*)&canary_like);
    return 0;
}
