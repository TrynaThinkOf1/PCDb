def parse(file, mode="raw", query=None):
    key_value_pairs = {}
    line_nums = {}

    tokens = []

    with open(f"DATABASES/{file}.css", 'r') as css:
        lines = css.readlines()
        comment = False
        kvp_mode = False
        raw_mode = False

        current_key = ""
        current_value = ""

        # parse
        for line_num, line in enumerate(lines, start=1):
            stripped_line = line.strip()

            if stripped_line.startswith("/*"):
                comment = True

            if stripped_line.endswith("*/"):
                comment = False


            if not comment:
                if stripped_line.startswith(".key_value_pairs {"):
                    kvp_mode = True
                    raw_mode = False

                elif stripped_line.startswith(".raw_data {"):
                    kvp_mode = False
                    raw_mode = True

                if kvp_mode:
                    if stripped_line.startswith("--key: #"):
                        stripped_line = stripped_line.removeprefix("--key: #").removesuffix(";")
                        current_key = stripped_line

                    elif stripped_line.startswith("--value: #"):
                        stripped_line = stripped_line.removeprefix("--value: #").removesuffix(";")
                        current_value = stripped_line

                        if current_key:
                            key_value_pairs[current_key] = current_value
                            line_nums[decode_raw_data(current_key).replace("'", "")] = line_num
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
            return f"Key: '{query}'\nValue: '{key_value_pairs[query]}'\nLine: {line_nums[query]}" #Key: {query} Found at line {line_nums[query]} With Value: {key_value_pairs[query]}
        else:
            return f"Key: {query} Not Found."

    if mode.lower() == "raw":
        return decode_raw_data(''.join(tokens))
    elif mode.lower() == "kvp":
        return decode_key_value_pairs(key_value_pairs)
    elif mode.lower() == "both":
        return decode_key_value_pairs(key_value_pairs), decode_raw_data(''.join(tokens))
    else:
        return "Invalid Mode"

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
    input_file = input("File to process: ").strip()
    mode = input("Parse (p) or Query (q): ").lower()

    if mode == "p":
        mode = input("Key-Value Pairs (kvp) or Raw (raw): ").lower()
        try:
            print(parse(input_file, mode))
        except Exception as e:
            print(e)
    elif mode == "q":
        query = input("Query: ")
        try:
            print(parse(input_file, query=query))
        except Exception as e:
            print(e)
    else:
        print("Invalid Mode")
