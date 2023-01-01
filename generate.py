import json
import sys
from hashlib import md5

import yaml
from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader("encryptor"),
    autoescape=select_autoescape(),
)


def one_time_pad(message: str, key: str, direction: int = -1) -> str:
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    message = message.upper()
    key = key.upper()
    message_nums = [letters.index(s) if s in letters else -1 for s in message]
    key_nums = [letters.index(s) if s in letters else -1 for s in key]
    return "".join(
        [
            message[i]
            if m == -1 or k == -1
            else letters[(m + direction * k) % len(letters)]
            for i, (m, k) in enumerate(zip(message_nums, key_nums))
        ]
    )


def encrypt_message(message: str, keys: list[str]) -> str:
    for key in keys:
        message = one_time_pad(message, key)
    return message


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
        codes = config["codes"]

        # list of messages to encode
        # (must all be shorter than their corresponding codes)
        # (should never be given to user)
        messages = config["messages"]

        # list of codes to be applied to each message
        key_mappings = config["key_mapping"]

    # get stuff to be sent to user

    # get code names and hashes (safe to give to user)
    # the hash is used to give feedback when the user has the right code
    code_names = list(codes.keys())
    code_hashes = {
        name: md5(value.encode()).hexdigest() for name, value in codes.items()
    }

    # map each code to list of messages it applies to
    code_appliers = {
        name: [i for i, key in enumerate(key_mappings) if name in key]
        for name in code_names
    }

    # encrypt messages (so they are safe to give to user)
    message_keys = [[codes[name] for name in keys] for keys in key_mappings]
    messages_encrypted = enumerate(
        [encrypt_message(msg, key) for msg, key in zip(messages, message_keys)]
    )

    render = template.render(
        code_names=code_names,
        messages=messages_encrypted,
        code_hashes=json.dumps(code_hashes),
        code_appliers=json.dumps(code_appliers),
        key_mappings=json.dumps(key_mappings),
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
