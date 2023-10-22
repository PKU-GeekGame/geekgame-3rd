.text
.code64
.global _start

_start:
	subq $32, %rsp    # buf = alloca(MAX_FLAG_LEN + 1)

	movq $548, %rax   # __NR_get_flag
	xorq %rdi, %rdi   # id = 0
	movq %rsp, %rsi   # buf = ..
	syscall

	movq $1, %rax     # __NR_write
	movq %rax, %rdi   # fd = STDOUT_FILENO
	movq %rsp, %rsi   # buf = ..
	movq $128, %rdx    # len = 128
	syscall

	ud2
