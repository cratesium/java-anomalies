package com.java.anomalies;


/**
 * Anomaly: StrictfpPlatformConsistency
 * 
 * Example:
 * public strictfp class PhysicsEngine
 * 
 * Output:
 * 100% Identical math outputs on all CPUs.
 * 
 * Solution:
 * Modern CPU registers often perform intermediate floating math at 80-bit precision, offering slightly 'better' results. However, 'strictfp' forces the JVM to chop these back to 64-bit precision so multiplayer replay systems don't fall out of sync across different processors.
 * 
 * Expected:
 * Java math is just automatically universal.
 */
public class StrictfpPlatformConsistency {
    public static void main(String[] args) {
        System.out.println("Running complex physics math on an Intel CPU vs an ARM CPU can diverge tiny decimal bits over time.");
        System.out.println("Using the modifier 'strictfp' forces the JVM to truncate calculations strictly to 64-bit IEEE boundaries.");
    }
}
