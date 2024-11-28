hex_data = ""

pairs = {}

tokens = []

def pairify(key, value):
    key = convert(key)
    value = convert(value)

    pairs[key] = value


def tokenizer(data):
    byte_data = data.encode('utf-8')
    hex_data = byte_data.hex()

    for i in range(0, len(hex_data), 6):
        token = hex_data[i:i + 6].ljust(6, '0')
        tokens.append(token)

    return tokens


def convert(data):
    byte_data = data.encode('utf-8')
    hex_data = byte_data.hex()

    return hex_data


def processor(data):
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
            tokenizer(part)


def write(file):
    with open(f"DATABASES/{file}.css", 'w') as css:
        css.write(".key_value_pairs {\n")
        for i, j in pairs.items():
            css.write(f"  --key: #{i}; \n  --value: #{j};\n")
        css.write("}\n")
        css.write(".raw_data {\n")
        for token in tokens:
            css.write(f"  color: #{token};\n")
        css.write("}")


if __name__ == "__main__":
    file_name = input("File to store data: ")
    print("All raw text will be stored, to store a key-value pair: {key:value}. Seperate key-value pairs from raw data with ;")
    data = input("Data to store: ")
    processor(data)
    write(file_name)