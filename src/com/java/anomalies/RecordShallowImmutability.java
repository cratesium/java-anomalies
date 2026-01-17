package com.java.anomalies;
import java.util.*;

/**
 * Anomaly: RecordShallowImmutability
 * 
 * Example:
 * Modify a list inside a Record
 * 
 * Output:
 * Success
 * 
 * Solution:
 * Records only ensure the *reference* cannot be changed. They do not automatically deep-freeze the objects they point to. If you want true immutability, pass a 'List.copyOf(list)' to the constructor.
 * 
 * Expected:
 * Some kind of Exception or compile error.
 */
public class RecordShallowImmutability {
    public static void main(String[] args) {
        List<String> list = new ArrayList<>();
        Data data = new Data(list);
        data.list().add("Modified!"); 
        System.out.println("Record content after modification: " + data.list());
    }
    record Data(List<String> list) {}
    static void dummy() {
    }
}
