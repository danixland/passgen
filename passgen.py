#! /usr/bin/env python
#
#    passgen.py - generate strong, easy to remember passwords from a dictionary
#    Copyright (C) 2026  Danilo 'danix' Macrì
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

import argparse
import random
import string
from zxcvbn import zxcvbn

### ANSI escape codes for colors
COLOR_GREEN = '\033[92m'
COLOR_YELLOW = '\033[93m'
COLOR_RED = '\033[91m'
COLOR_BLUE = '\033[94m'
COLOR_PURPLE = '\033[95m'
COLOR_RESET = '\033[0m'

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

def check_strength(password):
    result = zxcvbn(password)
    crack_times = result['crack_times_display']
    crack_times_K = {
        'offline_fast_hashing_1e10_per_second': "Offline Hashing, Fast",
        'offline_slow_hashing_1e4_per_second': "Offline Hashing, Slow",
        'online_no_throttling_10_per_second': "Online Hashing Fast (10 attempts per second)",
        'online_throttling_100_per_hour': "Online Hashing Slow (100 attempts per hour)"
    }
    crack_times_readable = {crack_times_K[key]: value for key, value in crack_times.items()}
    score = result['score']
    return score, result['feedback']['warning'], result['feedback']['suggestions'], crack_times_readable

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
    parser.add_argument('--strength', action='store_true', help='Display the strength of the password')
    
    args = parser.parse_args()
    
    password = generate_password(args.num_words, args.separator, args.random_separator, args.include_numerals, args.min_length, args.capitalize_words)
    
    if args.strength:
        score, message, sugg, ctimes = check_strength(password)
        print(f'Generated Password: {password}')
        # print(f'Strength: {"Weak (1/5)" if score == 0 else "Bad (2/5)" if score == 1 else "Mediocre (3/5)" if score == 2 else "Good (4/5)" if score == 3 else "Strong (5/5)"}')
        if 0 < score <= 1:
            color = COLOR_RED
        elif 2 < score <= 3:
            color = COLOR_YELLOW
        elif score == 4:
            color = COLOR_GREEN
        print(f'Strenght: {color}{"Weak (1/5)" if score == 0 else "Bad (2/5)" if score == 1 else "Mediocre (3/5)" if score == 2 else "Good (4/5)" if score == 3 else "Strong (5/5)"}{COLOR_RESET}')

        if message:
            print(f'Description: {message}')

        if sugg:
            print(f'Suggestions: {str(sugg[0])}')

        if ctimes:
            for key, value in ctimes.items():
                print(f" - {key}: {COLOR_PURPLE}{value}{COLOR_RESET}")

    else:
        print(password)

if __name__ == "__main__":
    main()