package com.java.anomalies;
import java.util.concurrent.*;

/**
 * Anomaly: ThreadLocalThreadLeak
 * 
 * Example:
 * ThreadLocal.set() without ThreadLocal.remove() in a ThreadPool
 * 
 * Output:
 * Set 10MB in ThreadLocal...
 * 
 * Solution:
 * When using Thread Pools (like Tomcat or standard Executors), threads are reused. If you set a ThreadLocal and forget to remove() it, that data lives on forever attached to that thread, causing massive memory leaks in web applications.
 * 
 * Expected:
 * ThreadLocal data dies when the specific task finishes.
 */
public class ThreadLocalThreadLeak {
    public static void main(String[] args) {
        // ThreadLocals are great for storing data specific to the current thread.
        ThreadLocal<byte[]> localCtx = new ThreadLocal<>();
        
        ExecutorService pool = Executors.newFixedThreadPool(1);
        pool.submit(() -> {
            localCtx.set(new byte[1024 * 1024 * 10]); // 10MB
            System.out.println("Set 10MB in ThreadLocal. If we don't call remove(), it stays forever in this pool thread!");
            // localCtx.remove(); <- FORGETTING THIS IS DEADLY
        });
        pool.shutdown();
    }
}
