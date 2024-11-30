hex_data = ""

pairs = {}

tokens = []

meta_data = {}

def mitochondria():
    file_name = input("Enter the file name: ")
    mode = input("Append (a), Remove (d), Replace (r), or Overwrite (o):")

    if mode.lower() == "a":
        append(file_name, (input("Enter token to append (press Enter to append K-V pair): ") or None), (input("Enter key:value to append (press Enter for None): ") or None))
    elif mode.lower() == "d":
        remove(file_name, (input("Enter token to remove (press Enter to remove K-V pair): ") or None), (input("Enter key to remove (press Enter for None): ") or None))
    elif mode.lower() == "r":
        replace(file_name, (input("Enter old-token:new-token (press Enter for None): ") or None), (input("Enter old key to replace (press Enter for None): ") or None),  (input("Enter new key:value to replace (press Enter for None): ") or None))
    elif mode.lower() == "o":
        print("Meta-data should be entered as key-value pairs without hex encoding.")
        print("Accepted meta-data includes: D_NAME (Database name), D_VERSION (Database version), D_DC (Date Created), D_DESC (Description)")
        print("Example: D_NAME=login_data1; D_VERSION=1.2.3; D_DC=11-29-2024; D_DESC=This database stores usernames.")
        meta_input = input("Enter metadata (or press Enter for None): ")
        meta_data = [item.strip() for item in meta_input.split(";") if item.strip()]
        print("Enter raw data or key-value pairs in the format {key:value}, separating multiple entries with ';'.")
        data_input = input("Enter the data to store: ")
        process(data_input)
        write(file_name, meta_data)

    else:
        print("Invalid Mode")
        return

def remove(file, token=None, key=None):
    with open(f"DATABASES/{file}.css", 'r') as css:
        lines = css.readlines()

    modified_lines = []
    skip = False

    tokens_to_remove = set()

    if token:
        tokens_to_remove.update(tokenize(token))

    index = 0
    while index < len(lines):
        line = lines[index]
        stripped_line = line.strip()

        if tokens_to_remove:
            if stripped_line.startswith("color: #") and stripped_line[8:14] in tokens_to_remove:
                index += 1
                continue

        if key:
            if stripped_line == f"--key: #{convert(key)};":
                skip = True
                index += 1
                continue

            if skip and stripped_line.startswith("--value: #"):
                skip = False
                index += 1
                continue

        modified_lines.append(line)
        index += 1

    with open(f"DATABASES/{file}.css", 'w') as css:
        css.writelines(modified_lines)


def append(file, token=None, key=None):
    with open(f"DATABASES/{file}.css", 'r') as css:
        lines = css.readlines()

    current_lines = [line for line in lines]
    new_lines = []

    if token:
        new_lines = current_lines
        new_lines.pop(-1)
        for i in tokenize(token):
            new_lines.append(f"  color: #{i};\n")
        new_lines.append("}")


    with open(f"DATABASES/{file}.css", 'w') as css:
        css.writelines(new_lines)

def replace(file, token=None, old_key=None, new_kv=None):
    with open(f"DATABASES/{file}.css", 'r') as css:
        lines = css.readlines()
        modified_lines = []

        old_to_new_tokens = {}

        if token:
            old_token, new_token = token.split(":")
            old_to_new_tokens = {tok: new_token for tok in tokenize(old_token)}

        if old_key and new_kv:
            new_key = new_kv.split(":")[0]
            new_value = new_kv.split(":")[1]

        for line in lines:
            stripped_line = line.strip()

            if "color: #" in stripped_line:
                token_start = stripped_line.find("#") + 1

                token_value = stripped_line[token_start:token_start + 6]

                if token_value in old_to_new_tokens:
                    line = f"  color: #{old_to_new_tokens[token_value]};\n"

            if stripped_line == f"--key: #{convert(old_key)};":
                line = f"  --key: #{convert(new_key)};\n"
                modified_lines.append(line)
                line = f"  --value: #{convert(new_value)};\n"

            modified_lines.append(line)

        with open(f"DATABASES/{file}.css", 'w') as css:
            css.writelines(modified_lines)


def pairify(key, value):
    key = convert(key)
    value = convert(value)

    pairs[key] = value


def tokenize(data):
    hex_data = (data.encode('utf-8')).hex()

    for i in range(0, len(hex_data), 6):
        token = hex_data[i:i + 6].ljust(6, '0')
        tokens.append(token)

    return tokens


def convert(data):
    hex_data = (data.encode('utf-8')).hex()

    return hex_data


def process(data):
    global pairs
    global tokens

    parts = data.split(';')
    for part in parts:
        part = part.strip()
        while '{' in part and '}' in part:
            start = part.index("{")
            end = part.index("}")
            pair_content = part[start + 1:end]
            key_value_pair = pair_content.split(':', 1)
            if len(key_value_pair) == 2:
                key, value = key_value_pair
                pairify(key.strip(), value.strip())
            part = part[end + 1:].strip()

        if part:
            tokenize(part)


def write(file, meta_data: str = None):
    with open(f"DATABASES/{file}.css", 'w') as css:
        if meta_data is not None:
            css.write(".META_DATA {\n")
            meta_data = {k: v for k, v in (item.split("=") for item in meta_data if "=" in item)}
            for k, v in meta_data.items():
                css.write("  --" + k + ": " + v + ";\n")
            css.write("}\n")
        css.write(".key_value_pairs {\n")
        for i, j in pairs.items():
            css.write(f"  --key: #{i}; \n  --value: #{j};\n")
        css.write("}\n")
        css.write(".raw_data {\n")
        for token in tokens:
            css.write(f"  color: #{token};\n")
        css.write("}")


if __name__ == "__main__":
    mitochondria()