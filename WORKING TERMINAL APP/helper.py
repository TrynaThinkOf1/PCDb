import parser, writer
import os
from time import sleep
from main import mitochondria

class Database:
    def __init__(self, name):
        self.name = name
        self.file_path = os.path.expanduser(f"/WORKING TERMINAL APP/sys_func_main_log()/{name}.css")
        self.meta_data = None
        self.data = None

        if os.path.exists(self.file_path):
            self.meta_data, self.key_value_pairs, self.raw_data = parser.parse(self.name, mode="both")
        else:
            print(f"Database '{name}' does not exist.")
            mitochondria()

    #########################
    #      WRITE FUNCS      #
    #########################

    def overwrite(self, new_data, new_meta_data=None):
        if new_meta_data:
            self.meta_data = [item.strip() for item in self.meta_data.split(";") if item.strip()]
        writer.process(new_data)

        writer.write(self.name, new_meta_data)

    def remove(self, token=None, key=None):
        writer.remove(self.name, token=token, key=key)

    def append(self, token=None, kv=None):
        writer.append(self.name, token=token, kv=kv)

    def replace(self, tokens=None, old_key=None, new_kv=None):
        writer.replace(self.name, token=tokens, old_key=old_key, new_kv=new_kv)

    #########################
    #       READ FUNCS      #
    #########################

    def parse(self, mode="raw"):
        return parser.parse(self.name, mode=mode)

    def query(self, query):
        return parser.parse(self.name, None, query=query)

def create_new_database():
    os.system("clear")
    database_name = input("Enter database name: ").strip()
    database_path = os.path.expanduser(f"/WORKING TERMINAL APP/sys_func_main_log()/{database_name}.css")
    if not os.path.exists(database_path):
        print("\nMETA DATA OPTIONS: D_NAME, D_VERSION, D_DC, D_DESC")
        meta_data = input("\nEnter meta data (separated by ;, leave empty if none): ")
        try:
            with open(database_path, 'w') as db_file:
                meta_items = [f"  --{item.split('=')[0].strip()}: {item.split('=')[1].strip()};\n" for item in meta_data.split(";") if "=" in item]
                db_file.write(".META_DATA {\n")
                db_file.writelines(meta_items)
                db_file.write("}\n")
                db_file.write(".key_value_pairs {\n}\n")
                db_file.write(".raw_data {\n}\n")

            percent = 0
            for i in range(10):
                os.system("clear")
                print(f"{percent}% -> [{'#' * percent}{' ' * (10 - percent)}]")
                sleep(0.25)
                percent += 10
            os.system("clear")
            print("Database Created Successfully!")
            sleep(1.5)
            os.system("clear")
            mitochondria()
        except Exception as e:
            print(e)
    else:
        print("Database already exists.")
        mitochondria()

def view_databases():
    os.system("clear")
    for file in os.listdir(os.path.expanduser("/WORKING TERMINAL APP/sys_func_main_log()/")):
        if file.endswith(".css"):
            print(file.removesuffix(".css"))
    print("\n========================================\n")
    choice = input("> ")
    if choice not in ["back", "2"]:
        manage_database(choice)
    else:
        os.system("clear")
        mitochondria()

def manage_database(database):
    db_instance = Database(database)

    os.system("clear")
    print(f"Database: {database}\n\n")
    print("1) Overwrite Database")
    print("2) Remove Data")
    print("3) Append Data")
    print("4) Replace Data")
    print("5) Parse Database")
    print("6) Query Database")
    print("7) Back")
    choice = input("> ")
    if choice == "1":
        os.system("clear")
        print("\nMETA DATA OPTIONS: D_NAME, D_VERSION, D_DC, D_DESC")
        meta_data = input("\nEnter new meta data (separated by ;, leave empty if none): ")
        print("\nDATA FORMAT: {key:value}; raw data; {another key:another value}")
        data = input("\nEnter new data: ")
        try:
            db_instance.overwrite(data, meta_data)
            percent = 0
            for i in range(10):
                os.system("clear")
                print(f"{percent}% -> [{'#' * percent}{' ' * (10 - percent)}]")
                sleep(0.25)
                percent += 10
            os.system("clear")
            print("Database Overwritten Successfully!")
            sleep(1.5)
            os.system("clear")
            mitochondria()
        except Exception as e:
            print(e)
        input("Press Enter to Return to Main Menu...\n")
        os.system("clear")
        mitochondria()
    elif choice == "2":
        os.system("clear")
        print("1) Remove Data by Token")
        print("2) Remove Data by Key")
        choice = input("> ")
        if choice == "1":
            token = input("Enter token to remove: ")
            db_instance.remove(token=token)
        elif choice == "2":
            key = input("Enter key to remove: ")
            db_instance.remove(key=key)
        else:
            print("Invalid choice.")
            manage_database(database)
        input("Press Enter to Return to Main Menu...\n")
        os.system("clear")
        mitochondria()
    elif choice == "3":
        os.system("clear")
        print("1) Append Raw Data")
        print("2) Append Key:Value Pair")
        choice = input("> ")
        if choice == "1":
            token = input("Enter token to append: ")
            db_instance.append(token=token)
        elif choice == "2":
            kv = input("Enter key:value pair to append: ")
            db_instance.append(kv=kv)
        else:
            print("Invalid choice.")
            manage_database(database)
        input("Press Enter to Return to Main Menu...\n")
        os.system("clear")
        mitochondria()
    elif choice == "4":
        os.system("clear")
        print("1) Replace Raw Data")
        print("2) Replace Key:Value Pair")
        choice = input("> ")
        if choice == "1":
            old_token = input("Enter token to replace: ")
            new_token = input("Enter new token: ")
            db_instance.replace(tokens=(old_token + ':' + new_token))
        elif choice == "2":
            old_key = input("Enter key to replace: ")
            new_kv = input("Enter new key:value pair: ")
            db_instance.replace(old_key=old_key, new_kv=new_kv)
        input("Press Enter to Return to Main Menu...\n")
        os.system("clear")
        mitochondria()
    elif choice == "5":
        os.system("clear")
        print("1) Parse Raw Data")
        print("2) Parse Key:Value Pairs")
        print("3) BOTH")
        choice = input("> ")
        if choice == "1":
            meta, raw = db_instance.parse(mode="raw")
            print(f"\nMETA DATA:\n{meta}\n\nRAW DATA:\n{raw}")
        elif choice == "2":
            meta, kvp = db_instance.parse(mode="kvp")
            print(f"\nMETA DATA:\n{meta}\n\nKEY VALUE PAIRS:\n{kvp}")
        elif choice == "3":
            meta, kvp, raw = db_instance.parse(mode="both")
            print(f"\nMETA DATA:\n{meta}\n\nKEY VALUE PAIRS:\n{kvp}\n\nRAW DATA:\n{raw}")
        else:
            print("Invalid choice.")
            manage_database(database)
        input("Press Enter to Return to Main Menu...\n")
        os.system("clear")
        mitochondria()
    elif choice == "6":
        os.system("clear")
        query = input("Enter key to query: ")
        if isinstance(db_instance.query(query), tuple):
            key, value = db_instance.query(query)
            print(f"\nKey: {key} \nValue: {value}")
        else:
            print(db_instance.query(query))
        input("Press Enter to Return to Main Menu...\n")
        os.system("clear")
        mitochondria()
    elif choice == "7":
        os.system("clear")
        mitochondria()
    else:
        print("Invalid choice")
        manage_database(database)

if __name__ == "__main__":
    pass