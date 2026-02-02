package com.java.anomalies;
import java.lang.ref.*;

/**
 * Anomaly: PhantomReferenceQueue
 * 
 * Example:
 * PhantomReference usage
 * 
 * Output:
 * Phantom references let us know EXACTLY...
 * 
 * Solution:
 * Unlike Weak or Soft references, you cannot call .get() on a PhantomReference (it always returns null). Its sole purpose is to be enqueued when the object it points to is absolutely, positively destroyed—useful for safely scheduling off-heap memory cleanup.
 * 
 * Expected:
 * Just use finalize(). (Don't!)
 */
public class PhantomReferenceQueue {
    public static void main(String[] args) {
        Object bigObject = new Object();
        ReferenceQueue<Object> rq = new ReferenceQueue<>();
        PhantomReference<Object> phantom = new PhantomReference<>(bigObject, rq);
        
        bigObject = null;
        System.gc(); // Suggest garbage collection
        
        System.out.println("Phantom references let us know EXACTLY when an object has been annihilated by the GC.");
    }
}
