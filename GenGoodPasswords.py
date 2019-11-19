import random
import sys

charset_numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
charset_special = ['!', '@', '#', '$', '%', '^', '&', '*', '-', '_', '+', '-', '?', '.']


def load_words():
    with open('top.txt') as f:
        words = f.read().split()    
    return words


if __name__ == "__main__":
    if(len(sys.argv) != 2):
        sys.exit(1)

    try:
        score = int(sys.argv[1])
        if score < 2 or score > 4:
            sys.exit(1)
    except:
        sys.exit(1)

    words = load_words()    
    word_space = len(words)-1

    charset = charset_numbers
    joinStr = ''

    wordlen = score
    charlen = 1 + score

    if(score > 2):
        charset += charset_special

    for _ in range(100000):
        if score > 3:
            joinStr = charset[random.randint(0,len(charset)-1)]
        print(
            joinStr.join([words[random.randint(0,word_space)].title() for _ in range(wordlen)]) +
            ''.join([charset[random.randint(0,len(charset)-1)] for _ in range(charlen)]) + "," + str(score)
        )
