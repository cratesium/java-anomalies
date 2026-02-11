package com.java.anomalies;
import java.io.*;

/**
 * Anomaly: ProcessWaitForBlock
 * 
 * Example:
 * process.waitFor() without consuming streams
 * 
 * Output:
 * Indefinite hanging
 * 
 * Solution:
 * The OS only allocates a tiny buffer (like 8KB) for a process's standard output. If your Java code waits without continuously reading that output stream, the buffer fills up, and the OS freezes the child process indefinitely. A classic integration deadlock.
 * 
 * Expected:
 * Waits cleanly for the script to finish.
 */
public class ProcessWaitForBlock {
    public static void main(String[] args) {
        try {
            // We launch a script that dumps 10MB of text to the console...
            // Process p = Runtime.getRuntime().exec("heavy_script.sh");
            // p.waitFor();
            System.out.println("If you don't read the Process's InputStream, the process's pipe buffer fills up.");
        } catch (Exception e) { }
    }
}
