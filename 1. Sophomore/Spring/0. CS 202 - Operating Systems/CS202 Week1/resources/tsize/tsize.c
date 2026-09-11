// Compiled against this machine's kernel headers, never loaded: the sizes of
// the kernel's own structures, read back from the object file's symbol table.
#include <linux/module.h>
#include <linux/sched.h>
#include <linux/mm_types.h>
#include <linux/fs.h>
#include <linux/cred.h>
#include <linux/fdtable.h>
char task_struct_size[sizeof(struct task_struct)];
char mm_struct_size[sizeof(struct mm_struct)];
char files_struct_size[sizeof(struct files_struct)];
char cred_size[sizeof(struct cred)];
char thread_struct_size[sizeof(struct thread_struct)];
MODULE_LICENSE("GPL");
