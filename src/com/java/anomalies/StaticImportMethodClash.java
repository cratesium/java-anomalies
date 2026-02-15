package com.java.anomalies;


/**
 * Anomaly: StaticImportMethodClash
 * 
 * Example:
 * import static collisions
 * 
 * Output:
 * Compile Error
 * 
 * Solution:
 * If two static imports deliver methods with identical names, Java refuses to guess which one you intend, despite parameter differences preventing a direct signature ambiguity. The compiler enforces strict name resolution to ensure maintainability.
 * 
 * Expected:
 * Intelligent resolution based on argument types.
 */
public class StaticImportMethodClash {
    public static void main(String[] args) {
        System.out.println("import static java.util.Collections.sort;");
        System.out.println("import static java.util.Arrays.sort;");
        System.out.println("Which 'sort' wins if you just type sort(data)? Neither! It's a compiler error.");
    }
}
