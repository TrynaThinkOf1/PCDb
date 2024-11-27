tokens = []
final_token = ""

def parse(file):
    global tokens, final_token
    tokens.clear()
    final_token = ""

    with open(f"DATABASES/{file}.css", 'r') as css:
        lines = css.readlines()
        comment = False

        # parse
        for line in lines:
            stripped_line = line.strip()
            if stripped_line.startswith("/*"):
                comment = True
            if not comment:
                if stripped_line.startswith("color: #"):
                    stripped_line = stripped_line.removeprefix("color: #").removesuffix(";")
                    if all(c in '0123456789abcdefABCDEF' for c in stripped_line) and len(stripped_line) == 6:
                        tokens.append(stripped_line)
            if stripped_line.endswith("*/"):
                comment = False

        final_token = ''.join(tokens)
        return final_token

def decode(token):
    try:
        print("Final token: " + final_token)
        byte_data = bytes.fromhex(token).replace(b'\x00', b'')
        human_output = str(byte_data).replace('b', '')
        print(human_output)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    decode(parse(input("Enter file name: ")))