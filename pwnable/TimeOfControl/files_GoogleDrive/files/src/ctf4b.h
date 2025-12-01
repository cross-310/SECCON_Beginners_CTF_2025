#define CTF4b_IOCTL_SEEK 0x4b001
#define CTF4b_IOCTL_READ 0x4b010
#define CTF4b_IOCTL_WRITE 0x4b100
#define CTF4b_MSG_MAX_SIZE 0x1000
#define CTF4b_DEV_NAME "ctf4b"
#define uint8_t unsigned char

struct ctf4b_request {
	char* buf;
    uint8_t size;
};
