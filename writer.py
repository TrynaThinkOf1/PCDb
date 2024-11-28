hex_data = ""

pairs = {}

def pairify(key, value):
    key = convert(key)
    value = convert(value)

    pairs[key] = value

def convert(data):
    global hex_data

    byte_data = data.encode('utf-8')
    hex_data = byte_data.hex()

    return hex_data

def write(file):
    with open(f"DATABASES/{file}.css", 'w') as css:
        css.write(".string {\n")
        for i, j in pairs.items():
            css.write(f"  --key: #{i}; \n  --value: #{j};\n")
        css.write("}")

if __name__ == "__main__":
    file_name = input("File to store data: ")
    length = int(input("Enter number of pairs: "))
    for i in range(length):
        pairify(input(f"Enter key: "), input(f"Enter value: "))
    write(file_name)