package com.java.anomalies;


/**
 * Anomaly: SystemPropertyParse
 * 
 * Example:
 * Boolean.getBoolean("true")
 * 
 * Output:
 * false\ntrue
 * 
 * Solution:
 * It's horribly misnamed! Boolean.getBoolean(String) actually reads a System Property (like something passed via -DmyProp=true) and checks if THAT is true. To parse a raw string, you must use parseBoolean().
 * 
 * Expected:
 * Boolean.getBoolean('true') to be true.
 */
public class SystemPropertyParse {
    public static void main(String[] args) {
        // People often think Boolean.getBoolean() parses a string to a boolean.
        String str = "true";
        System.out.println("Boolean.getBoolean('true') = " + Boolean.getBoolean(str));
        System.out.println("Boolean.parseBoolean('true') = " + Boolean.parseBoolean(str));
    }
}
