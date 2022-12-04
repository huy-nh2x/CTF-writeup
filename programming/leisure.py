from pwn import *
import re

p = remote("chals.tuctf.com", 30202)

pattern = re.compile("[a-zA-Z]")

while True:
	s = p.readline().decode()
	if(pattern.match(s)):
		print(s)
		continue
	print(s)
	print(eval(s))
	p.sendline(str(int(eval(s))).encode())
	p.recvuntil(b"Answer")
	print(p.readline().decode())
p.interactive()