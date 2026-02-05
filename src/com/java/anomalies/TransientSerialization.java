package com.java.anomalies;
import java.io.*;

/**
 * Anomaly: TransientSerialization
 * 
 * Example:
 * private transient String password;
 * 
 * Output:
 * Null/Zero upon loading
 * 
 * Solution:
 * The transient keyword acts as a privacy or memory-optimization flag. It tells Java not to bother writing that piece of data to disk. It's often used for passwords, temporary cache fields, or network sockets.
 * 
 * Expected:
 * Everything gets saved.
 */
public class TransientSerialization {
    public static void main(String[] args) {
        System.out.println("If a class implements Serializable, all its fields are saved to byte streams.");
        System.out.println("...Unless you mark the field 'transient'.");
        System.out.println("When deserialized, transient fields will just be null (or 0 for ints).");
    }
}
