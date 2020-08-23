import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.BiPredicate;

public class GameOfLife2D implements GameOfLife {

    /**
     * Map for all the possible rulesets to be defined
     */
    private static final Map<RuleSet, BiPredicate<Character, Integer>> RULES;

    static {
        Map<RuleSet, BiPredicate<Character, Integer>> tmp = new HashMap<>();

        // Ruleset 1
        BiPredicate<Character, Integer> liveToLive23 = (s, n) -> s == 1 && (n == 2 || n == 3);
        BiPredicate<Character, Integer> deadToLive33 = (s, n) -> s == 0 && n == 3;
        tmp.put(RuleSet.DEFAULT_RULE, liveToLive23.or(deadToLive33));

        // Ruleset 2
        BiPredicate<Character, Integer> liveToLive45 = (s, n) -> s == 1 && (n == 4 || n == 5);
        BiPredicate<Character, Integer> deadToLive55 = (s, n) -> s == 0 && n == 5;
        tmp.put(RuleSet.RULE_2, liveToLive45.or(deadToLive55));

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

    public GameOfLife2D(List<char[][]> layers, RuleSet ruleId) {
        // Setting the board limits
        this.xLim = layers.get(0).length;
        this.yLim = layers.get(0)[0].length;
        this.rule = ruleId;

        // Setting the board
        this.board = layers.get(0);
    }

    @Override
    public List<int[]> simulateStep() {
        return null;
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
        liveNeighbours += this.board[x][(y - 1) % this.yLim];
        liveNeighbours += this.board[(x + 1) % this.xLim][y];
        liveNeighbours += this.board[(x - 1) % this.xLim][y];
        liveNeighbours += this.board[(x + 1) % this.xLim][(y - 1) % this.yLim];
        liveNeighbours += this.board[(x - 1) % this.xLim][(y - 1) % this.yLim];
        liveNeighbours += this.board[(x + 1) % this.xLim][(y + 1) % this.yLim];
        liveNeighbours += this.board[(x - 1) % this.xLim][(y + 1) % this.yLim];

        return liveNeighbours;
    }

}
