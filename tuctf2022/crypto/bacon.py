from pwn import *
import string

UP = string.ascii_uppercase[:26]
a = [0 for i in range(9)]

CONN = remote("chals.tuctf.com", 30002)

def get_dict(l, length=15):
    d = {}
    for i in range(26):
        p = remote("chals.tuctf.com", 30002)
        level(p,l, chr(ord("A")+i)*length)
        log.info("Getting " + chr(ord("A")+i))
        p.recvuntil(b"encrypted is ")
        e = p.readline()[:-1].decode()
        a = [e[j*5:j*5+5] for j in range(int(len(e)/5))]
        d[chr(ord("A")+i)] = a
        p.close()
    return d

def gen_length(length):
    s = UP[:length]
    return s

def get_pos(l, d):
    pos_dict = [0, 0]
    for i in range(2,18):
        pos = []
        p = remote("chals.tuctf.com", 30002)
        text = gen_length(i)
        level(p,l, text)
        log.info("Getting " + str(i))
        p.recvuntil(b"encrypted is ")
        e = p.readline()[:-1].decode()
        t = [e[j*5:j*5+5] for j in range(int(len(e)/5))]
        for j in range(len(text)):
            pos.append(t.index(d[text[j]][0]))
        pos_dict.append(pos)
        p.close()
    return pos_dict


def solveX(l, d, pos_dict):
    level(CONN,l)
    for i in range(50):
        CONN.recvuntil(b"Decrypt ")
        result = ""
        target = CONN.readline()[:-1].decode()
        log.info("Target: " + target)
        length = int(len(target)/5)
        for i in range(int(len(target)/5)):
            pos = pos_dict[length][i]
            for j in d.keys():
                if (d[j][0]==target[pos*5:pos*5+5]):
                    result+=j
        
        log.info("Decrypt: " + result)
        CONN.sendline(result.encode())

def solve(l, d):
    level(CONN,l)
    for i in range(50):
        CONN.recvuntil(b"Decrypt ")
        result = ""
        target = CONN.readline()[:-1].decode()
        log.info("Target: " + target)
        for i in range(int(len(target)/5)):
            for key in d.keys():
                sub = d[key]
                if(sub[i]==target[5*i:5*i+5]):
                    result += key

        log.info("Decrypt: " + result)
        CONN.sendline(result.encode())

def level(p, x, text="a"):
    p.sendlineafter(b"What level? ",str(x).encode())
    p.sendlineafter(b"Give me text:",text.encode())
for i in range(10):
    log.info("Level: " + str(i))
    if(i==7 or i==6 or i==9):
        d = get_dict(i,1)
        p_d = get_pos(i, d)
        solveX(i, d, p_d)
    else:
        d = get_dict(i,17)
        solve(i,d)

CONN.interactive()
