import re

roman = {'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000,'IV':4,'IX':9,'XL':40,'XC':90,'CD':400,'CM':900}
eng_to_morse= {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
                    'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
                    'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
                    'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
                    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.'}

morse_to_eng = {}
for key, value in eng_to_morse.items():
    morse_to_eng[value] = key


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
	print(t)
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
	t = re.split(" ",text)
	print(text)
	print(t)
	a = []
	for i in range(len(t)):
		t[i] = t[i].replace("(","")
		if(len(t[i])!=5):
			a.insert(0,i)
	for i in a:
		del t[i]

	print(t)
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

# s = "(((((-7762071  + 72542 )  / 2773 )  + 64411 )  + 34982 )  - 96424 )"
# print(round(int(eval(s))))
