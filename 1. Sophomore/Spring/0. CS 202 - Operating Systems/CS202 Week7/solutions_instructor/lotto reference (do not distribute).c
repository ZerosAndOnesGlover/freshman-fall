#include "types.h"
#include "stat.h"
#include "user.h"
#include "pstat.h"

// lotto.c — three children with 1, 2 and 4 tickets spin until they are killed; the
// parent samples the process table after a fixed interval and reports how often the
// scheduler chose each of them.
//   lotto [TICKS]        (default 300 timer ticks = about 3 seconds)
// CS 202 Project 1 reference.
int
main(int argc, char *argv[])
{
  int tickets[3] = {1, 2, 4};
  int pids[3];
  int i, j, total = 0;
  struct pstat ps;
  int window = argc > 1 ? atoi(argv[1]) : 300;

  for(i = 0; i < 3; i++){
    int pid = fork();
    if(pid < 0){
      printf(1, "fork failed\n");
      exit();
    }
    if(pid == 0){
      settickets(tickets[i]);
      volatile int x = 0;
      for(;;)
        x = x + 1;
    }
    pids[i] = pid;
  }

  sleep(window);
  if(getpinfo(&ps) < 0){
    printf(1, "getpinfo failed\n");
    exit();
  }
  for(i = 0; i < NPROC; i++)
    if(ps.inuse[i])
      for(j = 0; j < 3; j++)
        if(ps.pid[i] == pids[j])
          total += ps.ticks[i];
  for(i = 0; i < NPROC; i++)
    if(ps.inuse[i])
      for(j = 0; j < 3; j++)
        if(ps.pid[i] == pids[j])
          printf(1, "tickets %d: chosen %d times, %d%% of %d\n",
                 ps.tickets[i], ps.ticks[i], total ? ps.ticks[i] * 100 / total : 0, total);
  for(i = 0; i < 3; i++)
    kill(pids[i]);
  for(i = 0; i < 3; i++)
    wait();
  printf(1, "settickets(0) returns %d\n", settickets(0));
  exit();
}
