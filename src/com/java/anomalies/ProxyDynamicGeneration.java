package com.java.anomalies;
import java.lang.reflect.*;

/**
 * Anomaly: ProxyDynamicGeneration
 * 
 * Example:
 * Proxy.newProxyInstance()
 * 
 * Output:
 * Intercepted run() call!
 * 
 * Solution:
 * Dynamic proxies weave bytecode at runtime, creating an interceptor for an interface. It is the core magic behind frameworks like Spring AOP, allowing them to wrap your database calls with transactional boundaries automatically.
 * 
 * Expected:
 * You have to write a concrete `class MyRun implements Runnable`.
 */
public class ProxyDynamicGeneration {
    public static void main(String[] args) {
        System.out.println("Java lets you create classes that don't exist at compile time!");
        Runnable proxy = (Runnable) Proxy.newProxyInstance(
            ClassLoader.getSystemClassLoader(),
            new Class[]{Runnable.class},
            (proxyObj, method, argsProxy) -> {
                System.out.println("Intercepted run() call!");
                return null;
            }
        );
        proxy.run();
    }
}
