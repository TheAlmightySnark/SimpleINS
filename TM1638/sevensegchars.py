#constants used to display characters on a seven segment LCD display

numbers = {
'1': '01100000',
'2': '11011010',
'3': '11110010',
'4': '01100110',
'5': '10110110',
'6': '10111110',
'7': '11100000',
'8': '11111110',
'9': '11110110',
'0': '11111100',
}

#upper case characters
characters = {
' ': '00000000',
'A': '11101110',
'B': '11111110',
'C': '10011100',
'D': '11111000',
'E': '10011110',
'F': '10001110',
'G': '10111100',
'H': '01101110',
'I': '00001100',
'J': '01111000',
'K': '01011110',
'L': '00011100',
'M': '10101010',
'N': '01101110',
'O': '11111100',
'P': '11001110',
'Q': '11011100',
'R': '11011110',
'S': '10110110',
'T': '10001100',
'U': '01111100',
'V': '01110100',
'W': '01010110',
'X': '10010010',
'Y': '01110110',
'Z': '11011010',
}

all_characters = {**numbers, **characters}

class Chars:

    def __init__(self):
        print('[sevensegchars.py] TM1638 initiated')


    #returns a blank character if the numer can't be found.
    def getNumber(self, number):
        if str(number) in numbers:
            return numbers[number]
        else:
            return characters[' ']

    def getCharacter(self, character, decimal_point=False):
        selected = all_characters[' ']

        if str(character) in all_characters:
            selected = all_characters[character]

        if(decimal_point):
            selected = selected[:7] + '1'

        return selected
