package com.java.anomalies;
import java.util.Optional;
import java.util.NoSuchElementException;

/**
 * Anomaly: OptionalGetUnsafe
 * 
 * Example:
 * Optional.empty().get()
 * 
 * Output:
 * And this is why you must check...
 * 
 * Solution:
 * Optional was introduced to fix NullPointerExceptions, but calling .get() directly on an empty optional throws a NoSuchElementException—you've just traded one crash for another. Always use .orElse(), .orElseGet(), or .ifPresent().
 * 
 * Expected:
 * It returns null.
 */
public class OptionalGetUnsafe {
    public static void main(String[] args) {
        Optional<String> emptyOp = Optional.empty();
        
        System.out.println("A lot of devs just call .get()...");
        try {
            String value = emptyOp.get();
        } catch (NoSuchElementException e) {
            System.out.println("And this is why you must check .isPresent() or use .orElse()!");
        }
    }
}
