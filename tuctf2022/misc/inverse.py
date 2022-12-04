from pwn import *

p = remote("chals.tuctf.com", 30100)

p.recvuntil(b"version ")

version = int(p.readline())

f = True
d = ""

log.info("Version: " + str(version))

def remove(string):
	return string.replace(" ", chr(ord(" ")-version))

def remove2(string):
	return string.replace("\n", "")

def r(text):
	global d
	text = remove2(text.decode())
	text = text.encode()
	a = [(text[len(text)-1-i]-version) for i in range(len(text))]
	a = ''.join([chr(i) if(i>0) else (chr(i+128)) for i in a])
	print("Origin: " + text.decode())
	print("Decoded: " + a)


def s(command):
	c = [(command[len(command)-1-i] + version) for i in range(len(command))]
	c = ''.join([chr(i) for i in c])
	p.sendline(c.encode())

r(p.recvuntil(b"> "))
s("cd secret".encode())
r(p.recvuntil(b"> "))
s("cat .flag.txt".encode())
r(p.recvuntil(b"> "))
p.interactive()
# TUCTF{my_5up3r_dup3r_53cr37_1337_5h3ll}