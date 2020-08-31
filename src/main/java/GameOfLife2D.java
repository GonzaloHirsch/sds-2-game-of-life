import java.util.*;
import java.util.function.BiPredicate;

public class GameOfLife2D implements GameOfLife {

    /**
     * Map for all the possible rulesets to be defined
     */
    private static final Map<RuleSet, BiPredicate<Character, Integer>> RULES;

    static {
        Map<RuleSet, BiPredicate<Character, Integer>> tmp = new HashMap<>();

        // Ruleset 1 -> Conway's Game of Life
        BiPredicate<Character, Integer> liveToLive23 = (s, n) -> s == 1 && (n == 2 || n == 3);
        BiPredicate<Character, Integer> deadToLive33 = (s, n) -> s == 0 && n == 3;
        tmp.put(RuleSet.DEFAULT_RULE, liveToLive23.or(deadToLive33));

        // Ruleset 2 -> Death and stable
        BiPredicate<Character, Integer> liveToLive12 = (s, n) -> s == 1 && (n >= 4 && n <= 6);
        BiPredicate<Character, Integer> deadToLive22 = (s, n) -> s == 0 && (n >= 3 && n <= 5);
        tmp.put(RuleSet.RULE_2, liveToLive12.or(deadToLive22));

        // Ruleset 3 -> Expansion
        BiPredicate<Character, Integer> liveToLive234 = (s, n) -> s == 1 && (n == 2 || n == 3 || n == 4);
        BiPredicate<Character, Integer> deadToLive35 = (s, n) -> s == 0 && (n == 3);
        tmp.put(RuleSet.RULE_3, liveToLive234.or(deadToLive35));

        RULES = Collections.unmodifiableMap(tmp);
    }

    /**
     * Properties for the class
     */
    private final char[][] board;
    private final int xLim;
    private final int yLim;
    private final RuleSet rule;
    private double maxDistance = 0;
    private int livingCellsCount = 0;
    private int totalCells;

    public GameOfLife2D(List<char[][]> layers, RuleSet ruleId) {
        // Setting the board limits
        this.xLim = layers.get(0).length;
        this.yLim = layers.get(0)[0].length;
        this.rule = ruleId;

        // Setting the board
        this.board = layers.get(0);
        this.totalCells = this.xLim * this.yLim;
    }

    @Override
    public List<int[]> simulateStep() {
        // List for active cells
        List<int[]> activeCells = new ArrayList<>();
        List<int[]> deadCells = new ArrayList<>();

        // Resetting the variables
        this.maxDistance = 0;
        this.livingCellsCount = 0;

        // Variable for the live neighbours
        int liveNeighbours, newState;

        // Varaible for the distance
        double distanceToCenter;

        for (int x = 0; x < this.xLim; x++) {
            for (int y = 0; y < this.yLim; y++) {
                // Calculating the amount of live neighbours
                liveNeighbours = this.countLiveNeighbours(x, y);

                // Calculating the new state
                newState = RULES.get(this.rule).test(this.board[x][y], liveNeighbours) ? 1 : 0;

                // If the cell is active, add it to the list and calculate the distance to the center
                if (newState == 1) {
                    // Adding to the list
                    activeCells.add(new int[]{x, y});

                    // Calculating the distance and checking if greater than max
                    distanceToCenter = this.getDistanceToCenter(x, y);
                    this.maxDistance = Math.max(distanceToCenter, this.maxDistance);

                // If the old state was alive and it is now dead
                } else if (this.board[x][y] == 1) {
                    deadCells.add(new int[]{x, y});
                }
            }
        }
        // Updating board
        for (int[] cell : activeCells) {
            this.livingCellsCount++;
            this.board[cell[0]][cell[1]] = 1;
        }
        for (int[] cell : deadCells) {
            this.board[cell[0]][cell[1]] = 0;
        }
        return activeCells;
    }

    @Override
    public double getLivingPercentage() {
        return ((double)this.livingCellsCount / (double)this.totalCells) * 100.0;
    }

    public double getMaxDistance() {
        return maxDistance;
    }

    @Override
    public double calculateMaxDistance() {
        double distanceToCenter;
        maxDistance = 0;

        for (int x = 0; x < this.xLim; x++) {
            for (int y = 0; y < this.yLim; y++) {
                // Calculating the distance and checking if greater than max
                if (this.board[x][y] == 1) {
                    distanceToCenter = this.getDistanceToCenter(x, y);
                    this.maxDistance = Math.max(distanceToCenter, this.maxDistance);
                }
            }
        }
        return maxDistance;
    }

    /**
     * Calculates the distance to the center of the space
     *
     * @param x X position for the cell
     * @param y Y position for the cell
     * @return The distance to the center
     */
    private double getDistanceToCenter(final int x, final int y) {
        return Math.sqrt(Math.pow(y - this.yLim / 2.0, 2) + Math.pow(x - this.xLim / 2.0, 2));
    }

    /**
     * Counts the given live neighbours for a given cell
     *
     * @param x X position for the cell
     * @param y Y position for the cell
     * @return The total number of live neighbours the cell has
     */
    private int countLiveNeighbours(final int x, final int y) {
        int liveNeighbours = 0;

        // Analyze current z plane
        liveNeighbours += this.board[x][(y + 1) % this.yLim];
        liveNeighbours += this.board[x][ModuleUtils.possibleNegative(y - 1, this.yLim)];
        liveNeighbours += this.board[(x + 1) % this.xLim][y];
        liveNeighbours += this.board[ModuleUtils.possibleNegative(x - 1, this.xLim)][y];
        liveNeighbours += this.board[(x + 1) % this.xLim][ModuleUtils.possibleNegative(y - 1, this.yLim)];
        liveNeighbours += this.board[ModuleUtils.possibleNegative(x - 1, this.xLim) % this.xLim][ModuleUtils.possibleNegative(y - 1, this.yLim)];
        liveNeighbours += this.board[(x + 1) % this.xLim][(y + 1) % this.yLim];
        liveNeighbours += this.board[ModuleUtils.possibleNegative(x - 1, this.xLim)][(y + 1) % this.yLim];

        return liveNeighbours;
    }

}
