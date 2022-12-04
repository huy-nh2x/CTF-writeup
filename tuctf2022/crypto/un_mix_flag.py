import string

def un_mix(oneLetter,num):

    if(oneLetter.isupper()):
        word = ord(oneLetter)-MIN_CAPLETTER
        shift = ord(num)-MIN_CAPLETTER
        return upperFlag[(word - shift)%len(upperFlag)]
    if(oneLetter.islower()):
        word = ord(oneLetter)-MIN_LETTER
        shift = ord(num)-MIN_LETTER
        return lowerFlag[(word - shift)%len(upperFlag)]


p = "ZBTZBHZBIZBSBSEzcawBSEzyzuawac"
i = 0

upperFlag = string.ascii_uppercase[:26]
lowerFlag = string.ascii_lowercase[:26]
MIN_LETTER = ord("a")
MIN_CAPLETTER = ord("A")

numShift = "t"
un_mixed = ""

for count, alpha in enumerate(p):
    un_mixed += un_mix(alpha, numShift)


c="ACUACIACJACT_gjhd_gfgbhdhj"
print(c)
i=0
while(i<len(c)-1):
	b = ""
	h = ""
	if(c[i] in upperFlag):
		b += "{0:05b}".format((ord(c[i]) - ord("A")))
		b += "{0:05b}".format((ord(c[i+1]) - ord("A")))
		b += "{0:05b}".format((ord(c[i+2]) - ord("A")))
		i = i+3
		print(chr(int(b,2)),end="")
		continue
	elif(c[i] in lowerFlag):
		h += "{0:01x}".format(ord(c[i])-ord("a"))
		h += "{0:01x}".format(ord(c[i+1])-ord("a"))
		print(chr(int(h,16)),end="")
		i = i+2
		continue
	print(c[i],end="")
	i+=1

