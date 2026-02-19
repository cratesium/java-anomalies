package com.java.anomalies;
import java.util.ServiceLoader;

/**
 * Anomaly: ServiceLoaderDiscovery
 * 
 * Example:
 * ServiceLoader.load(Driver.class)
 * 
 * Output:
 * Dynamically bridges remote plugins without code links.
 * 
 * Solution:
 * JDBC database connections use this heavily. When you load the Postgres JAR, the JVM scans its META-INF file, finds the 'org.postgres.Driver' declaration, and uses ServiceLoader to instantiate it without you ever importing postgres packages directly.
 * 
 * Expected:
 * Hardcoded instantiation via 'new PostgresDriver()'
 */
public class ServiceLoaderDiscovery {
    public static void main(String[] args) {
        System.out.println("Interfaces can be implemented by entirely detached JARs at runtime.");
        System.out.println("ServiceLoader reads the META-INF/services/ file in your classpath and auto-injects all known implementations seamlessly.");
    }
}
