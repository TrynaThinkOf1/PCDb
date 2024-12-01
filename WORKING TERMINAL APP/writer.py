hex_data = ""

pairs = {}

tokens = []

meta_data = {}

def remove(file, token=None, key=None):
    with open(f"sys_func_main_log()/{file}.css", 'r') as css:
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

    with open(f"sys_func_main_log()/{file}.css", 'w') as css:
        css.writelines(modified_lines)


def append(file, token=None, kv=None):
    with open(f"sys_func_main_log()/{file}.css", 'r') as css:
        lines = css.readlines()

    new_lines = []
    found = False

    if token:
        for line in lines:
            new_lines.append(line)
            if ".raw_data {" in line and not found:
                found = True

                for i in tokenize(token):
                    new_lines.append(f"  color: #{i};\n")

                if "}" not in lines[lines.index(line) + 1:]:
                    new_lines.append("}\n")
                continue

    elif kv:
        for line in lines:
            new_lines.append(line)
            if ".key_value_pairs {" in line and not found:
                found = True

                key, value = kv.split(":")
                key = convert(key.strip())
                value = convert(value.strip())
                new_lines.append(f"  --key: #{key}; \n  --value: #{value};\n")

                if "}" not in lines[lines.index(line) + 1:]:
                    new_lines.append("}\n")
                continue

    new_lines += [line for line in lines if line not in new_lines]

    with open(f"sys_func_main_log()/{file}.css", 'w') as css:
        css.writelines(new_lines)

def replace(file, token=None, old_key=None, new_kv=None):
    with open(f"sys_func_main_log()/{file}.css", 'r') as css:
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

        with open(f"sys_func_main_log()/{file}.css", 'w') as css:
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
    with open(f"sys_func_main_log()/{file}.css", 'w') as css:
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