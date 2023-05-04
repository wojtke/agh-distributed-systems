import sys

import Ice

Ice.loadSlice('./slice/Demo.ice')
import Demo


def main():
    with Ice.initialize(sys.argv, "./client_py/config.client") as communicator:
        properties = communicator.getProperties()
        endpoints = properties.getProperty("Demo.Endpoints")

        print(endpoints)

        while True:
            inp = input(">>> ")
            if inp == "":
                continue
            else:
                inp = inp.split()

            match inp:
                case ["quit"]:
                    communicator.destroy()
                    exit(0)

                case ["counter"]:
                    base = communicator.stringToProxy("global_counter:" + endpoints)
                    counter = Demo.GlobalCounterPrx.checkedCast(base)
                    value = counter.increment()
                    print(f"Counter value after incrementing: {value}")

                case ["note", "write", object_id, *data]:
                    base = communicator.stringToProxy(f"notepad/{object_id}:{endpoints}")
                    notepad = Demo.NotepadPrx.checkedCast(base)
                    notepad.write(" ".join(data))
                    print("Data written")

                case ["note", "read", object_id]:
                    base = communicator.stringToProxy(f"notepad/{object_id}:{endpoints}")
                    notepad = Demo.NotepadPrx.checkedCast(base)
                    result = notepad.read()
                    print(f"Data read:\n {result}")

                case ["parser", object_id, *data]:
                    base = communicator.stringToProxy(f"text_parser/{object_id}:{endpoints}")
                    parser = Demo.TextParserPrx.checkedCast(base)
                    count = parser.parse(" ".join(data))
                    print(f"Word count: {count}")

                case _:
                    print("Invalid command")
                    print("Available commands:")
                    print("  quit")
                    print("  counter")
                    print("  note write <object_id> <data>")
                    print("  note read <object_id>")
                    print("  parser <object_id> <data>")
                    print("")


if __name__ == "__main__":
    print("Client started...")
    main()
