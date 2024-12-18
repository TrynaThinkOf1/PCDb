def mitochondria():
    input_file = input("File to process: ").strip()
    mode = input("Parse (p) or Query (q): ").lower()

    if mode == "p":
        mode = input("Key-Value Pairs (kvp) or Raw (raw) or both (both): ").lower()
        try:
            print("-----------------------------------------------\n")
            print(parse(input_file, mode))
        except Exception as e:
            print(e)
    elif mode == "q":
        query = input("Query: ")
        try:
            print("-----------------------------------------------\n")
            print(parse(input_file, query=query))
        except Exception as e:
            print(e)
    else:
        print("Invalid Mode")

def parse(file, mode="raw", query=None):
    key_value_pairs = {}
    meta_data = {}

    line_nums = {}

    tokens = []

    with open(f"DATABASES/{file}.css", 'r') as css:
        lines = css.readlines()
        comment = False
        kvp_mode = False
        raw_mode = False
        meta = False

        current_key = ""
        current_value = ""

        # parse
        for line in lines:
            stripped_line = line.strip()

            if stripped_line.startswith("/*"):
                comment = True

            if stripped_line.endswith("*/"):
                comment = False

            if not comment:
                if stripped_line.startswith(".META_DATA {"):
                    meta = True

                if stripped_line.startswith(".key_value_pairs {"):
                    kvp_mode = True
                    raw_mode = False

                elif stripped_line.startswith(".raw_data {"):
                    kvp_mode = False
                    raw_mode = True

                if meta:
                    if stripped_line.startswith("--D"):
                        stripped_line = stripped_line.removeprefix("--").removesuffix(";")
                        key, value = stripped_line.split(":")
                        key = key.strip()
                        if "NAME" in key:
                            key = "Database Name"
                        elif "VERSION" in key:
                            key = "Database Version"
                        elif "DC" in key:
                            key = "Date Database was Created"
                        elif "DESC" in key:
                            key = "Database Description"
                        meta_data[key] = value.strip()

                if kvp_mode:
                    if stripped_line.startswith("--key: #"):
                        stripped_line = stripped_line.removeprefix("--key: #").removesuffix(";")
                        current_key = stripped_line

                    elif stripped_line.startswith("--value: #"):
                        stripped_line = stripped_line.removeprefix("--value: #").removesuffix(";")
                        current_value = stripped_line

                        if current_key:
                            key_value_pairs[current_key] = current_value
                            current_key = ""
                            current_value = ""

                elif raw_mode:
                    if stripped_line.startswith("color: #"):
                        stripped_line = stripped_line.removeprefix("color: #").removesuffix(";")

                        if all(c in '0123456789abcdefABCDEF' for c in stripped_line) and len(stripped_line) == 6:
                            tokens.append(stripped_line)


    if query is not None:
        key_value_pairs = decode_key_value_pairs(key_value_pairs)
        if key_value_pairs.get(query):
            return f"Key: '{query}'\nValue: '{key_value_pairs[query]}'\n"
        else:
            return f"Key: {query} Not Found."

    if mode.lower() == "raw":
        return f"\n\nMeta-Data: {format(meta_data)}\n\nRaw-Data: \n{decode_raw_data(''.join(tokens))}"
    elif mode.lower() == "kvp":
        return f"\n\nMeta-Data: {format(meta_data)}\n\nK-V Pairs: \n{format(decode_key_value_pairs(key_value_pairs))}"
    elif mode.lower() == "both":
        return f"\n\nMeta-Data: {format(meta_data)}\n\nK-V Pairs: \n{format(decode_key_value_pairs(key_value_pairs))}\n\nRaw-Data: \n{decode_raw_data(''.join(tokens))}"
    else:
        return "Invalid Mode"

def format(data):
    return '\n'.join([f"{key}: '{value}'" for key, value in data.items()])

def decode_key_value_pairs(dictionary):
    try:
        if dictionary is None:
            print("No Key-Value Pairs to decode.")
            return

        pairs = {}
        for i, j in dictionary.items():
            i = bytes.fromhex(i).replace(b'\x00', b'').decode('utf-8')
            j = bytes.fromhex(j).replace(b'\x00', b'').decode('utf-8')
            pairs[i] = j

        return pairs

    except Exception as e:
        raise Exception(e)

def decode_raw_data(data):
    try:
        byte_data = bytes.fromhex(data).replace(b'\x00', b'')
        return str(byte_data).replace('b', '')

    except Exception as e:
        raise Exception(e)


if __name__ == "__main__":
    mitochondria()