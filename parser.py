key_value_pairs = {}

tokens = []
final_token = ""

def parse(file):
    global key_value_pairs, final_token, tokens

    with open(f"DATABASES/{file}.css", 'r') as css:
        lines = css.readlines()
        comment = False
        kvp_mode = False
        raw_mode = False

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
                if stripped_line.startswith(".key_value_pairs {"):
                    kvp_mode = True

                elif stripped_line.startswith(".raw_data {"):
                    kvp_mode = False
                    raw_mode = True

                if kvp_mode:
                    if stripped_line.startswith("--key: #"):
                        stripped_line = stripped_line.removeprefix("--key: #").removesuffix(";")
                        current_key = stripped_line
                        print("New Key: " + current_key)
                    elif stripped_line.startswith("--value: #"):
                        stripped_line = stripped_line.removeprefix("--value: #").removesuffix(";")
                        current_value = stripped_line
                        print("New Value: " + current_value)
                        if current_key:
                            key_value_pairs[current_key] = current_value
                            print(f"Stored pair, Key: {current_key} Value: {current_value}")
                            current_key = ""
                            current_value = ""

                elif raw_mode:
                    if stripped_line.startswith("color: #"):
                        stripped_line = stripped_line.removeprefix("color: #").removesuffix(";")
                        if all(c in '0123456789abcdefABCDEF' for c in stripped_line) and len(stripped_line) == 6:
                            tokens.append(stripped_line)
                            print("New Token: " + stripped_line)

        print("Raw Data: " + decode_raw_data(''.join(tokens)))
        return key_value_pairs



def decode_key_value_pairs(dictionary):
    try:
        if dictionary is None:
            print("No data to decode.")
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
        human_output = str(byte_data).replace('b', '')
        return human_output

    except Exception as e:
        raise Exception(e)


if __name__ == "__main__":
    print(decode_key_value_pairs(parse(input("File to parse: "))))