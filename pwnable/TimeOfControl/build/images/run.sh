#!/bin/sh
exec qemu-system-x86_64 \
     -m 64M \
     -kernel bzImage \
     -initrd rootfs.cpio \
     -append "console=ttyS0 loglevel=3 oops=panic panic=-1 nokaslr pti=off" \
     -no-reboot -nographic \
     -cpu qemu64 \
     -smp 1 \
     -monitor /dev/null \
     -net nic,model=virtio -net user