import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.util.Collection;
import java.util.List;

public class Main {
    public static void main(String[] args){
        // Parsing the options
        OptionsParser.ParseOptions(args);

        // GENERAR BOARD

        GameOfLife gol = new GameOfLife3D(null, 1);

        int totalSteps = 100;
        List<int[]> pointsToWrite;

        for (int i = 1; i < totalSteps; i++){
            // Simulating the step
            pointsToWrite = gol.simulateStep();

            // Writing results to file
            GenerateOutputFile(pointsToWrite);
        }
    }

    private static void GenerateOutputFile(List<int[]> cells) {
        try {
            // StringBuilder to minimize file writes
            StringBuilder sb = new StringBuilder();

            // Creating the output for the file
            cells.forEach(cell -> {
                if (cell.length == 3){
                    sb.append(String.format("%d %d %d\n", cell[0], cell[1], cell[2]));
                } else {
                    sb.append(String.format("%d %d\n", cell[0], cell[1]));
                }
            });

            Files.write(Paths.get(OptionsParser.dynamicFile), sb.toString().getBytes(), StandardOpenOption.APPEND);
        } catch (FileNotFoundException e) {
            System.out.println("File not found");
        } catch (IOException e) {
            System.out.println("Error writing to the output file");
        }
    }
}

