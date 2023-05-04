module Demo {
  interface GlobalCounter {
    // singleton, stateful
    int increment();
  };

  interface Notepad {
    // stateful
    void write(string text);
    string read();
  };

  interface TextParser {
    // stateless
    int parse(string text);
  };
};