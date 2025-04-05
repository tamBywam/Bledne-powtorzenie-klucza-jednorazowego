# Jakub Opólski
import sys


def prepare_text(input_file, output_file, line_length):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        text = infile.read().replace('\n', ' ')
        for i in range(0, len(text), line_length):
            line = text[i:i+line_length]
            outfile.write(line.ljust(line_length) + '\n')

def xor_encrypt(plain_file, key_file, crypto_file):
    with open(plain_file, 'r') as pfile, open(key_file, 'r') as kfile, open(crypto_file, 'w') as cfile:
        plaintext = pfile.readlines()
        key = kfile.read().strip()
        key_len = len(key)
        for line in plaintext:
            line = line.rstrip('\n')
            encrypted_bytes = bytes([ord(line[i]) ^ ord(key[i % key_len]) for i in range(len(line))])
            cfile.write(encrypted_bytes.hex() + '\n')

def crypto_analysis(crypto_file, decrypt_file):
    with open(crypto_file, 'r') as cfile:
        ciphertexts = [bytes.fromhex(line.strip()) for line in cfile]

    num_lines = len(ciphertexts)
    line_length = len(ciphertexts[0])

    guessed_key = [None] * line_length
    key_score = [0] * line_length

    for col in range(line_length):
        possible_keys = {}
        for row in range(num_lines):
            val = ciphertexts[row][col]
            key_candidate = val ^ 0x20
            valid = 0
            for other_row in range(num_lines):
                decoded = ciphertexts[other_row][col] ^ key_candidate
                if decoded == 32 or (97 <= decoded <= 122):
                    valid += 1
            if key_candidate in possible_keys:
                possible_keys[key_candidate] += valid
            else:
                possible_keys[key_candidate] = valid

        if possible_keys:
            best_key, score = max(possible_keys.items(), key=lambda x: x[1])
            guessed_key[col] = best_key
            key_score[col] = score

    result = []
    for row in range(num_lines):
        line = ''
        for col in range(line_length):
            if guessed_key[col] is not None:
                decoded = ciphertexts[row][col] ^ guessed_key[col]
                if decoded == 32 or (97 <= decoded <= 122):
                    line += chr(decoded)
                else:
                    line += '_'
            else:
                line += '_'
        result.append(line)

    with open(decrypt_file, 'w') as dfile:
        for line in result:
            dfile.write(line + '\n')

def main():
    option = sys.argv[1]

    if option == '-p':
        prepare_text('orig.txt', 'plain.txt', 64)
    elif option == '-e':
        xor_encrypt('plain.txt', 'key.txt', 'crypto.txt')
    elif option == '-k':
        crypto_analysis('crypto.txt', 'decrypt.txt')

if __name__ == "__main__":
    main()