import sys

import Ice

Ice.loadSlice('./slice/Demo.ice')
import Demo


class GlobalCounterI(Demo.GlobalCounter):
    def __init__(self):
        self.count = 0
        print("GlobalCounter created")

    def increment(self, current=None):
        print("GlobalCounter - incrementing count:", self.count)
        self.count += 1
        return self.count


class NotepadI(Demo.Notepad):
    def __init__(self, name):
        self.notes = []
        self.name = name
        print(f"Notepad ({name}) created")

    def write(self, data, current=None):
        print(f"Notepad ({self.name}) - writing:", data)
        self.notes.append(data)

    def read(self, current=None):
        print(f"Notepad ({self.name}) - reading")
        return "\n".join(self.notes)


class NotepadLocator(Ice.ServantLocator):
    def __init__(self):
        self.servant_map = {}
        print("NotepadLocator created")

    def locate(self, current):
        print("NotepadLocator - locating servant")
        identity = current.id.name

        if identity not in self.servant_map:
            print(f"Creating new servant for identity: {identity}")
            self.servant_map[identity] = NotepadI(identity)

        return self.servant_map[identity]

    def finished(self, current, servant, cookie):
        print("NotepadLocator - finished")
        pass

    def deactivate(self, category):
        print("NotepadLocator deactivated")


class TextParserI(Demo.TextParser):
    def __init__(self, name="default"):
        self.name = name
        print(f"TextParser ({name}) created")

    def parse(self, text, current=None):
        print(f"TextParser ({self.name}) - parsing:", text)
        return len(text.split())


def main():
    with Ice.initialize(sys.argv, "./server/config.server") as communicator:
        adapter = communicator.createObjectAdapter("DemoAdapter")

        adapter.add(GlobalCounterI(), Ice.stringToIdentity("global_counter"))
        adapter.addServantLocator(NotepadLocator(), "notepad")

        adapter.add(TextParserI("p1"), Ice.stringToIdentity("text_parser/p1"))
        adapter.add(TextParserI("p2"), Ice.stringToIdentity("text_parser/p2"))

        adapter.addDefaultServant(TextParserI(), "text_parser")

        adapter.activate()
        communicator.waitForShutdown()


if __name__ == "__main__":
    print("Server started...")
    main()
