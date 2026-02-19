package com.java.anomalies;


/**
 * Anomaly: RuntimeHaltDestructive
 * 
 * Example:
 * Runtime.getRuntime().halt(0)
 * 
 * Output:
 * If halt() ran, this finally block would NEVER execute.
 * 
 * Solution:
 * System.exit triggers a cascading shutdown sequence: locks sync, files close, and registered shutdown-hooks trigger. Halt bypasses the OS signal handlers entirely and kills the process instance without a trace. It is essentially an instant self-kill -9 command.
 * 
 * Expected:
 * Halt shuts down the system safely.
 */
public class RuntimeHaltDestructive {
    public static void main(String[] args) {
        try {
            System.out.println("System.exit(0) kindly executes all Thread shutdown hooks first.");
            System.out.println("Runtime.getRuntime().halt(0) detonates the JVM on the spot, discarding shutdown hooks! (Avoid this unless desperate).");
            // Runtime.getRuntime().halt(0);
        } finally {
            System.out.println("If halt() ran, this finally block would NEVER execute.");
        }
    }
}
