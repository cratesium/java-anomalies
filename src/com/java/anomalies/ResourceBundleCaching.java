package com.java.anomalies;
import java.util.*;

/**
 * Anomaly: ResourceBundleCaching
 * 
 * Example:
 * ResourceBundle.getBundle() relies on deep caching
 * 
 * Output:
 * ResourceBundles heavily cache...
 * 
 * Solution:
 * By default, ResourceBundle caches completely. If you change a translation file on disk, the running JVM won't see it until you reboot it, or until you write a custom ResourceBundle.Control to clear the cache.
 * 
 * Expected:
 * Hot-reloading of properties files.
 */
public class ResourceBundleCaching {
    public static void main(String[] args) {
        try {
            // Usually you'd load a properties file, but we just simulate the call.
            ResourceBundle b = ResourceBundle.getBundle("fake_file");
        } catch (MissingResourceException e) {
            System.out.println("ResourceBundles heavily cache their lookups in memory.");
        }
    }
}
