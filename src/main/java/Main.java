import java.util.List;

public class Main {
    public static void main(String[] args){
        // PARSEO DE INPUT

        // GENERAR BOARD

        GameOfLife gol = new GameOfLife3D();

        int totalSteps = 100;
        List<int[]> pointsToWrite;

        for (int i = 1; i < totalSteps; i++){
            pointsToWrite = gol.simulateStep();

            /*
            * [
            *  [x, y, z],
            *  [z, y, z]
            *
            *
            * ]
            * */

            // WRITE AL ARCHIVO
        }
    }
}
