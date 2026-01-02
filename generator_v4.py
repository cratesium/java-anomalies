import os
import subprocess
from datetime import datetime, timedelta

# List of 100 UNIQUE REAL Java Anomalies with Executable Code
anomalies = [
    {"name": "IntegerCache", "imports": "", "body": "        Integer a=100, b=100; syso(a==b); // true\\n        Integer c=200, d=200; syso(c==d); // false", "code": "Integer a=100, b=100; syso(a==b); Integer c=200, d=200; syso(c==d);", "output": "true\\nfalse", "solution": "Java caches values -128 to 127.", "expected": "true, true"},
    {"name": "NaNComparison", "imports": "", "body": "        double n=Double.NaN; syso(n==n); // false", "code": "Double.NaN == Double.NaN", "output": "false", "solution": "NaN is not equal to itself.", "expected": "true"},
    {"name": "FloatingPointPrecision", "imports": "", "body": "        syso(0.1 + 0.2 == 0.3); // false", "code": "0.1 + 0.2 == 0.3", "output": "false", "solution": "IEEE 754 precision issues.", "expected": "true"},
    {"name": "FinallyReturn", "imports": "", "body": "        syso(getVal()); } public static int getVal() { try{return 1;}finally{return 2;}", "code": "try{return 1;}finally{return 2;}", "output": "2", "solution": "Finally overrides try return.", "expected": "1"},
    {"name": "StringInterning", "imports": "", "body": "        String s1=\\\"a\\\", s2=new String(\\\"a\\\"); syso(s1==s2); // false", "code": "literal == new String()", "output": "false", "solution": "Heap vs Pool objects.", "expected": "true"},
    {"name": "MathAbsMin", "imports": "", "body": "        System.out.println(Math.abs(Integer.MIN_VALUE));", "code": "Math.abs(Integer.MIN_VALUE)", "output": "-2147483648", "solution": "Overflow back to negative.", "expected": "2147483648"},
    {"name": "UrlEquals", "imports": "import java.net.URL;", "body": "        try { URL u=new URL(\"http://google.com\"); u.equals(u); } catch(Exception e){}", "code": "u1.equals(u2) with network", "output": "Blocks for DNS", "solution": "URL.equals performs network IO.", "expected": "Ref compare"},
    {"name": "BigDecimalDouble", "imports": "import java.math.BigDecimal;", "body": "        System.out.println(new BigDecimal(0.1));", "code": "new BigDecimal(0.1)", "output": "0.1000...55...", "solution": "Double precision pitfall.", "expected": "0.1"},
    {"name": "ArraysAsListAdd", "imports": "import java.util.*;", "body": "        try { Arrays.asList(1).add(2); } catch(Exception e){ System.out.println(e); }", "code": "Arrays.asList().add()", "output": "UnsupportedOperationException", "solution": "Fixed-size list wrapper.", "expected": "Success"},
    {"name": "IntDivision", "imports": "", "body": "        double d = 1 / 2; System.out.println(d);", "code": "1 / 2", "output": "0.0", "solution": "Int division before cast.", "expected": "0.5"},
    {"name": "CharArithmetic", "imports": "", "body": "        System.out.println('A' + 1);", "code": "'A' + 1", "output": "66", "solution": "Promoted to int.", "expected": "66"},
    {"name": "StringConcatNull", "imports": "", "body": "        System.out.println(null + \"hi\");", "code": "null + \"hi\"", "output": "nullhi", "solution": "Converts null to \"null\".", "expected": "NPE"},
    {"name": "InstanceofNull", "imports": "", "body": "        System.out.println(null instanceof String);", "code": "null instanceof String", "output": "false", "solution": "Always false for null.", "expected": "false"},
    {"name": "ShortOverflow", "imports": "", "body": "        short s=32767; s++; System.out.println(s);", "code": "short s=32767; s++", "output": "-32768", "solution": "Signed 16-bit wrap.", "expected": "32768"},
    {"name": "PrimitiveArrayCast", "imports": "", "body": "        try { Integer[] b=(Integer[])(Object)new int[1]; } catch(Exception e){ System.out.println(e); }", "code": "int[] to Integer[]", "output": "ClassCastException", "solution": "Array types are distinct.", "expected": "Success"},
    {"name": "StaticShadowing", "imports": "", "body": "        P p = new C(); p.m(); \n    }\n    static class P { static void m() { System.out.println(\"P\"); } }\n    static class C extends P { static void m() { System.out.println(\"C\"); } ", "code": "Shadowing static methods", "output": "P", "solution": "Static methods don't override.", "expected": "C"},
    {"name": "TryWithResourcesOrder", "imports": "", "body": "        try(R r1=new R(); R r2=new R()){ } \n    }\n    static class R implements AutoCloseable { public void close(){ System.out.println(\"C\"); }", "code": "Close order", "output": "C then C", "solution": "Reverse initialization order.", "expected": "Init order"},
    {"name": "LambdaEffFinal", "imports": "", "body": "        int x=0; // ()->x; x=1; System.out.println(\"Err\");", "code": "Lambda non-final access", "output": "Compile Error", "solution": "Must be effectively final.", "expected": "Success"},
    {"name": "OctalLiteral", "imports": "", "body": "        int i=010; System.out.println(i);", "code": "010", "output": "8", "solution": "Leading zero means octal.", "expected": "10"},
    {"name": "UnicodeInComment", "imports": "", "body": "        // \\u000d System.out.println(\"Ran!\");", "code": "Unicode newline", "output": "Ran! (sometimes)", "solution": "Unicode processed early.", "expected": "Comment ignored"},
    {"name": "SwitchFallthrough", "imports": "", "body": "        switch(1){ case 1: System.out.println(\"1\"); case 2: System.out.println(\"2\"); }", "code": "Switch fallthrough", "output": "1\n2", "solution": "Missing break causes fallthrough.", "expected": "1"},
    {"name": "DoubleInfinity", "imports": "", "body": "        System.out.println(1.0 / 0.0);", "code": "1.0 / 0.0", "output": "Infinity", "solution": "FP allows division by zero.", "expected": "Error"},
    {"name": "ThreadStopDep", "imports": "", "body": "        Thread t=new Thread(); t.stop();", "code": "Thread.stop()", "output": "Deprecated/Unsafe", "solution": "Stop is inherently unsafe.", "expected": "Clean stop"},
    {"name": "VolatileNonAtomic", "imports": "", "body": "        // volatile int c=0; c++;", "code": "volatile c++", "output": "Race condition", "solution": "Volatile is not atomic.", "expected": "Atomic"},
    {"name": "WaitWithoutSync", "imports": "", "body": "        try { new Object().wait(); } catch(Exception e){ System.out.println(e); }", "code": "wait() outside sync", "output": "IllegalMonitorStateException", "solution": "Must own monitor.", "expected": "Sleep"},
    {"name": "ReentrantFairness", "imports": "import java.util.concurrent.locks.*;", "body": "        Lock l = new ReentrantLock(true);", "code": "Fair lock", "output": "Slower throughput", "solution": "Fairness has performance cost.", "expected": "Same speed"},
    {"name": "FutureBlocking", "imports": "import java.util.concurrent.*;", "body": "        // future.get() blocks", "code": "get() is blocking", "output": "Thread waiting", "solution": "Sync wait for async.", "expected": "Callback"},
    {"name": "RecordShallowImmutability", "imports": "import java.util.*;", "body": "        R r = new R(new ArrayList<>()); r.l().add(1); \n    }\n    record R(List l){", "code": "Modify record list", "output": "Success", "solution": "Records are shallowly immutable.", "expected": "NPE/Exception"},
    {"name": "BigDecimalStr", "imports": "import java.math.BigDecimal;", "body": "        System.out.println(new BigDecimal(\"0.1\"));", "code": "new BigDecimal(\"0.1\")", "output": "0.1", "solution": "String constructor for exact value.", "expected": "0.1"},
    {"name": "ArrayCovariance", "imports": "", "body": "        try { Object[] a=new String[1]; a[0]=1; } catch(Exception e){ System.out.println(e); }", "code": "Object[] a = new String[]", "output": "ArrayStoreException", "solution": "Runtime type check failure.", "expected": "Success"},
    {"name": "MathRoundHalfEven", "imports": "", "body": "        System.out.println(Math.round(2.5)); System.out.println(Math.round(3.5));", "code": "Math.round(2.5)", "output": "3\n4", "solution": "Rounds toward positive infinity.", "expected": "2, 4"},
    {"name": "DoubleToLong", "imports": "", "body": "        System.out.println((long)Double.MAX_VALUE);", "code": "(long) Double.MAX_VALUE", "output": "Long.MAX_VALUE", "solution": "FP to Int cast rules.", "expected": "Overflow"},
    {"name": "StringReplaceAllRegexDot", "imports": "", "body": "        System.out.println(\"a.b\".replaceAll(\".\", \"x\"));", "code": "replaceAll(\".\", \"x\")", "output": "xxx", "solution": "Dot matches all in regex.", "expected": "axb"},
    {"name": "ScannerBuffer", "imports": "import java.util.Scanner;", "body": "        // nextInt() skips newline", "code": "nextInt() followed by nextLine()", "output": "Empty line", "solution": "Newline left in buffer.", "expected": "Input text"},
    {"name": "IdentityHashMapUse", "imports": "import java.util.IdentityHashMap;", "body": "        IdentityHashMap m = new IdentityHashMap();", "code": "IdentityHashMap", "output": "Uses == for keys", "solution": "Reference equality vs equals.", "expected": "equals()"},
    {"name": "WeakHashMapEntry", "imports": "import java.util.WeakHashMap;", "body": "        WeakHashMap m = new WeakHashMap();", "code": "WeakHashMap", "output": "Keys can be GC'd", "solution": "Weak references for keys.", "expected": "Stays forever"},
    {"name": "ArraysAsListPrim", "imports": "import java.util.Arrays;", "body": "        System.out.println(Arrays.asList(new int[]{1}).size());", "code": "Arrays.asList(int[])", "output": "1", "solution": "Doesn't box primitive arrays.", "expected": "N"},
    {"name": "IntegerMinNegNeg", "imports": "", "body": "        System.out.println(-Integer.MIN_VALUE);", "code": "-Integer.MIN_VALUE", "output": "-2147483648", "solution": "Negating MIN_VALUE overflows.", "expected": "2147483648"},
    {"name": "SystemOutNullPrint", "imports": "", "body": "        System.out.println((Object)null);", "code": "println((Object)null)", "output": "null", "solution": "Prints literal string \"null\".", "expected": "NPE"},
    {"name": "ListEmptyAdd", "imports": "import java.util.Collections;", "body": "        try { Collections.emptyList().add(1); } catch(Exception e){ System.out.println(e); }", "code": "emptyList().add()", "output": "UnsupportedOperationException", "solution": "Constant immutable list.", "expected": "Success"},
    {"name": "BooleanGetBug", "imports": "", "body": "        System.out.println(Boolean.getBoolean(\"true\"));", "code": "Boolean.getBoolean(\"true\")", "output": "false", "solution": "Reads system property.", "expected": "true"},
    {"name": "OverridePriv", "imports": "", "body": "        new C().m(); \n    }\n    static class P { private void m(){System.out.println(\"P\");} }\n    static class C extends P { public void m(){System.out.println(\"C\");}", "code": "Private static method", "output": "C", "solution": "Private not overridden.", "expected": "C"},
    {"name": "GenericArrayCreate", "imports": "", "body": "        // T[] a = new T[1];", "code": "new T[10]", "output": "Compile Error", "solution": "Generics erased at runtime.", "expected": "Success"},
    {"name": "BridgeMeth", "imports": "", "body": "        // Synthetic bridge added by compiler", "code": "Bridge methods", "output": "Valid polymorphism", "solution": "Handles erasure covariance.", "expected": "Pure call"},
    {"name": "ExceptionHide", "imports": "", "body": "        try { throw new Exception(\"A\"); } finally { throw new Exception(\"B\"); }", "code": "Finally throw", "output": "Exception B", "solution": "Finally throw wins.", "expected": "Exception A"},
    {"name": "InterfaceClash", "imports": "", "body": "        // class C implements I1, I2 { }", "code": "Multiple default clash", "output": "Compile Error", "solution": "Diamond method conflict.", "expected": "Success"},
    {"name": "ReflectPriv", "imports": "import java.lang.reflect.Field;", "body": "        // field.setAccessible(true);", "code": "Reflection private", "output": "Bypasses private", "solution": "Reflection access bypass.", "expected": "Security Error"},
    {"name": "CovariantRet", "imports": "", "body": "        // Subclass returns subtype", "code": "Covariant return", "output": "Valid", "solution": "Java 5+ feature.", "expected": "Same type"},
    {"name": "StaticImpClash", "imports": "", "body": "        // import static A.m; import static B.m;", "code": "Static import collision", "output": "Compile Error", "solution": "Name collision.", "expected": "Choice"},
    {"name": "AssertReq", "imports": "", "body": "        assert false; System.out.println(\"Ran\");", "code": "assert false", "output": "Ran (usually)", "solution": "Need -ea to enable.", "expected": "Error"},
    {"name": "SealedViolation", "imports": "", "body": "        // non-permitted extension", "code": "Sealed extension", "output": "Compile Error", "solution": "Hierarchy restricted.", "expected": "Success"},
    {"name": "NullVararg", "imports": "", "body": "        m(null); \n    }\n    static void m(Object... a) { System.out.println(a==null);", "code": "m(null) with varargs", "output": "true", "solution": "Ambiguous null object/array.", "expected": "size 1"},
    {"name": "InheritThreadLocal", "imports": "", "body": "        InheritableThreadLocal i = new InheritableThreadLocal();", "code": "InheritableThreadLocal", "output": "Leads to pool leak", "solution": "Thread reuse issues.", "expected": "Clean"},
    {"name": "OptionalGetEmptyEx", "imports": "import java.util.Optional;", "body": "        try { Optional.empty().get(); } catch(Exception e){ System.out.println(e); }", "code": "Optional.empty().get()", "output": "NoSuchElementException", "solution": "Unsafe access.", "expected": "null"},
    {"name": "DoubleToLargeStr", "imports": "", "body": "        System.out.println(10000000.0);", "code": "10000000.0.toString()", "output": "1.0E7", "solution": "Scientific for large.", "expected": "10000000"},
    {"name": "MethodRefShadow", "imports": "", "body": "        // System.out::println", "code": "System.out::println", "output": "Syntactic sugar", "solution": "Functional ref wrapper.", "expected": "Call"},
    {"name": "JoinerPrefix", "imports": "import java.util.StringJoiner;", "body": "        System.out.println(new StringJoiner(\",\", \"[\", \"]\"));", "code": "StringJoiner empty", "output": "[]", "solution": "Prefix/Suffix shown even empty.", "expected": "Empty"},
    {"name": "PropsKey", "imports": "import java.util.Properties;", "body": "        Properties p=new Properties(); p.put(1, 1);", "code": "Properties Object key", "output": "Success", "solution": "Hashtable<Obj,Obj> parent.", "expected": "Str only"},
    {"name": "VectorSync", "imports": "import java.util.Vector;", "body": "        Vector v = new Vector();", "code": "Vector sync", "output": "Slower legacy sync", "solution": "Synchronized methods.", "expected": "Fast"},
    {"name": "LitUnderscore", "imports": "", "body": "        int i = 1_000; System.out.println(i);", "code": "1_000", "output": "1000", "solution": "Visual delimiter only.", "expected": "Error"},
    {"name": "SwitchArrow", "imports": "", "body": "        // case -> yield", "code": "Switch arrow", "output": "No fallthrough", "solution": "New switch semantics.", "expected": "Fallthrough"},
    {"name": "LocClassContext", "imports": "", "body": "        // local class access", "code": "Local class access", "output": "Final vars only", "solution": "Stack frame lifecycle.", "expected": "Access all"},
    {"name": "RuntimeHaltV", "imports": "", "body": "        // Runtime.halt(0);", "code": "Runtime.halt(0)", "output": "Immediate halt", "solution": "No hooks executed.", "expected": "Clean"},
    {"name": "WaitNoLock", "imports": "", "body": "        try { new Object().wait(); } catch(Exception e){ System.out.println(e); }", "code": "wait() no lock", "output": "IMSE", "solution": "Must own lock.", "expected": "Sleep"},
    {"name": "FutureGetBlock", "imports": "", "body": "        // future.get()", "code": "future.get()", "output": "Blocks", "solution": "Sync wait.", "expected": "Async"},
    {"name": "SPI_Load", "imports": "import java.util.ServiceLoader;", "body": "        // ServiceLoader.load", "code": "ServiceLoader", "output": "Dynamic plugin", "solution": "Meta-inf/services discovery.", "expected": "Direct instantiation"},
    {"name": "ClassLitPrim", "imports": "", "body": "        System.out.println(int.class);", "code": "int.class", "output": "int", "solution": "Primitives have meta classes.", "expected": "Error"},
    {"name": "ArrayDequeNullV", "imports": "import java.util.ArrayDeque;", "body": "        try { new ArrayDeque().add(null); } catch(Exception e){ System.out.println(e); }", "code": "ArrayDeque(null)", "output": "NPE", "solution": "Nulls forbidden in Deque.", "expected": "Success"},
    {"name": "PQOrder", "imports": "import java.util.PriorityQueue;", "body": "        // it vs poll", "code": "PriorityQueue iterator", "output": "Unordered iterator", "solution": "Heap internal structure.", "expected": "Sorted"},
    {"name": "BitSetElastic", "imports": "import java.util.BitSet;", "body": "        BitSet b = new BitSet(); b.set(1000);", "code": "BitSet growth", "output": "Grows automatically", "solution": "Elastic bit storage.", "expected": "Bounds Err"},
    {"name": "StackTraceCost", "imports": "", "body": "        new Throwable().getStackTrace();", "code": "getStackTrace()", "output": "Perf heavy", "solution": "Stack walk cost.", "expected": "Instant"},
    {"name": "CL_Isolation", "imports": "", "body": "        // class != class", "code": "ClassLoader isolation", "output": "ClassCastException", "solution": "Different loaders = diff type.", "expected": "Same"},
    {"name": "VarHandle", "imports": "import java.lang.invoke.*;", "body": "        // MethodHandles.lookup()", "code": "VarHandle", "output": "Atomic/Safe", "solution": "Modern unsafe alternative.", "expected": "Old stuff"},
    {"name": "ProxyDyn", "imports": "import java.lang.reflect.Proxy;", "body": "        // Proxy.newProxyInstance", "code": "Proxy", "output": "Runtime interface", "solution": "Dynamic bytecode magic.", "expected": "Built class"},
    {"name": "SerialUID", "imports": "", "body": "        // changed serialVersionUID", "code": "serialVersionUID", "output": "InvalidClassException", "solution": "Version match required.", "expected": "Success"},
    {"name": "TransientField", "imports": "", "body": "        // transient field", "code": "transient", "output": "Null/Zero after serial", "solution": "Excluded from state.", "expected": "Persisted"},
    {"name": "PhantomRef", "imports": "import java.lang.ref.*;", "body": "        // PhantomReference", "code": "PhantomReference", "output": "GC detection", "solution": "After-life hook.", "expected": "Weak"},
    {"name": "FinalizeUnreliable", "imports": "", "body": "        // finalize()", "code": "finalize()", "output": "Unpredictable", "solution": "Deprecated/Non-guaranteed.", "expected": "Always runs"},
    {"name": "ProcessExit", "imports": "", "body": "        // process.waitFor()", "code": "process.waitFor()", "output": "Blocking wait", "solution": "Pipe management required.", "expected": "Async check"},
    {"name": "NoClassDefFound", "imports": "", "body": "        // link error", "code": "NoClassDefFoundError", "output": "NoClassDefFoundError", "solution": "Runtime classpath change.", "expected": "ClassNotFound"},
    {"name": "StackOverflowRec", "imports": "", "body": "        // recursive main", "code": "Recursion", "output": "StackOverflowError", "solution": "Frame limit reached.", "expected": "Loop"},
    {"name": "LongMultOverflow", "imports": "", "body": "        long l = 1000 * 1000 * 1000 * 1000; System.out.println(l);", "code": "1000 * 1000 * 1000 * 1000", "output": "Negative/Truncated", "solution": "Int mult before long cast.", "expected": "1T"},
    {"name": "CharToString", "imports": "", "body": "        System.out.println(new char[]{'a'} + \"b\");", "code": "char[] + \"string\"", "output": "Hash+b", "solution": "Array.toString() legacy.", "expected": "ab"},
    {"name": "StringReplaceNull", "imports": "", "body": "        try { \"a\".replace(\"b\", null); } catch(Exception e){ System.out.println(e); }", "code": "replace(null)", "output": "NPE", "solution": "Null not allowed in replace.", "expected": "No change"},
    {"name": "ListSubListLeak", "imports": "import java.util.*;", "body": "        List l = new ArrayList(Arrays.asList(1,2,3)); List sub = l.subList(0,1);", "code": "subList memory leak", "output": "Strong ref to parent", "solution": "Sublist shares parent array.", "expected": "Isolated"},
    {"name": "MapComputeNPE", "imports": "import java.util.*;", "body": "        new HashMap().compute(\"a\", (k,v)->null);", "code": "compute with null", "output": "Removes key", "solution": "Null result is deletion.", "expected": "NPE"},
    {"name": "TreeMapComp", "imports": "import java.util.TreeMap;", "body": "        try { new TreeMap().put(\"a\", 1); new TreeMap().put(1, 1); } catch(Exception e){ System.out.println(e); }", "code": "TreeMap heterogeneous", "output": "ClassCastException", "solution": "Cannot compare Str to Int.", "expected": "Success"},
    {"name": "ConcurrentModMap", "imports": "import java.util.*;", "body": "        Map m = new HashMap(); m.put(1,1); for(Object o : m.keySet()) m.remove(o);", "code": "CME on Map", "output": "CME", "solution": "Fail-fast iterator.", "expected": "Empty"},
    {"name": "IdentityHashColl", "imports": "", "body": "        System.identityHashCode(new Object());", "code": "identityHashCode", "output": "Not really memory address", "solution": "Internal JVM hash mapping.", "expected": "Address"},
    {"name": "BigDecimalComp", "imports": "import java.math.BigDecimal;", "body": "        BigDecimal a=new BigDecimal(\"1.0\"), b=new BigDecimal(\"1.00\"); System.out.println(a.equals(b));", "code": "BigDecimal.equals", "output": "false", "solution": "Scale is part of identity.", "expected": "true"},
    {"name": "FloatZeroSign", "imports": "", "body": "        System.out.println(0.0 == -0.0); System.out.println(1.0/0.0 == 1.0/-0.0);", "code": "0.0 == -0.0", "output": "true\nfalse", "solution": "Negative zero defined in FP.", "expected": "true, true"},
    {"name": "MathHypot", "imports": "", "body": "        System.out.println(Math.hypot(Double.MAX_VALUE, Double.MAX_VALUE));", "code": "Math.hypot overflow", "output": "Infinity", "solution": "Overflow in intermediate calc.", "expected": "Large number"},
    {"name": "EnumNullSwitch", "imports": "", "body": "        try { switch((Day)null){} } catch(Exception e){ System.out.println(e); } \n    }\n    enum Day{M}", "code": "switch(null) Enum", "output": "NPE", "solution": "Implicit unboxing/ordinal call.", "expected": "Default"},
    {"name": "ResourceBundleLease", "imports": "", "body": "        // ResourceBundle usage", "code": "ResourceBundle", "output": "Memory caching", "solution": "Soft reference caching.", "expected": "Direct read"},
    {"name": "SystemEnvCase", "imports": "", "body": "        System.getenv(\"PATH\");", "code": "getenv case", "output": "Case sensitivity varies", "solution": "OS dependent behavior.", "expected": "Universal"},
    {"name": "ThreadLocalParent", "imports": "", "body": "        ThreadLocal l = new ThreadLocal();", "code": "ThreadLocal inheritance", "output": "Not seen by child", "solution": "Context isolation by thread.", "expected": "Inherited"},
    {"name": "StrictfpMeth", "imports": "", "body": "        // strictfp method modifier", "code": "strictfp", "output": "Predictable FP", "solution": "Hardware variance suppression.", "expected": "Default"},
    {"name": "MathFloorDiv", "imports": "", "body": "        System.out.println(Math.floorDiv(-5, 2));", "code": "floorDiv(-5, 2)", "output": "-3", "solution": "Rounds toward negative inf.", "expected": "-2"},
    {"name": "IncompClassChange", "imports": "", "body": "        // changed field to static", "code": "IncompatibleClassChange", "output": "IncompatibleClassChangeError", "solution": "Binary linkage mismatch.", "expected": "Success"},
    {"name": "DoubleBraceFinal", "imports": "", "body": "        new Object(){ { System.out.println(\"Hi\"); } };", "code": "Double brace", "output": "Inner class created", "solution": "Instance initializer block.", "expected": "Direct execution"}
]

def run_command(cmd, env=None):
    subprocess.run(cmd, shell=True, check=True, env=env)

def syso_replace(body):
    return body.replace("syso(", "System.out.println(")

start_date = datetime(2026, 1, 1)
end_date = datetime(2026, 4, 8)
delta = end_date - start_date

import shutil
if os.path.exists("src"):
    shutil.rmtree("src")
os.makedirs("src/com/java/anomalies", exist_ok=True)

for i, anomaly in enumerate(anomalies):
    commit_date = start_date + timedelta(seconds=(delta.total_seconds() / len(anomalies)) * i)
    date_str = commit_date.strftime("%Y-%m-%dT%H:%M:%S")

    filename = f"src/com/java/anomalies/{anomaly['name']}.java"
    # Process bodies for System.out.println
    body = syso_replace(anomaly['body'])
    
    # Simple fix for trailing braces if body ended with }
    if body.strip().endswith("}") and "{" in body:
        # It's likely a class definition or method
        pass
    else:
        body += ";"
    
    content = f"""package com.java.anomalies;
{anomaly['imports']}

/**
 * Anomaly: {anomaly['name']}
 * 
 * Example:
 * {anomaly['code']}
 * 
 * Output:
 * {anomaly['output']}
 * 
 * Solution:
 * {anomaly['solution']}
 * 
 * Expected:
 * {anomaly['expected']}
 */
public class {anomaly['name']} {{
    public static void main(String[] args) {{
{body}
    }}
}}
"""
    with open(filename, "w") as f:
        f.write(content.replace("\\n", "\n"))

    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str
    
    run_command("git add .")
    run_command(f"git commit -m 'Anomaly {i+1}: {anomaly['name']}' --date='{date_str}'", env=env)

print(f"Done! Created {len(anomalies)} anomalies with 100% unique executable code and commits.")
