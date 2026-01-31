package com.java.anomalies;
import java.io.*;

/**
 * Anomaly: SerializationUIDMismatch
 * 
 * Example:
 * Not defining serialVersionUID
 * 
 * Output:
 * InvalidClassException on update
 * 
 * Solution:
 * When Java serializes an object, it calculates a hash of the class structure. If you don't explicitly define `private static final long serialVersionUID = 1L;`, the compiler generates one entirely based on the fields and methods. Any change breaks compatibility.
 * 
 * Expected:
 * I can just add new fields and older serialized data will leave them null.
 */
public class SerializationUIDMismatch {
    public static void main(String[] args) {
        System.out.println("If you serialize a class, then add a field to it without setting a static serialVersionUID...");
        System.out.println("Deserializing the old bytes will throw an InvalidClassException!");
    }
}
