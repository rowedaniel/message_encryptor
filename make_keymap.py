import random
import sys


def main():
    if len(sys.argv) < 2:
        raise ValueError("Usage: make_keymap.py keycount overlap message")
    number_keys = int(sys.argv[1])
    key_overlap = int(sys.argv[2])
    message = " ".join(sys.argv[3:])

    keymaps = [["0" for _ in message] for key in range(number_keys)]

    for char in range(len(message)):

        # choose two keys to apply to this character
        for i in range(key_overlap):
            key = random.randint(0, number_keys - 1)
            keymaps[key][char] = "1"

    for keymap in keymaps:
        print("".join(keymap))


if __name__ == "__main__":
    main()
