/* PROG 201 Week 12 -- the rude client. Connects, sends a request, and then
 * closes the connection HARD (RST via SO_LINGER 0) or soft (FIN via close),
 * so the server's subsequent write() has a broken pipe to write into.
 * Use it to test that your server survives a client that hangs up mid-response
 * (Project 2, Part 2 -- the SIGPIPE pair).
 *
 *   rudeclient PORT [rst|fin]        (default: fin -- graceful close)
 *
 * Build: make        (warning-clean under -Wall -Wextra)
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>

int main(int argc, char **argv)
{
    if (argc < 2) { fprintf(stderr, "usage: %s PORT [rst|fin]\n", argv[0]); return 2; }
    int port = atoi(argv[1]);
    int rst  = (argc > 2 && strcmp(argv[2], "rst") == 0);

    int fd = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in s = {0};
    s.sin_family = AF_INET; s.sin_addr.s_addr = htonl(INADDR_LOOPBACK); s.sin_port = htons(port);
    if (connect(fd, (void *)&s, sizeof s) < 0) { perror("connect"); return 1; }

    const char *req = "GET / HTTP/1.0\r\n\r\n";
    if (write(fd, req, strlen(req)) < 0) perror("write");

    if (rst) {                                  /* abrupt: RST on close -> ECONNRESET on server write */
        struct linger lg = {1, 0};
        setsockopt(fd, SOL_SOCKET, SO_LINGER, &lg, sizeof lg);
        printf("[rude] sent request, RST-closing\n");
    } else {                                    /* graceful: FIN, then a later server write -> SIGPIPE/EPIPE */
        printf("[rude] sent request, FIN-closing\n");
    }
    close(fd);
    return 0;
}
