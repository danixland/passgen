#! /usr/bin/env python

import argparse
import random

### VARIABLES
# by default we'll use these many words
word_count = 3
# minimum char lenght of the generated password
min_chars = 12
# our list of separators
separators = ["~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "-", "+", "=", "{", "}", "[", "]", "|", ":", ";", "<", ">", ",", ".", "?"]
# our dictionary
dictionary = '/usr/share/dict/words'

def get_random_words(num_words):
    with open(dictionary, 'r') as file:
        words = file.read().splitlines()

    if not num_words:
        num_words = word_count
    return [random.choice(words) for _ in range(num_words)]

def get_separator(custom_symbol, use_random):
    if use_random:
        separator = random.choice(separators)
    elif custom_symbol:
        separator = custom_symbol
    else:
        separator = "@"
    return separator

def generate_password(num_words, custom_symbol=None, use_random_separator=False, include_numerals=True, min_length=0, capitalize_words=False):
    words = get_random_words(num_words)

    if capitalize_words:
        # Capitalize one of the words by default
        random_word_index = random.randint(0, num_words - 1)
        words[random_word_index] = words[random_word_index].capitalize()

    if not include_numerals:
        password = ''.join(words)
    else:
        # Ensure at least one number is included
        password = ''.join(words)
        if not any(char.isdigit() for char in password):
            password += str(random.randint(0, 9))

    separator = get_separator(custom_symbol, use_random_separator)

    # Add separators between words
    password = separator.join(words)

    while True:
        if not include_numerals and not any(char.isdigit() for char in password):
            break
        if not include_numerals or (include_numerals and not any(char.isdigit() for char in password)):
            password += str(random.randint(0, 9))
            break
        # Find positions to place the separator and number
        positions = []
        for i in range(len(password) - len(separator)):
            if password[i:i+len(separator)] == separator:
                positions.append(i)
        if not positions:
            break
        pos = random.choice(positions)
        new_password = password[:pos] + str(random.randint(0, 9)) + separator + password[pos+len(separator):]
        
        # Ensure only one symbol is between each word and the number is correctly placed
        if new_password.count(separator) == num_words - 1 and (include_numerals or not any(char.isdigit() for char in new_password)):
            password = new_password
            break
    
    while len(password) < min_length:
        extra_word = random.choice(words)
        password += separator + extra_word

    return password

def main():
    parser = argparse.ArgumentParser(description="Generate a strong password using random words.")
    parser.add_argument('num_words', type=int, nargs='?', default=word_count,
    					help='Number of words to use in the password (default: '+str(word_count)+')')
    parser.add_argument('-s', '--separator', choices=separators, default=None, 
                        help='Custom separator symbol (default: "@")')
    parser.add_argument('-r', '--random-separator', action='store_true', 
                        help='Use a random separator from our list')
    parser.add_argument('--min-length', type=int, default=min_chars,
                        help='Minimum length in characters for the password (default: '+str(min_chars)+')')
    parser.add_argument('-0', '--no-numerals', action='store_false', dest='include_numerals',
                        help='Disable numbers in the output')
    parser.add_argument('-A', '--no-capitals', action='store_false', dest='capitalize_words',
                        help='Disable capitalized words in the output')
    
    args = parser.parse_args()
    
    password = generate_password(args.num_words, args.separator, args.random_separator, args.include_numerals, args.min_length, args.capitalize_words)
    
    print(f"{password}")

if __name__ == "__main__":
    main()