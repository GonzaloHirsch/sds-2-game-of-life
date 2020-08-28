import org.apache.commons.math3.stat.regression.SimpleRegression;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.util.ArrayList;
import java.util.List;

public class Main {
    private final static String STAT_FILE = "./parsable_files/statistics.txt";
    private final static String OBS_FILE = "./parsable_files/observable_vs_time.txt";
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

        List<int[]> pointsToWrite;
        // Used to calculate the slope (velocity) of the function maxDistance(t)
        SimpleRegression regressionDistance = new SimpleRegression();
        // Getting the initial maximum distance into the regression
        regressionDistance.addData(0, gol.calculateMaxDistance());

        // Used to calculate the rate of change of the living cells
        SimpleRegression regressionLiving = new SimpleRegression();
        regressionDistance.addData(0, ConfigurationParser.livingTotalPercentage);

        // To create the graph observable vs time
        List<Double> observable = new ArrayList<>();
        observable.add(ConfigurationParser.livingTotalPercentage);

        for (int i = 1; i < OptionsParser.timeInterval; i++) {
            // Simulating the step
            pointsToWrite = gol.simulateStep();

            // Adding the points to the regressions
            regressionDistance.addData(i, gol.getMaxDistance());
            regressionLiving.addData(i, gol.getLivingPercentage());

            observable.add(gol.getLivingPercentage());

            // Writing results to file
            GenerateOutputFile(pointsToWrite, i);
        }
        AddToObservableStatisticsFile(OptionsParser.ruleSet, observable);
        AddToVelocityStatisticsFile(ConfigurationParser.is2D, DISPLACEMENT_STATS, ruleSet, ConfigurationParser.livingLimitedPercentage, regressionDistance.getSlope());
        AddToVelocityStatisticsFile(ConfigurationParser.is2D, LIVING_STATS, ruleSet, ConfigurationParser.livingLimitedPercentage, regressionLiving.getSlope());
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
     * Generates the observable vs time statistics file
     *
     * @param observable Data of living cell % or maximum displacement based on time
     */
    private static void AddToObservableStatisticsFile(RuleSet rule, List<Double> observable) {
        StringBuilder sb = new StringBuilder();
        sb.append(rule.toString()).append("\n");
        for (int t = 0; t < observable.size(); t++) {
            sb.append(String.format("%d %.3f\n", t, observable.get(t)));
        }
        try {
            Files.write(Paths.get(OBS_FILE), sb.toString().getBytes(), StandardOpenOption.APPEND);
        } catch (FileNotFoundException e) {
            System.out.println(OBS_FILE + " not found");
        } catch (IOException e) {
            System.out.println("Error writing to the statistics file: " + OBS_FILE);
        }
    }

    /**
     * Generates the velocity vs initial living % statistics file
     *
     * @param livingPercentage Number between 0 and 100 that indicates the percentage of living cells in the initial configuration inside the limited space
     * @param velocity Slope of the regression created by the max distance of a living cell to the origin in function of time intervals
     */
    private static void AddToVelocityStatisticsFile(boolean is2D, String statType, RuleSet rule, double livingPercentage, double velocity) {
        try {
            String sf = String.format("%d %s %s %.3f %.3f\n", is2D ? 2 : 3, statType, rule.toString(), livingPercentage, velocity);
            Files.write(Paths.get(STAT_FILE), sf.getBytes(), StandardOpenOption.APPEND);

        } catch (FileNotFoundException e) {
            System.out.println(STAT_FILE + " not found");
        } catch (IOException e) {
            System.out.println("Error writing to the statistics file: " + STAT_FILE);
        }

    }

}

