#constants used to display characters on a seven segment LCD display

numbers = {
'1': '00110000',
'2': '01101101',
'3': '01111001',
'4': '00110011',
'5': '01011011',
'6': '01011111',
'7': '01110000',
'8': '01111111',
'9': '01111011',
'0': '01111110',
}

#upper case characters
characters = {
' ': '00000000',
'A': '01110111',
'B': '01111111',
'C': '01001110',
'D': '01111100',
'E': '01001111',
'F': '01000111',
'G': '01011110',
'H': '00110111',
'I': '00000110',
'J': '00111100',
'K': '00101111',
'L': '00001110',
'M': '01010101',
'N': '00110111',
'O': '01111110',
'P': '01100111',
'Q': '01101110',
'R': '01101111',
'S': '01011011',
'T': '01000110',
'U': '00111110',
'V': '00111010',
'W': '00101011',
'X': '01001001',
'Y': '00111011',
'Z': '01101101',
}

all_characters = {**numbers, **characters}

class Chars:

    def __init__(self):
        print('[sevensegchars.py] initiated')


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
            selected = '1' + selected[1:]

        return selected
