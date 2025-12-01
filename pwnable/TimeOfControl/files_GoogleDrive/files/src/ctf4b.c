#include <linux/module.h>
#include <linux/cdev.h>
#include <linux/fs.h>
#include <linux/uaccess.h>
#include <linux/errno.h>
#include <linux/device.h>
#include "ctf4b.h"

MODULE_LICENSE("GPL");
MODULE_AUTHOR("KuonRuri");
MODULE_DESCRIPTION("TimeOfControl: SECCON Beginners CTF 2025");

static int ctf4b_open(struct inode *inode, struct file *filp)
{
	return 0;
}

static int ctf4b_release(struct inode *inode, struct file *filp)
{
	return 0;
}

char global_msg[CTF4b_MSG_MAX_SIZE] = "Kernel Pwn is fun!";
long msg_offset = 0;

bool is_offset_valid(long offset) {
	if (offset >= 0 && offset + 0x100 < CTF4b_MSG_MAX_SIZE) {
		return true;
	}
	return false;
}

static long ctf4b_ioctl(struct file *filp, unsigned int cmd, unsigned long arg)
{
	struct ctf4b_request req;
	switch (cmd) {
		case CTF4b_IOCTL_READ:
			if (!is_offset_valid(msg_offset)) {
				return -EINVAL;
			}
			if (copy_from_user(&req, (struct ctf4b_request __user *)arg, sizeof(req))) {
				return -EFAULT;
			}
			if (copy_to_user((char __user *)req.buf, &global_msg[msg_offset], req.size)) {
				return -EFAULT;
			}
			msg_offset += req.size;
			break;
		case CTF4b_IOCTL_WRITE:
			if (!is_offset_valid(msg_offset)) {
				return -EINVAL;
			}
			if (copy_from_user(&req, (struct ctf4b_request __user *)arg, sizeof(req))) {
				return -EFAULT;
			}
			if (copy_from_user(&global_msg[msg_offset], (char __user *)req.buf, req.size)) {
				return -EFAULT;
			}
			msg_offset += req.size;
			break;
		case CTF4b_IOCTL_SEEK:
			msg_offset = (long)arg;
			if (!is_offset_valid(msg_offset)) {
				return -EINVAL;
			}
			break;
		default:
			return -EINVAL;
	}

	return 0;
}

static struct file_operations module_fops = {
	.owner = THIS_MODULE,
	.unlocked_ioctl = ctf4b_ioctl,
	.open = ctf4b_open,
	.release = ctf4b_release,
};

static dev_t dev_id;
static struct cdev c_dev;

static int __init ctf4b_init(void)
{
	if (alloc_chrdev_region(&dev_id, 0, 1, CTF4b_DEV_NAME) < 0) {
		pr_err("Failed to allocate character device region\n");
		return -1;
	}
	cdev_init(&c_dev, &module_fops);
	if (cdev_add(&c_dev, dev_id, 1) < 0) {
		pr_err("Failed to add character device\n");
		unregister_chrdev_region(dev_id, 1);
		return -1;
	}
	return 0;
}

static void __exit ctf4b_exit(void)
{
	cdev_del(&c_dev);
	unregister_chrdev_region(dev_id, 1);
}

module_init(ctf4b_init);
module_exit(ctf4b_exit);
