package com.java.anomalies;
import java.util.concurrent.*;

/**
 * Anomaly: InheritableThreadLocalLeak
 * 
 * Example:
 * new InheritableThreadLocal<>() with Executors
 * 
 * Output:
 * Potential massive security scope leaks.
 * 
 * Solution:
 * Inheriting context is useful for trace-IDs, but in pooled environments, a thread never truly 'dies'. If the pool assigns the thread to a completely different user's HTTP request later, it might still have Admin security credentials floating inside its InheritableThreadLocal.
 * 
 * Expected:
 * Clean state context.
 */
public class InheritableThreadLocalLeak {
    public static void main(String[] args) {
        System.out.println("InheritableThreadLocal passes parent thread data to newly spawned child threads.");
        System.out.println("But if you're using Executors, threads are dumped back into a pool, and the 'leaked' parent context persists for future jobs!");
    }
}
