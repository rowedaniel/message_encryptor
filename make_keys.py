import random
import sys


def main():
    LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if len(sys.argv) < 2:
        print("missing argument: length of key")
        return
    key_len = int(sys.argv[1])

    print("".join([random.choice(LETTERS) for i in range(key_len)]))


if __name__ == "__main__":
    main()
