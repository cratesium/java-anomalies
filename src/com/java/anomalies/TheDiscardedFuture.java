package com.java.anomalies;
import java.util.concurrent.*;

/**
 * Anomaly: TheDiscardedFuture
 * 
 * Example:
 * ExecutorService.submit() without checking Future
 * 
 * Output:
 * No error printed
 * 
 * Solution:
 * When using 'submit()', exceptions are swallowed by the Future. You only see them if you call 'future.get()'. If you want errors to print immediately, use 'execute()' instead.
 * 
 * Expected:
 * Application crash or error log.
 */
public class TheDiscardedFuture {
    public static void main(String[] args) {
        ExecutorService service = Executors.newSingleThreadExecutor();
        // If this task throws an exception, you'll never hear about it!
        service.submit(() -> {
            throw new RuntimeException("Invisible Error");
        });
        service.shutdown();
        System.out.println("Task submitted. If it died, we didn't see it.");
    }
}
