package com.java.anomalies;


/**
 * Anomaly: EnumOrdinalFragility
 * 
 * Example:
 * Enum.ordinal() saved to database
 * 
 * Output:
 * The DB saved ACTIVE as ordinal: 1\nIf we add 'NEW'...
 * 
 * Solution:
 * Never rely on enum.ordinal() for persistent storage or RPC data. If another developer rearranges the enum constants in the source file, all your database values will silently point to the wrong constants. Always save the enum.name() (as a string) instead.
 * 
 * Expected:
 * Using numbers is faster and saves DB space, so it seems like a good idea.
 */
public class EnumOrdinalFragility {
    public static void main(String[] args) {
        enum Status { PENDING, ACTIVE, INACTIVE }
        
        Status current = Status.ACTIVE;
        System.out.println("The DB saved ACTIVE as ordinal: " + current.ordinal());
        System.out.println("If we add 'NEW' at the top of the enum, ACTIVE becomes ordinal 2, breaking all our DB mappings!");
    }
}
