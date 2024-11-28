tokens = []

def convert(string):
    global tokens
    token = ""

    byte_data = string.encode('utf-8')
    hex_data = byte_data.hex()
    for i in range(0, len(hex_data), 6):
        token = hex_data[i:i+6].ljust(6, '0')
        tokens.append(token)

    return tokens

def write(file):
    with open(f"DATABASES/{file}.css", 'w') as css:
        css.write(".string {\n")
        for token in tokens:
            css.write(f"  color: #{token};\n")
        css.write("}")

if __name__ == "__main__":
    file_name = input("File to store data: ")
    convert(input("Enter string: "))
    write(file_name)