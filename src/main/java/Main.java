import org.apache.commons.math3.stat.regression.SimpleRegression;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.util.ArrayList;
import java.util.List;

public class Main {
    private final static String STAT_FILE = "./parsable_files/statistics.txt";
    private final static String RADIUS_FILE = "./parsable_files/radius_vs_time.txt";
    private final static String LIVING_PERCENT_FILE = "./parsable_files/living_percent_vs_time.txt";
    private final static String LIVING_STATS = "Living";
    private final static String DISPLACEMENT_STATS = "Displacement";

    public static void main(String[] args) {
        // Parsing the options
        OptionsParser.ParseOptions(args);

        try {
            // Parsing the initial configuration
            ConfigurationParser.ParseConfiguration(OptionsParser.staticFile, OptionsParser.dynamicFile);
        } catch (FileNotFoundException e) {
            System.out.println("File not found");
            System.exit(1);
        }

        // Generate GameOfLife board and rule sets to follow
        List<char[][]> board = ConfigurationParser.board;
        RuleSet ruleSet = OptionsParser.ruleSet;
        GameOfLife gol = ConfigurationParser.is2D ? new GameOfLife2D(board, ruleSet) : new GameOfLife3D(board, ruleSet);
        double initialMaxDistance = gol.calculateMaxDistance();

        List<int[]> pointsToWrite;

        // To create the graph evolution vs time
        List<Double> livingVsTime = new ArrayList<>();
        List<Double> radiusVsTime = new ArrayList<>();
        livingVsTime.add(ConfigurationParser.livingTotalPercentage);
        radiusVsTime.add(initialMaxDistance);

        for (int i = 1; i < OptionsParser.timeInterval; i++) {
            // Simulating the step
            pointsToWrite = gol.simulateStep();

            livingVsTime.add(gol.getLivingPercentage());
            radiusVsTime.add(gol.getMaxDistance());

            // Writing results to file
            GenerateOutputFile(pointsToWrite, i);
        }
        AddToEvolutionStatisticsFile(ConfigurationParser.is2D, ConfigurationParser.livingLimitedPercentage, OptionsParser.ruleSet, livingVsTime, LIVING_PERCENT_FILE);
        AddToEvolutionStatisticsFile(ConfigurationParser.is2D, ConfigurationParser.livingLimitedPercentage, OptionsParser.ruleSet, radiusVsTime, RADIUS_FILE);
    }

    private static void GenerateOutputFile(List<int[]> cells, int iteration) {
        try {
            BufferedWriter bf = new BufferedWriter(new FileWriter(OptionsParser.dynamicFile, true));
            bf.append(String.format("%d\n", iteration));

            // Creating the output for the file
            cells.forEach(cell -> {
                try {
                    if (cell.length == 3) {
                        bf.append(String.format("%d %d %d\n", cell[0], cell[1], cell[2]));
                    } else {
                        bf.append(String.format("%d %d\n", cell[0], cell[1]));
                    }
                } catch (IOException e) {
                    System.out.println("Error writing to the output file");
                }
            });

            bf.close();
        } catch (FileNotFoundException e) {
            System.out.println("File not found");
        } catch (IOException e) {
            System.out.println("Error writing to the output file");
        }
    }

    /**
     * Generates the evolution vs time statistics file
     *
     * @param evolution Data of living cell % or maximum displacement based on time
     */
    private static void AddToEvolutionStatisticsFile(boolean is2D, double initialPercentage, RuleSet rule, List<Double> evolution, String file) {
        StringBuilder sb = new StringBuilder();
        sb.append(String.format("%d %.3f %d", is2D ? 2 : 3, initialPercentage, rule.getRuleId()));
        for (Double aDouble : evolution) {
            sb.append(String.format(" %.3f", aDouble));
        }
        sb.append("\n");
        try {
            Files.write(Paths.get(file), sb.toString().getBytes(), StandardOpenOption.APPEND);
        } catch (FileNotFoundException e) {
            System.out.println(file + " not found");
        } catch (IOException e) {
            System.out.println("Error writing to the statistics file: " + file);
        }
    }
}

