#########################################################################
# Assignment: pa01 - Encrypting a plaintext file using the Hill cipher  #
#                                                                       #
# Author: Allan Aquino Vieira                                           #
# Language: python 3                                                    #
# To Compile: Python                                                    #
#                                                                       #
# To Execute: python -> python3 pa01.py kX.txt pX.txt                   #
# where kX.txt is the keytext file                                      #
# and pX.txt is plaintext file                                          #
#                                                                       #
# Note:                                                                 #
# All input files are simple 8 bit ASCII input                          #
# All execute commands above have been tested on Eustis                 #
#                                                                       #
# Class: CIS3360 - Security in Computing - Spring 2025                  #
# Instructor:                                                           #
# Due Date: Feb 23, 2025                                                #
#########################################################################


import sys

key_file_name: str = ""
key = 0
key_dimensions: int = ""
plain_text_file_name: str = ""
plain_text: str = ""
cipher_text = ""


def read_file(file_name: str) -> str:
    file_object = None
    file_content = None

    try:
        with open(file_name, "rt") as file_object:
            if not file_object:
                print(f"{file_name} is empty!")
            else:
                file_content = file_object.read()

        # print("type(file_content) =", type(file_content))
        # print("file_content\n", file_content)

    except FileNotFoundError as open_error:
        file_object.flush()
        print(f"{file_name} not found!")
        print(open_error)

    finally:
        return file_content


def key_parser(key):
    if key:
        # KEY file contents parsing
        key_dimensions = int(key[:key.find("\n")])
        temp = key[(key.find("\n"))+1:].split()

        # Building Key Matrix key_dimensions * key_dimensions
        i = 0
        key = [[] for _ in range(key_dimensions)]
        # Each sub list is a matrix Row
        for element in range(key_dimensions):
            for item in range(key_dimensions):
                key[element].append(int(temp[i]))
                i += 1

    return key, key_dimensions


def format_plaintext(plain_text: str, key_dimension: int) -> str:

    temp = ""

    if plain_text:
        plain_text = plain_text.replace("\n", "")
        plain_text = plain_text.lower()

        for letter in plain_text:
            if letter.isalpha():
                if letter.isascii():
                    temp += letter
            else:
                pass

        while (len(temp) % key_dimension):
            temp = temp + "x"

        plain_text = temp

    else:
        print("Plain text file is empty")

    return plain_text


def create_plain_text_matrix(content, key_dimension: int):

    if not (len(content) % key_dimension):

        i = 0
        matrix = [[] for vectors in range(int(len(content)/key_dimension))]
        temp = content.split()
        # print("temp", temp)
        # print(int(len(content)/key_dimension))

        for vectors in range(int(len(content)/key_dimension)):

            for elements in range(key_dimension):

                matrix[vectors].append(ord(content[i])-ord("a"))
                i += 1
    else:
        while (len(content) % key_dimension):
            content = content + "x"

        i = 0
        matrix = [[] for vectors in range(int(len(content)/key_dimension))]
        temp = content.split()

        for vectors in range(int(len(content)/key_dimension)):

            for elements in range(key_dimension):

                matrix[vectors].append(ord(content[i])-ord("a"))
                i += 1
    # print(matrix)
    return matrix


def print_sqr_matrix(matrix: list, dimention: int):
    for rows in range(dimention):
        for columns in range(dimention):
            print("%4d" % matrix[rows][columns], end="")
        print()


def hill_cipher(key_matrix, plain_text_vectors, key_dimensions):

    cipher_text_str = ""
    temp: int = 0
    for vectors in range(len(plain_text_vectors)):  # plain text sets
        for rows in range(key_dimensions):  # rows of key
            for elements in range(key_dimensions):
                temp += (key_matrix[rows][elements] *
                         plain_text_vectors[vectors][elements])
            temp = (temp % 26)+ord("a")
            cipher_text_str += chr((temp))
            temp = 0
    return cipher_text_str


def eighty_char_row_output(cipher):
    formatted_output = ""
    for i in range(len(cipher)):
        # formatted_output += cipher[i:(i+1)]
        if i > 1 and (not (i % 80)):
            formatted_output += "\n"
        formatted_output += cipher[i:(i+1)]
    return formatted_output


def main():
    global key
    global key_dimensions
    global key_file_name
    global plain_text
    global plain_text_file_name
    global cipher_text

    # Reads terminal arguments into arg_in
    arg_in = sys.argv[1:]

    #########################################
    # VALIDATE NUMBER OF TERMINAL ARGUMENTS #
    #########################################

    if len(arg_in) < 2:
        print("Not enough arguments!")
        print("Please enter the file names for: Encyption Key followed by Plain Text.")
    elif len(arg_in) > 2:
        print("Too many arguments!")
        print("Please enter the file names for: Encyption Key followed by Plain Text.")
    else:
        key_file_name = arg_in[0]
        plain_text_file_name = arg_in[1]
        # print("""The terminal arguments recived were:""" +
        #       """\n  Key file name is""", key_file_name,
        #       """\n  Plain text file name""", plain_text_file_name)
        key = read_file(key_file_name)
        plain_text = read_file(plain_text_file_name)

    ##################
    # ENCRIPTION KEY #
    ##################

    key, key_dimensions = key_parser(key)
    print("\nKey matrix:")
    print_sqr_matrix(key, key_dimensions)

    ##############
    # PLAIN TEXT #
    ##############

    plain_text = plain_text.strip()
    plain_text = format_plaintext(plain_text, key_dimensions)
    print("\nPlaintext:\n" + eighty_char_row_output(plain_text))
    plain_text_matrix = create_plain_text_matrix(plain_text, key_dimensions)

    ##############
    # ENCRYPTION #
    ##############

    cipher_text = hill_cipher(key, plain_text_matrix, key_dimensions)
    cipher_text = eighty_char_row_output(cipher_text)

    print("\nCiphertext:\n" + cipher_text)


if __name__ == '__main__':
    main()


#       I Allan Aquino Vieira (a) affirm that this program is
# entirely my own work and that I have neither developed my code together with
# any another person, nor copied any code from any other person, nor permitted
# my code to be copied or otherwise used by any other person, nor have I
# copied, modified, or otherwise used programs created by others. I acknowledge
# that any violation of the above terms will be treated as academic dishonesty.
