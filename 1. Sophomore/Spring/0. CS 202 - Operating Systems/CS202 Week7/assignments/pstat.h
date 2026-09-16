#ifndef _PSTAT_H_
#define _PSTAT_H_

#include "param.h"

// What getpinfo() reports about every slot in the process table.
struct pstat {
  int inuse[NPROC];    // whether this slot is in use
  int pid[NPROC];      // the process's id
  int tickets[NPROC];  // how many tickets it holds
  int ticks[NPROC];    // how many timer ticks it has been scheduled for
};

#endif // _PSTAT_H_
