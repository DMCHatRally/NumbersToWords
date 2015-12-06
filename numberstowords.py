###==PROGRAM DESIGNED AND WRITTEN BY DMITRIY CHERNOSHEY================================####
# You may use, modify and copy this program, however, please keep this header intact
# Suggestions welcome. 


""" This program takes an input string up to 3000 numerical characters long and creates a verbal
    representation/translation of that number in English, implementing Latin convention generator for 
    formation for numbers larger than base 21. The idea is to handle each large number
    by breaking it up in triplets because between words 'thousand', 'million' etc. the same word
    structure repeats in English. Each triplet can be represented as 'number of hundreds' plus 
    whatever tens and singles there are. The tens and singles portion is handled separately
    because we have special cases of singles, teens and numbers indicating tens like 'twenty' or
    'fifty'. The user input is analyzed and routed by the parser function to appropriate
    functions. If input is larger than 999, it is converted into an list of lists where each
    element represents an order of a thousand. The element is converted into input for appropriate
    functions. The output is also placed in a list. Final word list is modified and filtered to look
    similar to a sentence.""" 

import sys
dict_1019={10:'ten', 11:'eleven', 12:'twelve', 13:'thirteen', 14:'fourteen', 15:'fifteen',
			16:'sixteen', 17:'seventeen', 18:'eighteen', 19:'nineteen'}

dict_ones= {0:'',1: 'one', 2:'two', 3:'three', 4:'four', 5:'five', 6:'six', 7:'seven', 
			8:'eight', 9:'nine'}

dict_tens={2:'twenty', 3:'thirty', 4:'fourty', 5:'fifty', 6:'sixty', 7:'seventy',
			8:'eighty', 9:'ninety'}
	
bigNumbs=[' ','thousand','million','billion','trillion','quadrillion','quintillion','sextillion',
				'septillion','octillion','nonillion','decillion','undecillion','duodecillion',
				'tredecillion','quattuordecillion','quindecillion','sexdecillion','septendecillion',
				'octodecillion','novemdecillion','vigintillion']

arrunits =['','un','duo','tre','quattuor','quinqua','se','septe','octo','nove']
arrtens = ['','deci','viginti','triginta','quadraginta','quinquaginta','sexaginta','septuaginta',
		'octoginta','nonaginta']
arrhundreds = ['','centi','ducenti','trecenti','quadringenti','quingenti','sescenti','septingenti',
				'octingenti','nongenti']
M=['viginti','octoginta', 'octingenti']
N=['deci','triginta','quadraginta','quinquaginta','sexaginta','septuaginta','centi','ducenti',
	'trecenti','quadringenti','quingenti','sescenti','septingenti']
S=['viginti','triginta','quadraginta', 'quinquaginta', 'trecenti','quadringenti','quingenti']
X=['octoginta','centi','octingenti']


#==================================LATIN CONVERSION ENGINE===============================

def fixLatNum(list_arg):
	incoming=list_arg
	modified=[]

	for i in range(0,len(incoming)): #deleting empty spaces
		if incoming[i]=='':
			pass
		else:
			modified.append(incoming[i])

	incoming=modified

	for i in range(0,len(incoming)-1): #correcting list components to comply with formation model
		if incoming[i]=='tre' and (incoming[i+1] in S or X):
			incoming[i]='tres'
			
		if incoming[i]== 'se' and (incoming[i+1] in S or X):
			incoming[i]= 'ses'
			
		if incoming[i]=='septe' and (incoming[i+1] in M or N):
			incoming[i]='septem'
			
		if incoming[i]== 'nove' and (incoming[i+1] in M or N):
			incoming[i]= 'noven'

		
	if incoming[-2].endswith(('i','a','e','o')): #removing vowels before '-illion'
		tempLst=list(incoming[-2])
		del tempLst[-1]
		incoming[-2]=''.join(tempLst)
		
	return incoming


def latNum(number):
	base=0
	if number<=21:
		return bigNumbs[number]
	elif number>21:
		base =number-1
		numberStr=str(base)
		if len(numberStr)<3:
			numberStr='0'+numberStr
		containerLst=[arrunits[int(numberStr[2])],arrtens[int(numberStr[1])],arrhundreds[int(numberStr[0])],'illion']
		newList= fixLatNum(containerLst)
		word=''.join(newList)
		return word

#=============================END LATIN CONVERSION=======================================		

def firstHundred(numb): #controls conversion for input from 0 to 99 for 2digit args only  
	numbStr=str(numb)   # 
	if numbStr[0]=='0':  #checks if tens equals 0 if so returns units
		return dict_ones[int(numbStr[1])]
	elif 10<=int(numb)<=19: # then checks if the whole thing belongs to duodecimals 
		return dict_1019[int(numb)]
	elif numbStr[1]!='0':     #tens is not zero at this point, checking if units equals 0
		return dict_tens[int(numbStr[0])]+' '+dict_ones[int(numbStr[1])]  #returns both translated
	else:                # the only case logically left over is tens not zero and ones are zero
		return dict_tens[int(numbStr[0])]

def firstThousand(numb): #controls creation 3 digit numbers from 100 to 999
	
	numbLst=list(str(numb))
	hundredtxt=firstHundred(numbLst[1]+numbLst[2])
	if (numbLst[1]+numbLst[2])=='00':
		return dict_ones[int(numbLst[0])]+' hundred'
	else:
		return dict_ones[int(numbLst[0])]+' hundred and '+hundredtxt  #fhundred(int(numbLst[0]))+hundredtxt

"""1 hundred and 65 million 5 hundred and 15 thousand 4 hundred and 12""" #that's the idea here	

def aThousand(numArg):  #controls conversion of inputs from 0 to 999. Calls other functions. 
	inputNum=int(numArg) #Also converts triples in large numbers into words
	if len(numArg)>1 and inputNum==0: #string passed has more than 1 character and when converted
		return ''                     # to number evaluates to zero, which means all characters
	elif numArg=='0':                 # are zeroes.
		return('Zero')
	elif 0<inputNum<10:
		return(dict_ones[inputNum])
	elif inputNum<100:
		return(firstHundred(inputNum))
	elif inputNum<1000:
		return(firstThousand(inputNum))
	else:
		pass

def parser(num_arg): # 
	if int(num_arg)<1000:
		print('\nTRANSLATION: \n' , aThousand(num_arg).capitalize())
	else:
		strArr=list(num_arg)  #converts to string and makes a list
		strArr.reverse()   #the list is reversed for incremental processing
		
		grouped=[]         #this will hold the array of triples
		for i in range(0, len(strArr),3):  #creates array of triples
			subArr=[]                      #holds each triple and empties with each iteration
			for j in range(0,3):
				if i<len(strArr):
					subArr.append(strArr[i])
					i+=1
			
			grouped.append(subArr)

		words=[]
		counter=0
		andFlag=int(''.join(reversed(grouped[0]))) # this extracts the last 3 digits to determine if insertion 
		                                           # of 'and' is necessary

		for eachEl in grouped:
			
			eachEl.reverse()
			block = "".join(eachEl)
			if block=='000':
				wBlock=''
			elif counter<1000: #len(bigNumbs):
				wBlock = aThousand(block)+' '+latNum(counter)+' '
			words.append(wBlock)
			counter+=1
		
		if 0<andFlag<100:            #inserting and before last subarray in words array. Takes care of cases such as
			words.insert(1,'and ') # 'one thousand AND fifty one'

		words.reverse()
		

		answerLst=(' '.join(words)).split() #cleaning up the text from extra spaces
		answer=' '.join(answerLst).capitalize()
		print('\nTRANSLATION: \n', answer)

def chkUsrInp(userInp):
	if len(userInp)>3000:
		print('A MESSAGE FROM PROGRAM AUTHOR:\n "I see you love very large numbers...\n', \
			'Your number was {0} digits long and cannot be translated at this time.\n'.format(str(len(userInp))), \
			'Please enter up to 3000 digits\n Faithfully yours,', \
			'DMITRIY CHERNOSHEY"')

	else:
		flag=0
		for ch in userInp:
			if ch not in ('0123456789'):
				flag=1
		if flag==1:
			print("Please enter only numbers without spaces")
		else:
			parser(userInp)
			if len(userInp)>15:
				print('\nYou entered {0} digits'.format(str(len(userInp))))



def main():    #controls user interface and checks input for non-digits and proper length
	if len(sys.argv)==1:  #this means only the filename is in the sys.argv list
		print('\n=============================================================\n')
		userInp = input('ENTER A NUMBER UP TO 3000 DIGITS: ')
	else:
		userInp = sys.argv[1]

	chkUsrInp(userInp)

if __name__=='__main__':
	main()