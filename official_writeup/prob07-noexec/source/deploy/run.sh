#!/bin/bash

set -e

cd $(dirname $0)

echo 'Welcome to PKU GeekGame!'
echo 'Available levels:'
echo ' 1) Easy (Flag 1)'
echo ' 2) Hard (Flag 2/3)'
echo -n 'Enter your choice: ' && read LV

case $LV in
	1) INITRAMFS=easy.cpio.gz
	   CMDLINE="flag1=$(cat flag1.txt) flag2=no_flag_here"
	   ;;
	2) INITRAMFS=hard.cpio.gz
	   CMDLINE="flag1=$(cat flag2.txt) flag2=$(cat flag3.txt)"
	   ;;
	*) echo 'Bad choice, goodbye!'
	   exit 1
	   ;;
esac

if [[ -f ./anticheat ]]; then
	. ./anticheat
fi

qemu() {
	exec qemu-system-x86_64 \
		-kernel bzImage \
		-initrd $INITRAMFS \
		-append "console=ttyS0 quiet $CMDLINE" \
		-m 512M \
		-nographic \
		-serial tcp::4444,server \
		</dev/null >/dev/null 2>/dev/null
}

qemu &

sleep 0.2
nc -N localhost 4444

kill $! || true
wait || true

echo 'See you later!'
