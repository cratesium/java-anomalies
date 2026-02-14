package com.java.anomalies;


/**
 * Anomaly: IncompatibleClassChangeErrorExt
 * 
 * Example:
 * Library update altering class contract types
 * 
 * Output:
 * IncompatibleClassChangeError
 * 
 * Solution:
 * Binary compatibility means older compiled .class files must cleanly link with modern dependencies. An interface uses the 'invokeinterface' bytecode instruction, while an abstract class uses 'invokevirtual'. Altering the fundamental structure of a hierarchy snaps these bytecode linkages immediately.
 * 
 * Expected:
 * A clean runtime failure or NoSuchMethodException.
 */
public class IncompatibleClassChangeErrorExt {
    public static void main(String[] args) {
        System.out.println("If a class 'A' extends abstract class 'B'...");
        System.out.println("Then someone updates jar 'B' and changes that class to an interface...");
        System.out.println("JVM throws an IncompatibleClassChangeError the moment 'A' executes via bytecode.");
    }
}
