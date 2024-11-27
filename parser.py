tokens = []
final_token = ""

def parse():
    global tokens, final_token
    with open("DATABASES/base1.css", 'r') as css:
        lines = css.readlines()
        comment = False

        # parse
        for line in lines:
            stripped_line = line.strip()
            if stripped_line.startswith("/*"):
                comment = True
            if not comment:
                if stripped_line.startswith("color: #"):
                    stripped_line = stripped_line.removeprefix("color: #")
                    stripped_line = stripped_line.removesuffix(";")
                    tokens.append(stripped_line)
            if stripped_line.endswith("*/"):
                comment = False

        for token in tokens:
            final_token += token

        return final_token

def decode(token):
    try:
        byte_data = bytes.fromhex(token).replace(b'\x00', b'')
        human_output = str(byte_data).replace('b', '')
        print(human_output)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    decode(parse())