package com.java.anomalies;
import java.util.concurrent.*;

/**
 * Anomaly: FutureGetIsBlocking
 * 
 * Example:
 * future.get()
 * 
 * Output:
 * Blocked Thread
 * 
 * Solution:
 * Using Future.get() turns your asynchronous code back into synchronous code. It's often better to use CompletableFuture and its 'thenAccept' callbacks to keep things truly async.
 * 
 * Expected:
 * An async callback mechanism.
 */
public class FutureGetIsBlocking {
    public static void main(String[] args) {
        // Don't be fooled by the async hype. .get() is synchronous.
        System.out.println("future.get() will stop this thread until the result is ready.");
    }
}
