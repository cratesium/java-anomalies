package com.java.anomalies;


/**
 * Anomaly: IdentityHashCodeAddress
 * 
 * Example:
 * System.identityHashCode()
 * 
 * Output:
 * Identity Hash: 2055281021
 * 
 * Solution:
 * It's a persistent myth that identityHashCode generates a real RAM address. In modern JVMs, it's typically just a randomly generated integer stored in the object's header. Real memory addresses change constantly during Garbage Collector relocation anyway!
 * 
 * Expected:
 * The physical memory address pointer for C-style interoperability.
 */
public class IdentityHashCodeAddress {
    public static void main(String[] args) {
        Object obj = new Object();
        // People assume this gives physical memory RAM addresses...
        int hash = System.identityHashCode(obj);
        System.out.println("Identity Hash: " + hash);
    }
}
