import random
import argparse
import math

charset_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
charset_capitals = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
charset_numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
charset_special = ['!', '@', '#', '$', '%', '^', '&', '*', '-', '_', '+', '-', '?']

MANGLE_CHANCE = (1/10)
PREPEND_CHANCE = (1/20)
APPEND_CHANCE = (1/5)


LENGTH_MINIMUM = 11
LENGTH_MAXIMUM = 16
APPEND_MAXIMUM = 5
PREPEND_MAXIMUM = 3

CHARSET_BONUS = 0.2
CHARSET_PENALTY = 0.2

MINIMUM_SCORE = 3.2
PEAK_SCORE = 4.0



def readDictionary(dFileName):
	try:
		dFile = open(dFileName, 'r')
	except:
		print("Failed to open " + dFileName)
		return (None, None)

	
	try:
		fullDict = [line.strip() for line in dFile]
	except:
		print("Failed to load dictionary.")
		return (None, None)
	fDictCount = len(fullDict)
	
	return (fullDict, fDictCount)



def generateRandomString(length, charset):
	setLen = len(charset)
	string = ""

	for i in range(length):
		index = random.randint(0, setLen-1)
		string += charset[index]	

	return string	


def getRandomWord(wordDict, wordDictCount):
	word = random.randint(0, wordDictCount-1)
	return wordDict[word]


def getShannonEntropy(string):
	ent = 0.0
	
	symbols = {}
	for char in string:
		if not char in symbols:
			symbols[char] = 1
		else:
			symbols[char] += 1	

	count = len(symbols)
	for symbol in symbols:
		freq = symbols[symbol] / count
		ent = ent + freq * math.log(freq, 2)
	ent = -ent

	return ent


def scorePassword(password):
	score = getShannonEntropy(password)

	if not set(password).isdisjoint(charset_numbers):
		score += CHARSET_BONUS
	else:
		score -= CHARSET_PENALTY
	if not set(password).isdisjoint(charset_special):
		score += CHARSET_BONUS
	else:
		score -= CHARSET_PENALTY
	if not set(password).isdisjoint(charset_capitals):
		score += CHARSET_BONUS
	else:
		score -= CHARSET_PENALTY

	return score


def mangleString(string, charset):
	mangle_cap = int(len(string) * MANGLE_CHANCE) + 1
	mangled = 0

	for i in range(len(string)):
		if(mangled < mangle_cap and random.randint(0, (1/MANGLE_CHANCE)) == 0):
			string = list(string)
			string[i] = charset[random.randint(0, len(charset)-1)]
			mangled += 1


	return "".join(string)
		


def generatePassword(wordDict, wordDictCount):
	score = 0
	password = ""

	while score < MINIMUM_SCORE:
		wordCount = random.randint(1, 3)	
		if wordCount < 0:
			wordCount = 1
	
		charset = charset_letters + charset_capitals + charset_numbers + charset_special

		for word in range(wordCount):
			password += getRandomWord(wordDict, wordDictCount)
			app = random.randint(0, (1/PREPEND_CHANCE))
			if app == 0 or (word == wordCount-1 and wordCount < 3):
				password += generateRandomString(random.randint(1, PREPEND_MAXIMUM), charset)

		if len(password) < LENGTH_MINIMUM or random.randint(0, (1/APPEND_CHANCE)) == 0:
			if len(password) < LENGTH_MINIMUM:
				password += generateRandomString(random.randint(LENGTH_MINIMUM - len(password), LENGTH_MAXIMUM - len(password)), charset)
			else:
				password += generateRandomString(random.randint(1, APPEND_MAXIMUM), charset)

		password = mangleString(password, charset_numbers + charset_special)

		score = scorePassword(password)

	if score > PEAK_SCORE:
		score = 4
	else:
		score = 3

	return password, score


def main():
	argparser = argparse.ArgumentParser(description='Generates secure passwords')
	argparser.add_argument('--count', '-c', type=int,
	                   help='The number of passwords to generate', default=1)
	argparser.add_argument('--dict', '-d', type=str, required=True, help='The dictionary file to use')

	prog_args = argparser.parse_args()

	wordDict, wordDictCount = readDictionary(prog_args.dict)
	if wordDict == None or wordDictCount == None:
		return 1

	for i in range(prog_args.count):
		p, score = generatePassword(wordDict, wordDictCount)
		print(p + "," + str(score) )

	return 0


if __name__=='__main__':
	main()
