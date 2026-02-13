package com.java.anomalies;


/**
 * Anomaly: SystemEnvCaseSensitivity
 * 
 * Example:
 * System.getenv("path")
 * 
 * Output:
 * Varies by OS structure.
 * 
 * Solution:
 * Java strives for 'Write Once, Run Anywhere'. However, System.getenv directly exposes the underlying Operating System's environment variables. Windows env vars are case-insensitive. Linux environments are strictly case-sensitive. This discrepancy breaks cross-platform scripts.
 * 
 * Expected:
 * Consistent behavior across operating systems.
 */
public class SystemEnvCaseSensitivity {
    public static void main(String[] args) {
        String homeCase1 = System.getenv("path");
        String homeCase2 = System.getenv("PATH");
        System.out.println("Depending on whether you run this on MacOS, Linux, or Windows, one of these may be null!");
    }
}
