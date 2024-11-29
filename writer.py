hex_data = ""

pairs = {}

tokens = []

meta_data = {}

def mitochondria():
    file_name = input("File to store data: ")
    print("Meta-data is stored as un-hexed key-value pairs (D_NAME: Database name, D_VERSION: Database version, D_DC: Database data created, D_DESC: Database description)")
    print("Example: D_NAME=username_data1; D_VERSION=1.2.3 (only ints and '.'); D_DC=11-29-2024; D_DESC=This is a database for storing usernames.")
    meta_data = input("Meta data to store (return for None): ").split(";").strip()
    print("All raw text will be stored, to store a key-value pair: {key:value}. Seperate key-value pairs from raw data with ;")
    data = input("Data to store: ")
    process(data)
    write(file_name, meta_data=meta_data)

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