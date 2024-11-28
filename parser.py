key_value_pairs = {}


def parse(file):
    global key_value_pairs

    with open(f"DATABASES/{file}.css", 'r') as css:
        lines = css.readlines()
        comment = False

        current_key = ""
        current_value = ""

        # parse
        for line in lines:
            stripped_line = line.strip()

            if stripped_line.startswith("/*"):
                comment = True
            if not comment:
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

            if stripped_line.endswith("*/"):
                comment = False

        return key_value_pairs


def decode(dictionary):
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
        print(e)


if __name__ == "__main__":
    file_data = parse(input("Enter file name: "))
    decoded_data = decode(file_data)
    if decoded_data:
        print("Decoded Data: ", decoded_data)