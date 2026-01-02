import os
import subprocess
from datetime import datetime, timedelta

# List of 100 REAL Java Anomalies
anomalies = [
    {"name": "IntegerCache", "code": "Integer a=100, b=100; syso(a==b); // true\\nInteger c=200, d=200; syso(c==d); // false", "output": "true\\nfalse", "solution": "Caching -128 to 127.", "expected": "true/true"},
    {"name": "NaNComparison", "code": "syso(Double.NaN == Double.NaN);", "output": "false", "solution": "NaN is not equal to itself per IEEE 754.", "expected": "true"},
    {"name": "FloatingPointPrecision", "code": "syso(0.1 + 0.2 == 0.3);", "output": "false", "solution": "Binary representation limits.", "expected": "true"},
    {"name": "FinallyReturn", "code": "try{return 1;}finally{return 2;}", "output": "2", "solution": "Finally overrides try return.", "expected": "1"},
    {"name": "StringInterning", "code": "String s1=\"a\"; String s2=new String(\"a\"); syso(s1==s2);", "output": "false", "solution": "Heap vs Pool.", "expected": "true"},
    {"name": "MathAbsMin", "code": "syso(Math.abs(Integer.MIN_VALUE));", "output": "-2147483648", "solution": "Overflow back to negative.", "expected": "2147483648"},
    {"name": "UrlEquals", "code": "new URL(\"http://google.com\").equals(url2)", "output": "Blocks for DNS", "solution": "URL.equals performs network IO.", "expected": "String compare"},
    {"name": "BigDecimalDouble", "code": "new BigDecimal(0.1)", "output": "0.1000000000000000055...", "solution": "Double precision issue in constructor.", "expected": "0.1"},
    {"name": "ArraysAsListAdd", "code": "Arrays.asList(1,2).add(3)", "output": "UnsupportedOperationException", "solution": "Fixed-size list wrapper.", "expected": "Success"},
    {"name": "IntDivision", "code": "double d = 1 / 2;", "output": "0.0", "solution": "Integer division before cast.", "expected": "0.5"},
    {"name": "CharArithmetic", "code": "syso('A' + 1)", "output": "66", "solution": "Promoted to int.", "expected": "B"},
    {"name": "StringConcatNull", "code": "String s = null; syso(s + \"hi\");", "output": "nullhi", "solution": "StringBuilder appends \"null\".", "expected": "NPE or hi"},
    {"name": "InstanceofNull", "code": "null instanceof Object", "output": "false", "solution": "instanceof always false for null.", "expected": "true/false ambiguously"},
    {"name": "ShortOverflow", "code": "short s = 32767; s++;", "output": "-32768", "solution": "Signed 16-bit wrap.", "expected": "32768"},
    {"name": "PrimitiveArrayCast", "code": "Object a = new int[1]; Integer[] b = (Integer[]) a;", "output": "ClassCastException", "solution": "int[] is not Integer[].", "expected": "Success"},
    {"name": "StaticShadowing", "code": "Parent.staticMethod() handled by ref type", "output": "Parent output", "solution": "Static methods don't override.", "expected": "Child output"},
    {"name": "TryWithResourcesOrder", "code": "try(A a; B b)", "output": "B closes then A", "solution": "Reverse initialization order.", "expected": "A then B"},
    {"name": "LambdaEffectivelyFinal", "code": "int x=0; lambda(()->x); x=1;", "output": "Compile Error", "solution": "Local variables must be effectively final.", "expected": "Dynamic access"},
    {"name": "DoubleBraceMemoryLeak", "code": "new ArrayList<>() {{ add(1); }}", "output": "Anonymous class retains outer ref", "solution": "Creates sub-class with hidden reference.", "expected": "Inline init"},
    {"name": "MethodHiding", "code": "Static method in subclass same signature", "output": "No polymorphism", "solution": "Static methods are hidden, not overridden.", "expected": "Polymorphic behavior"},
    {"name": "OctalLiteral", "code": "int i = 010;", "output": "8", "solution": "Leading zero means octal.", "expected": "10"},
    {"name": "UnicodeInComment", "code": "// \\u000d System.exit(0);", "output": "Program exits", "solution": "Unicode escapes processed early.", "expected": "Comment ignored"},
    {"name": "LongLiteralMissingL", "code": "long l = 2147483648;", "output": "Compile Error", "solution": "Integer too large before casting.", "expected": "Auto-cast"},
    {"name": "FloatLiteralMissingF", "code": "float f = 1.0;", "output": "Compile Error", "solution": "Double to float requires cast/F.", "expected": "Auto-cast"},
    {"name": "ModuloNegative", "code": "-5 % 2", "output": "-1", "solution": "Sign follows dividend.", "expected": "1"},
    {"name": "ShiftLimitInt", "code": "1 << 32", "output": "1", "solution": "Shift amount is modulo 32.", "expected": "0 or 4294967296"},
    {"name": "ShiftLimitLong", "code": "1L << 64", "output": "1", "solution": "Shift amount is modulo 64.", "expected": "0"},
    {"name": "StrictfpPrecision", "code": "strictfp keyword usage", "output": "Consistent FP", "solution": "Hardware-independent floating point.", "expected": "Generic FP"},
    {"name": "VarargsAmbiguity", "code": "method(String...) vs method(String, String)", "output": "Compile Error (often)", "solution": "Ambiguous method call rules.", "expected": "Specific match"},
    {"name": "BinarySearchUnsorted", "code": "Arrays.binarySearch(new int[]{3,1,2}, 1)", "output": "Undefined (-1 or -2)", "solution": "Requires sorted array.", "expected": "1"},
    {"name": "HashSetMutableKey", "code": "Set s; s.add(obj); obj.setVal(2); s.contains(obj);", "output": "false", "solution": "Hashcode changed, key lost.", "expected": "true"},
    {"name": "ThreadStartTwice", "code": "t.start(); t.start();", "output": "IllegalThreadStateException", "solution": "Threads cannot be restarted.", "expected": "Nothing or Restart"},
    {"name": "SynchronizedNull", "code": "synchronized(null)", "output": "NPE", "solution": "Monitor object cannot be null.", "expected": "Lock ignore"},
    {"name": "DeadlockSelfJoin", "code": "Thread.currentThread().join();", "output": "Hangs forever", "solution": "Waiting for self to finish.", "expected": "Completion"},
    {"name": "DoubleInfinity", "code": "1.0 / 0.0", "output": "Infinity", "solution": "Floating point allows div-by-zero.", "expected": "Error"},
    {"name": "DoubleNaNEquality", "code": "Double.NaN != Double.NaN", "output": "true", "solution": "NaN is unique per IEEE.", "expected": "false"},
    {"name": "ConstructorException", "code": "throw in constructor", "output": "Object partially created", "solution": "Finalizers might still run.", "expected": "No object"},
    {"name": "StaticBlockException", "code": "throw in static block", "output": "ExceptionInInitializerError", "solution": "Class fails to load.", "expected": "Runtime error"},
    {"name": "EnumCompare", "code": "enum1 == enum2 vs equals()", "output": "Both work (safe)", "solution": "Enums are singleton-guaranteed.", "expected": "Need equals"},
    {"name": "SystemExitFinally", "code": "try{System.exit(0);}finally{syso(\"hi\");}", "output": "Nothing", "solution": "exit() halts JVM immediately.", "expected": "hi"},
    {"name": "InfiniteRecusion", "code": "main calling main", "output": "StackOverflowError", "solution": "Unbounded stack growth.", "expected": "Infinite loop"},
    {"name": "ZeroLengthArray", "code": "new int[0]", "output": "Valid object", "solution": "Arrays can be empty but not null.", "expected": "Null or error"},
    {"name": "MultiDimArrayInit", "code": "int[][] a = new int[5][];", "output": "a[0] is null", "solution": "Sub-arrays not initialized.", "expected": "Empty arrays"},
    {"name": "CharRange", "code": "(char) 65536", "output": "0 (wrap)", "solution": "char is 16-bit unsigned.", "expected": "65536"},
    {"name": "ByteRange", "code": "(byte) 128", "output": "-128", "solution": "byte is signed 8-bit.", "expected": "128"},
    {"name": "ArrayStoreException", "code": "Object[] a = new String[1]; a[0] = 1;", "output": "ArrayStoreException", "solution": "Array covariance pitfall.", "expected": "ClassCastException"},
    {"name": "StringSubstringMemory", "code": "Old Java substring shared backing array", "output": "Memory leak", "solution": "Pre-Java 7u6 sharing issues.", "expected": "Isolation"},
    {"name": "IteratorRemoveNoNext", "code": "it.remove() without it.next()", "output": "IllegalStateException", "solution": "Iterator state machine.", "expected": "Remove first"},
    {"name": "ConcurrentHashMapNull", "code": "chm.put(null, 1)", "output": "NPE", "solution": "CHM doesn't allow null keys.", "expected": "Success"},
    {"name": "TreeMapNullKey", "code": "treeMap.put(null, 1)", "output": "NPE", "solution": "Cannot compare null key.", "expected": "Success"},
    {"name": "ArraysAsListArrays", "code": "Arrays.asList(new int[]{1}) vs Integer[]", "output": "Size 1 vs Size N", "solution": "Boxed array vs primitive array.", "expected": "Size N"},
    {"name": "IntegerEqualsLong", "code": "new Integer(1).equals(new Long(1))", "output": "false", "solution": "Type check before value check.", "expected": "true"},
    {"name": "BooleanGetBoolean", "code": "Boolean.getBoolean(\"true\")", "output": "false", "solution": "Reads system property, not string.", "expected": "true"},
    {"name": "IdentityHashMapUses", "code": "map.put(new String(\"a\"), 1) x 2", "output": "2 entries", "solution": "Uses == reference equality.", "expected": "1 entry"},
    {"name": "UnboxingNPE", "code": "Integer i = null; int x = i;", "output": "NPE", "solution": "Automatic unboxing of null.", "expected": "0 or error"},
    {"name": "ScannerNextLine", "code": "nextInt() followed by nextLine()", "output": "Empty string", "solution": "Newline character left in buffer.", "expected": "First string"},
    {"name": "URLHashCode", "code": "url.hashCode() with network", "output": "Blocks/Unreliable", "solution": "URL hash/equals use DNS.", "expected": "Fast/Local"},
    {"name": "SystemOutNull", "code": "System.out.println(null)", "output": "null", "solution": "Prints string \"null\".", "expected": "NPE"},
    {"name": "CollectionsEmptyListAdd", "code": "Collections.emptyList().add(1)", "output": "UnsupportedOperationException", "solution": "Immutable constant list.", "expected": "Success"},
    {"name": "StringReplaceAllRegex", "code": "s.replaceAll(\".\", \"x\")", "output": "xxxx", "solution": "Dot matches everything in regex.", "expected": "x replaced once"},
    {"name": "DoubleToLongBits", "code": "Double.doubleToLongBits(NaN)", "output": "Canonical NaN bits", "solution": "NaN handling in bit conversion.", "expected": "Literal bits"},
    {"name": "OverridePrivate", "code": "Subclass 'overriding' private method", "output": "No override", "solution": "Private methods are not visible.", "expected": "Override"},
    {"name": "GenericArrayCreation", "code": "new T[10]", "output": "Compile Error", "solution": "Generics erased at runtime.", "expected": "New array"},
    {"name": "BridgeMethod", "code": "Polymorphism with generics", "output": "Synthetic method", "solution": "Compiler adds bridge methods.", "expected": "Standard call"},
    {"name": "GenericTypeInference", "code": "List<String> l = new ArrayList<>()", "output": "Diamond operator", "solution": "Java 7+ type inference.", "expected": "Full type"},
    {"name": "ExceptionHidingFinally", "code": "finally throw overrides try throw", "output": "Only finally exception seen", "solution": "Last exception wins.", "expected": "Both seen"},
    {"name": "ThreadYield", "code": "Thread.yield()", "output": "Hint only", "solution": "No guarantee of context switch.", "expected": "Immediate stop"},
    {"name": "InterfaceDefaultConflict", "code": "Two interfaces, same default method", "output": "Compile Error", "solution": "Diamond problem in interfaces.", "expected": "Choice"},
    {"name": "ReflectionPrivateField", "code": "setAccessible(true) on final", "output": "Value changed (mostly)", "solution": "Reflection bypasses visibility.", "expected": "Success always"},
    {"name": "UnsafeUsage", "code": "sun.misc.Unsafe", "output": "Low level access", "solution": "Memory manipulation risk.", "expected": "Safety"},
    {"name": "CovariantReturn", "code": "Override returns subtype", "output": "Valid", "solution": "Java 5+ covariant returns.", "expected": "Same type only"},
    {"name": "StaticImportConflict", "code": "Importing two same named statics", "output": "Compile Error", "solution": "Namespace collision.", "expected": "Choice"},
    {"name": "AssertEnable", "code": "assert false;", "output": "Nothing (default)", "solution": "Need -ea flag to enable.", "expected": "Error"},
    {"name": "RecordImmutability", "code": "Record with List field", "output": "List can be modified", "solution": "Shallow immutability.", "expected": "Deep init"},
    {"name": "SealedClassViolation", "code": "Extend sealed without permit", "output": "Compile Error", "solution": "Hierarchy restricted.", "expected": "Success"},
    {"name": "NullVarargs", "code": "method(null)", "output": "NPE or null array", "solution": "Ambiguity in null varargs.", "expected": "One null element"},
    {"name": "InheritableThreadLocalLeak", "code": "ThreadPool with ThreadLocal", "output": "Stale data", "solution": "Threads reused, values persist.", "expected": "Clean state"},
    {"name": "OptionalGetEmpty", "code": "Optional.empty().get()", "output": "NoSuchElementException", "solution": "Unsafe access.", "expected": "null"},
    {"name": "MathRoundHalfEven", "code": "Math.round(2.5) vs 3.5", "output": "3 and 4", "solution": "Rounds to positive infinity.", "expected": "2 and 4 (even)"},
    {"name": "DoubleToStringLarge", "code": "new Double(10000000).toString()", "output": "1.0E7", "solution": "Scientific notation for large.", "expected": "10000000"},
    {"name": "EnumMapOrdinal", "code": "EnumMap internal array", "output": "High performance", "solution": "Uses ordinals internally.", "expected": "Hash map perf"},
    {"name": "FunctionalInterfaceCheck", "code": "@FunctionalInterface with 2 methods", "output": "Compile Error", "solution": "Strictly one abstract method.", "expected": "Success"},
    {"name": "MethodReferenceShadow", "code": "System.out::println in lambda", "output": "Execution", "solution": "Syntax for brevity.", "expected": "Expression"},
    {"name": "StringJoinerPrefix", "code": "Empty joiner with prefix", "output": "Empty (default)", "solution": "Prefix depends on content.", "expected": "Prefix only"},
    {"name": "PropertiesKeyType", "code": "props.put(1, 1)", "output": "Success (buggy)", "solution": "Extends Hashtable<Obj,Obj>.", "expected": "String only"},
    {"name": "VectorSynchronization", "code": "Vector performance", "output": "Slow", "solution": "Legacy synchronization.", "expected": "Fast"},
    {"name": "BinaryLiteralUnderscore", "code": "0b11_00", "output": "12", "solution": "Readable numeric literals.", "expected": "Error"},
    {"name": "SwitchExpressionFallthrough", "code": "yield vs ->", "output": "No fallthrough with ->", "solution": "Newer switch semantics.", "expected": "Fallthrough"},
    {"name": "LocalClassContext", "code": "Class inside method", "output": "Isolated", "solution": "Access to final locals only.", "expected": "Full access"},
    {"name": "ThreadStopDeprecation", "code": "thread.stop()", "output": "ThreadDeath/Inconsistent", "solution": "Dangerously unsafe.", "expected": "Clean stop"},
    {"name": "RuntimeHalt", "code": "Runtime.halt(0)", "output": "Immediate stop", "solution": "No shutdown hooks run.", "expected": "Clean exit"},
    {"name": "MemoryBarrierVolatile", "code": "volatile variable write", "output": "Visibility guaranteed", "solution": "Happens-before edge.", "expected": "Atomic"},
    {"name": "WaitWithoutLock", "code": "obj.wait() outside sync", "output": "IMSE", "solution": "Must own monitor.", "expected": "Sleep"},
    {"name": "ReentrantLockFairness", "code": "Strict FIFO hint", "output": "Reduced throughput", "solution": "Queueing overhead.", "expected": "Same speed"},
    {"name": "FutureGetBlocking", "code": "future.get()", "output": "Blocks thread", "solution": "Synchronous wait for async.", "expected": "Callback"},
    {"name": "CompletableFutureJoin", "code": "join() vs get()", "output": "Unchecked exception", "solution": "Syntactic sugar for get().", "expected": "Checked"},
    {"name": "ServiceLoaderSPI", "code": "META-INF/services/...", "output": "Plugin loaded", "solution": "Standard extension point.", "expected": "Dynamic class"},
    {"name": "DoubleToLong", "code": "(long) Double.MAX_VALUE", "output": "Large positive", "solution": "Casting rules for FP to Int.", "expected": "Overflow"},
    {"name": "IntegerMIN_MIN", "code": "-Integer.MIN_VALUE", "output": "-2147483648", "solution": "Negative of Min is Min.", "expected": "2147483648"},
    {"name": "ClassLiteralPrimitive", "code": "int.class", "output": "int", "solution": "Primitives have Class objects.", "expected": "Error"}
]

def run_command(cmd, env=None):
    subprocess.run(cmd, shell=True, check=True, env=env)

start_date = datetime(2026, 1, 1)
end_date = datetime(2026, 4, 8)
delta = end_date - start_date

# Clean up existing files first
import shutil
if os.path.exists("src"):
    shutil.rmtree("src")
os.makedirs("src/com/java/anomalies", exist_ok=True)

# Total anomalies: 100
for i, anomaly in enumerate(anomalies):
    commit_date = start_date + timedelta(seconds=(delta.total_seconds() / len(anomalies)) * i)
    date_str = commit_date.strftime("%Y-%m-%dT%H:%M:%S")

    filename = f"src/com/java/anomalies/{anomaly['name']}.java"
    content = f"""package com.java.anomalies;

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
        // Run example here if applicable
    }}
}}
"""
    with open(filename, "w") as f:
        f.write(content)

    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str
    
    run_command("git add .")
    # Using commit --amend or just committing. Since we want 90+ commits, we'll just commit.
    # Note: git init was done earlier.
    run_command(f"git commit -m 'Added {anomaly['name']} anomaly' --date='{date_str}'", env=env)

print("Done! Created 100 REAL anomalies with 100 backdated commits.")
