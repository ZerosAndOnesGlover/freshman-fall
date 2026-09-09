/* PROG 201 Project 2 -- REFERENCE DAEMON (do not distribute).
 * The complete production httpd the marking notes describe. Students build
 * their own from their Week 5-6 server; this is the instructor reference only.
 * Thread pool + accept loop; graceful drain on SIGTERM via a self-pipe;
 * SIGPIPE ignored so a client disconnect returns EPIPE instead of killing us.
 * Foreground (systemd-style), logs to stderr, unprivileged.
 * Warning-clean under:
 *   cc -Wall -Wextra -Werror -O2 -std=gnu11 -pthread \
 *      -fstack-protector-strong -D_FORTIFY_SOURCE=2 -o httpd httpd.c
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <errno.h>
#include <unistd.h>
#include <signal.h>
#include <pthread.h>
#include <time.h>
#include <fcntl.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <arpa/inet.h>
#include <poll.h>

#define BACKLOG 128
#define NWORKERS_DEFAULT 4
#define QCAP 256

static int listen_fd = -1;
static int stop_pipe[2];               /* self-pipe: SIGTERM handler writes */
static volatile sig_atomic_t draining = 0;

/* --- a tiny bounded connection queue, one lock+condvars --- */
static int q[QCAP]; static int qhead, qtail, qcount;
static pthread_mutex_t qlock = PTHREAD_MUTEX_INITIALIZER;
static pthread_cond_t  qnotempty = PTHREAD_COND_INITIALIZER;
static pthread_cond_t  qnotfull  = PTHREAD_COND_INITIALIZER;
static int shutting = 0;

static void q_push(int fd){
    pthread_mutex_lock(&qlock);
    while(qcount==QCAP && !shutting) pthread_cond_wait(&qnotfull,&qlock);
    if(shutting){ pthread_mutex_unlock(&qlock); close(fd); return; }
    q[qtail]=fd; qtail=(qtail+1)%QCAP; qcount++;
    pthread_cond_signal(&qnotempty);
    pthread_mutex_unlock(&qlock);
}
static int q_pop(void){
    pthread_mutex_lock(&qlock);
    while(qcount==0 && !shutting) pthread_cond_wait(&qnotempty,&qlock);
    if(qcount==0 && shutting){ pthread_mutex_unlock(&qlock); return -1; }
    int fd=q[qhead]; qhead=(qhead+1)%QCAP; qcount--;
    pthread_cond_signal(&qnotfull);
    pthread_mutex_unlock(&qlock);
    return fd;
}

static void on_term(int sig){ (void)sig; char c='x'; ssize_t n=write(stop_pipe[1],&c,1); (void)n; }

/* Serve one HTTP/1.0 request: read the request line, reply with a fixed body.
 * Returns after one request (HTTP/1.0, connection: close). */
static void serve(int cfd){
    char buf[4096]; ssize_t n = read(cfd, buf, sizeof buf - 1);
    if(n<=0){ close(cfd); return; }
    buf[n]=0;
    /* slow path marker: GET /slow sleeps to model an in-flight request */
    if(strncmp(buf,"GET /slow",9)==0) { struct timespec t={0,200*1000*1000}; nanosleep(&t,0); }
    const char *body = "hello\n";
    char resp[256];
    int rl = snprintf(resp,sizeof resp,
        "HTTP/1.0 200 OK\r\nContent-Length: %zu\r\nConnection: close\r\n\r\n%s",
        strlen(body), body);
    /* write() may hit EPIPE if the client vanished. Because we SIG_IGN SIGPIPE
     * in main, this returns -1/EPIPE instead of killing the process. */
    ssize_t w = write(cfd, resp, rl);
    if(w<0 && errno==EPIPE) fprintf(stderr,"[worker] client gone (EPIPE), handled\n");
    close(cfd);
}

static void *worker(void *a){ (void)a;
    for(;;){ int fd=q_pop(); if(fd<0) break; serve(fd); }
    return 0;
}

int main(int argc,char**argv){
    int port = argc>1?atoi(argv[1]):8080;
    int nw   = argc>2?atoi(argv[2]):NWORKERS_DEFAULT;

    signal(SIGPIPE, SIG_IGN);                    /* the key line -- see the lab */
    struct sigaction sa={0}; sa.sa_handler=on_term; sigemptyset(&sa.sa_mask);
    sigaction(SIGTERM,&sa,0); sigaction(SIGINT,&sa,0);
    if(pipe(stop_pipe)<0){perror("pipe");return 1;}

    listen_fd=socket(AF_INET,SOCK_STREAM,0);
    int one=1; setsockopt(listen_fd,SOL_SOCKET,SO_REUSEADDR,&one,sizeof one);
    struct sockaddr_in addr={0}; addr.sin_family=AF_INET; addr.sin_addr.s_addr=htonl(INADDR_LOOPBACK); addr.sin_port=htons(port);
    if(bind(listen_fd,(void*)&addr,sizeof addr)<0){ fprintf(stderr,"bind :%d: %s\n",port,strerror(errno)); return 1; }
    if(listen(listen_fd,BACKLOG)<0){perror("listen");return 1;}

    pthread_t th[64]; if(nw>64)nw=64;
    for(int i=0;i<nw;i++) pthread_create(&th[i],0,worker,0);
    fprintf(stderr,"[httpd] pid %d listening on 127.0.0.1:%d, %d workers\n",getpid(),port,nw);

    struct pollfd pf[2]={ {listen_fd,POLLIN,0}, {stop_pipe[0],POLLIN,0} };
    for(;;){
        int r=poll(pf,2,-1);
        if(r<0){ if(errno==EINTR) continue; perror("poll"); break; }
        if(pf[1].revents&POLLIN){                 /* SIGTERM arrived */
            fprintf(stderr,"[httpd] SIGTERM: draining\n"); draining=1; break;
        }
        if(pf[0].revents&POLLIN){
            int cfd=accept(listen_fd,0,0);
            if(cfd<0){ if(errno==EINTR||errno==ECONNABORTED) continue; perror("accept"); continue; }
            q_push(cfd);
        }
    }
    /* graceful shutdown: stop accepting, let workers drain the queue, join */
    close(listen_fd);
    pthread_mutex_lock(&qlock); shutting=1;
    pthread_cond_broadcast(&qnotempty); pthread_cond_broadcast(&qnotfull);
    pthread_mutex_unlock(&qlock);
    for(int i=0;i<nw;i++) pthread_join(th[i],0);
    fprintf(stderr,"[httpd] drained and exiting 0\n");
    return 0;
}
