/* cs202ring.c — a Linux character device: the same ring buffer as the xv6 one, written
 * against the kernel's file_operations interface.
 *
 *   make                       builds cs202ring.ko against the running kernel's headers
 *   modinfo cs202ring.ko       what the module says about itself
 *   sudo insmod cs202ring.ko   — which you cannot do on the lab machines (PS 9 Q1)
 *
 * What is here: the module's skeleton, its init and exit, and the operations table.
 * What is yours: cs202ring_read and cs202ring_write, including the copies across the
 * user boundary, and the buffer they share.
 * CS 202 Week 9, PS 9. */
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/fs.h>
#include <linux/uaccess.h>
#include <linux/mutex.h>

#define RINGSIZE 512
#define DEVNAME  "cs202ring"

static int major;
static DEFINE_MUTEX(ring_lock);
static char ring[RINGSIZE];
static size_t head, tail;                 /* head: next write; tail: next read */

static ssize_t cs202ring_read(struct file *f, char __user *buf, size_t n, loff_t *off)
{
	/* TODO (Q1b): under ring_lock, copy up to n bytes out of the ring with
	 * copy_to_user(), and return how many were copied — or 0 if it is empty.
	 * Do not block: blocking correctly needs a wait queue, which is Q1(d). */
	(void)f; (void)buf; (void)n; (void)off;
	(void)ring; (void)head; (void)tail;
	return -EINVAL;
}

static ssize_t cs202ring_write(struct file *f, const char __user *buf, size_t n, loff_t *off)
{
	/* TODO (Q1b): under ring_lock, copy up to n bytes in with copy_from_user(),
	 * discarding what does not fit, and return how many were stored. */
	(void)f; (void)buf; (void)n; (void)off;
	return -EINVAL;
}

static const struct file_operations cs202ring_fops = {
	.owner = THIS_MODULE,
	.read  = cs202ring_read,
	.write = cs202ring_write,
};

static int __init cs202ring_init(void)
{
	major = register_chrdev(0, DEVNAME, &cs202ring_fops);
	if (major < 0) {
		pr_err("cs202ring: register_chrdev failed: %d\n", major);
		return major;
	}
	head = tail = 0;
	pr_info("cs202ring: loaded with major %d; mknod /dev/cs202ring c %d 0\n", major, major);
	return 0;
}

static void __exit cs202ring_exit(void)
{
	unregister_chrdev(major, DEVNAME);
	pr_info("cs202ring: unloaded\n");
}

module_init(cs202ring_init);
module_exit(cs202ring_exit);
MODULE_LICENSE("GPL");
MODULE_AUTHOR("CS 202");
MODULE_DESCRIPTION("A ring-buffer character device, for CS 202 Week 9");
