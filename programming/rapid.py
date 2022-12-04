from pwn import *
import re
from word2number import w2n

p = remote("chals.tuctf.com", 30200)

pattern = re.compile("[a-zA-Z]")

p.sendline(b"2500")
p.recvuntil(b"Answer: ")

roman = {'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000,'IV':4,'IX':9,'XL':40,'XC':90,'CD':400,'CM':900}
eng_to_morse= {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
                    'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
                    'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
                    'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
                    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.'}

morse_to_eng = {}
for key, value in eng_to_morse.items():
    morse_to_eng[value] = key

def convert(text):
    text = text.replace("minus","-")
    text = text.replace("plus","+")
    text = text.replace("divided by","/")
    text = text.replace("multiply", "*")
    text = text.replace(",","")
    text = text.replace("  "," ) ")
    text = text.replace("negative "," - ")
    return text


def ion(text):
    result = 0
    sub = []
    sub1 = []
    sub2 = []

    if("quintillion" in text):
        sub = text.split("quintillion")
        result += w2n.word_to_num(sub[0]) * (10**18)

    if("quadrillion" in text):
        if(sub==[]):
            sub1 = text.split("quadrillion")
        else:
            sub1 = sub[1].split("quadrillion")
        result += w2n.word_to_num(sub1[0]) * (10**15)

    if("trillion" in text):
        if (sub1 == []):
            if (sub == []):
                sub2 = text.split("trillion")
            else:
                sub2 = sub[1].split("")
        else:
            sub2 = sub1[1].split("trillion")
        print(sub)
        result += w2n.word_to_num(sub2[0]) * (10**12)

    if(sub2==[]):
        result += w2n.word_to_num(text) 
    else:
        result += w2n.word_to_num(sub2[1])
    return result

def w_2_n(text):
	tmp = text
	log.info("Origin: " + text)
	text = convert(text)
	t = re.split(r"[+\*\/\.]| -", text)
	log.info("After: " + text)
	print(t)
	count = 0
	for i in t:
		n  = 0
		first = 0
		if("ion" in i):
		        first = ion(i)
		if(i==''):
			continue
		try:
			n = w2n.word_to_num(i)
		except:
			log.info("Error: " + i)

		if (first!=0):
			n = first
		if(")" in i):
			text = text.replace(i, str(n)+")", 1)
			count+=1
		else:
			text = text.replace(i, str(n), 1)
	text = count*"(" + text
	if(re.findall(r"[a-z]",text)):
		return w_2_n(tmp)
	return text

def romanToInt(s):
   i = 0
   num = 0
   while i < len(s):
      if i+1<len(s) and s[i:i+2] in roman:
         num+=roman[s[i:i+2]]
         i+=2
      else:
         num+=roman[s[i]]
         i+=1
   return num

def r_2_n(text):
	t = re.split(" ",text)
	a = []
	for i in range(len(t)):
		t[i] = t[i].replace("(","")
		t[i] = t[i].replace(")","")
		t[i] = t[i].replace("-","")
		if(not re.match(r"[A-Z]",t[i])):
			a.insert(0,i)
	for i in a:
		del t[i]
	for i in t:
		text = text.replace(i,str(romanToInt(i)),1)
	return text


def morse_to_english(message):
    message = message.split(" ")
    english = []  # Will contain English versions of letters
    for code in message:
        if code in morse_to_eng:
            english.append(morse_to_eng[code])
    return "".join(english)

def m_2_n(text):
	log.info("TEXT: " + text)
	t = re.split(" ",text)
	a = []
	for i in range(len(t)):
		t[i] = t[i].replace("(","")
		if(len(t[i])!=5):
			a.insert(0,i)
	for i in a:
		del t[i]
	for i in t:
		text = text.replace(i, str(morse_to_english(i)),1)
	return text.replace(" ","")


def i_2_n(text):
	text = text.replace("=","-")
	t = []
	for i in range(int(len(text)/7)+1):
		t.append(text[7*i:7*i+7].replace(" ",""))
	num = [i[0] for i in t]
	return ''.join(num)


while True:
	s = p.readline().decode()
	if("everything" in  s):
		p.interactive()
		print(p.clean().decode())
	tmp = s
	if "Answer" in s:
		s = s[8:]
	if("exec" in s):
		p.readline()
		continue
	if(re.findall(r"[a-z]",s)):
		s = w_2_n(s)
	elif(re.findall(r"[A-Z]",s)):
		s = r_2_n(s)
	elif(re.findall(r"\.",s)):
		s = m_2_n(s)
	elif(s.startswith("\n")):
		p.readline()
		p.readline()
		s = p.readline().decode()
		p.readline()
		p.readline()
		s = i_2_n(s)
		log.info("Calc: " + s)
	try:
		result = round(eval(s))
	except:
		print("Cannot eval: " + tmp)
		continue
	log.info("R: " + str(result))
	p.sendline(str(result).encode())
	
	p.recvuntil("orr")
	
	print("Read: "  + p.readline().decode())
p.interactive()