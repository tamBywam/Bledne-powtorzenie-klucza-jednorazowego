import sys
import os


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

def xor_decrypt(crypto_file, key_file, decrypt_file):
    with open(crypto_file, 'r') as cfile, open(key_file, 'r') as kfile, open(decrypt_file, 'w') as dfile:
        ciphertexts = [bytes.fromhex(line.strip()) for line in cfile]
        key = kfile.read().strip()
        key_len = len(key)
        for ct in ciphertexts:
            decrypted_line = ''.join(chr(ct[i] ^ ord(key[i % key_len])) for i in range(len(ct)))
            dfile.write(decrypted_line + '\n')

def crypto_analysis(crypto_file, decrypt_file):
    with open(crypto_file, 'r') as cfile, open(decrypt_file, 'w') as dfile:
        ciphertexts = [bytes.fromhex(line.strip()) for line in cfile]
        num_lines = len(ciphertexts)
        line_length = len(ciphertexts[0])
        result = [['_' for _ in range(line_length)] for _ in range(num_lines)]

        for i in range(num_lines):
            for j in range(i + 1, num_lines):
                for k in range(line_length):
                    xor_val = ciphertexts[i][k] ^ ciphertexts[j][k]
                    if (xor_val & 0b11100000) == 0b01000000:
                        m1_guess = xor_val ^ 0x20
                        if 97 <= m1_guess <= 122:
                            result[i][k] = chr(m1_guess)
                            result[j][k] = ' '
                        else:
                            m2_guess = xor_val ^ 0x20
                            if 97 <= m2_guess <= 122:
                                result[j][k] = chr(m2_guess)
                                result[i][k] = ' '

        for line in result:
            dfile.write(''.join(line) + '\n')

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