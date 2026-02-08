package com.java.anomalies;
import java.util.Scanner; import java.io.ByteArrayInputStream;

/**
 * Anomaly: ScannerSkipNewline
 * 
 * Example:
 * sc.nextInt(); sc.nextLine();
 * 
 * Output:
 * Number was: 42\nText was: ''
 * 
 * Solution:
 * nextInt() reads the integer but completely ignores the \n character trailing it. The very next call to nextLine() instantly consumes that leftover \n, returning a blank string. Always do an extra dummy `sc.nextLine()` after picking up ints from console input.
 * 
 * Expected:
 * Text was: 'Hello World'
 */
public class ScannerSkipNewline {
    public static void main(String[] args) {
        String input = "42\\nHello World\\n";
        Scanner sc = new Scanner(new ByteArrayInputStream(input.getBytes()));
        
        int number = sc.nextInt();
        String text = sc.nextLine();
        
        System.out.println("Number was: " + number);
        System.out.println("Text was: '" + text + "'");
    }
}
