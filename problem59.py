import itertools
import string


def decrypt(key: str, encrypted: str) -> str:
    """Decrypts encrypted by xor'ing it with key cyclically."""

    key_len = len(key)
    decrypted = ''

    # Go through the encrypted string in chunks the length of the key
    for i in range(0, len(encrypted), key_len):
        chunk = encrypted[i:i + key_len]  # Pull out a chunk the size of the key

        # Apply the key to the chunk
        for j, c in enumerate(chunk):
            decrypted += chr(ord(key[j]) ^ ord(c))

    return decrypted


if __name__ == "__main__":  # Set up an import guard

    # Problem parameters
    KEY_LEN = 3
    POSSIBLE_LETTERS = string.ascii_lowercase
    FILE_LOCATION = 'p059_cipher.txt'

    # Load all possible keys made from lowercase ascii characters
    all_keys = list(itertools.product(POSSIBLE_LETTERS, repeat=KEY_LEN))

    # Load the cipher
    encoded_all = open(FILE_LOCATION).read()

    # Parse the data by converting all values into their corresponding characters
    encoded_all = ''.join(map(lambda x: chr(int(x)), encoded_all.split(',')))

    # Start with a blank solution
    solution = ''

    # Try decrypting using each key
    for k in all_keys:
        decrypted = decrypt(k, encoded_all)

        # Decryption is considered successful if the text contains the word 'and'
        if ' and ' in decrypted:
            # Store the decrypted string
            solution = decrypted
            # Break so we dont keep trying more keys
            break

    # Print the sum of all the ascii characters in the decrypted string
    print(sum(map(ord, solution)))
