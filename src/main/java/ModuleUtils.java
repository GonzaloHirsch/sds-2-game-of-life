public final class ModuleUtils {
    private ModuleUtils() {
        throw new AssertionError();
    }

    public static int possibleNegative(int a, int b) {
        int module = a % b;
        return module >= 0 ? module : module + b;
    }
}
