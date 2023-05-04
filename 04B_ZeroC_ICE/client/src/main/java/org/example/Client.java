package org.example;

import com.zeroc.Ice.Communicator;
import com.zeroc.Ice.ObjectPrx;
import com.zeroc.Ice.Properties;
import com.zeroc.Ice.Util;
import Demo.GlobalCounterPrx;
import Demo.NotepadPrx;
import Demo.TextParserPrx;

import java.util.Arrays;
import java.util.Scanner;

public class Client {

    private enum Command {
        QUIT, COUNTER, NOTE, PARSER
    }

    private static Communicator communicator;
    private static String endpoints;

    public static void main(String[] args) {
        communicator = Util.initialize(args, "config.client");
        Properties properties = communicator.getProperties();
        endpoints = properties.getProperty("Demo.Endpoints");

        System.out.println(endpoints);

        Scanner scanner = new Scanner(System.in);
        while (true) {
            System.out.print(">>> ");
            String input = scanner.nextLine();
            if (input.isEmpty()) {
                continue;
            }

            String[] parts = input.split(" ");
            Command command;
            try {
                command = Command.valueOf(parts[0].toUpperCase());
            } catch (IllegalArgumentException e) {
                printHelp();
                continue;
            }

            switch (command) {
                case QUIT:
                    quitCommand();
                    break;

                case COUNTER:
                    counterCommand();
                    break;

                case NOTE:
                    if (parts.length >= 3) {
                        noteCommand(parts[1], parts[2], Arrays.copyOfRange(parts, 3, parts.length));
                    }
                    break;

                case PARSER:
                    if (parts.length >= 2) {
                        parserCommand(parts[1], Arrays.copyOfRange(parts, 2, parts.length));
                    }
                    break;
            }
        }
    }

    private static void quitCommand() {
        communicator.destroy();
        System.exit(0);
    }

    private static void counterCommand() {
        GlobalCounterPrx counter = GlobalCounterPrx.checkedCast(
                communicator.stringToProxy("global_counter:" + endpoints));
        int value = counter.increment();
        System.out.println("Counter value after incrementing: " + value);
    }

    private static void noteCommand(String action, String objectId, String[] data) {
        ObjectPrx base = communicator.stringToProxy("notepad/" + objectId + ":" + endpoints);
        NotepadPrx notepad = NotepadPrx.checkedCast(base);
        if ("write".equals(action)) {
            notepad.write(String.join(" ", data));
            System.out.println("Data written");
        } else if ("read".equals(action)) {
            String result = notepad.read();
            System.out.println("Data read:\n" + result);
        }
    }

    private static void parserCommand(String objectId, String[] data) {
        TextParserPrx parser = TextParserPrx.checkedCast(
                communicator.stringToProxy("text_parser/" + objectId + ":" + endpoints));
        int count = parser.parse(String.join(" ", data));
        System.out.println("Word count: " + count);
    }

    private static void printHelp() {
        System.out.println("Invalid command");
        System.out.println("Available commands:");
        System.out.println("  quit");
        System.out.println("  counter");
        System.out.println("  note write <object_id> <data>");
        System.out.println("  note read <object_id>");
        System.out.println("  parser <object_id> <data>");
    }
}
