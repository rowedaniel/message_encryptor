import json
import sys
from hashlib import md5

import yaml
from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader("encryptor"),
    autoescape=select_autoescape(),
)


def one_time_pad_character(message: str, key: str, direction: int = -1) -> str:
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if message not in letters or key not in letters:
        return message
    m_num = letters.index(message)
    k_num = letters.index(key)
    out = letters[(m_num + direction * k_num) % len(letters)]
    return out


def encrypt_message(
    message: str,
    keys: dict[str, str],
    keymasks: list[str],
) -> str:
    # initialize keys and output array, making everything uppercase
    encrypted = list(message.upper())
    keys = {name: key.upper() for name, key in keys.items()}

    # keep track of where each key is at
    key_indicies = {key: 0 for key in keys.keys()}

    for i, char in enumerate(encrypted):
        # apply all specified keys to the current character
        for (key_name, key), mask in zip(keys.items(), keymasks.values()):
            # only apply keys designated for this character
            if mask[i] != "1":
                continue

            # get current key character, then advance counter
            key_char = key[key_indicies[key_name]]
            key_indicies[key_name] += 1
            key_indicies[key_name] %= len(key)

            # apply key
            char = one_time_pad_character(char, key_char)
        encrypted[i] = char
    return "".join(encrypted)


def get_hash(value: str) -> str:
    return md5(value.upper().encode()).hexdigest()


def generate(
    template_filename: str,
    config_filename: str,
    output_filename: str,
) -> None:
    """
    Generate a valid standalone HTML file which contains the encrypted message
    """

    template = env.get_template(template_filename)

    # get config
    with open(config_filename, "r") as file:
        config = yaml.safe_load(file)

        # hashmap mapping code names to plaintext values
        # (should never be given to user)
        keys = config["keys"]

        # message to encode
        # (should never be given to user)
        message = config["message"]

        # mask determining which characters each key applies to
        # can be given as-is to user
        keymasks = config["keymasks"]
        if len(keymasks) < len(keys):
            raise ValueError("must have same number of keys and keymasks")
        if any([len(message) < len(mask) for mask in keymasks]):
            raise ValueError("all keymasks must have same length as message")

    # get stuff to be sent to user

    # get code names and hashes (safe to give to user)
    # the hash is used to give feedback when the user has the right code
    code_names = list(keys.keys())
    code_hashes = {name: get_hash(value) for name, value in keys.items()}

    # encrypt message (so they are safe to give to user)
    message_encrypted = enumerate(encrypt_message(message, keys, keymasks))
    keymask_list = {name: list(value) for name, value in keymasks.items()}

    render = template.render(
        code_names=code_names,
        message=message_encrypted,
        code_hashes=json.dumps(code_hashes),
        keymasks=json.dumps(keymask_list),
    )

    with open(f"encryptor/build/{output_filename}", "w") as file:
        file.write(render)


def main():
    if len(sys.argv) != 3:
        print("Usage: generate.py input_filename output_filename")
        return

    generate("template.html", sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
