package com.java.anomalies;
import java.util.Properties;

/**
 * Anomaly: PropertiesNonStringKeys
 * 
 * Example:
 * Properties.put(Integer, Object)
 * 
 * Output:
 * ...throws ClassCastException internally.
 * 
 * Solution:
 * The Properties class is an ancient remnant of Java 1.0, wrongly structured via inheritance to inherit from Hashtable. It allows the smuggling of non-String primitives via .put(). However, its dedicated methods like .store() rely blindly on casting the values back to Strings, detonating on execution.
 * 
 * Expected:
 * Compile-time error forbidding non-Strings.
 */
public class PropertiesNonStringKeys {
    public static void main(String[] args) {
        Properties props = new Properties();
        // Since Properties extends Hashtable<Object, Object>, this is insanely legal:
        props.put(Integer.valueOf(1), new Object());
        
        System.out.println("Successfully smuggled non-strings into Properties!");
        try {
            // But when we try to save it to disk...
            // props.store(System.out, "Crash here"); 
            System.out.println("Trying to serialize this to a file throws ClassCastException internally.");
        } catch (Exception e) {}
    }
}
