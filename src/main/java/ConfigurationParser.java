import com.sun.xml.internal.bind.v2.schemagen.xmlschema.Particle;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.List;
import java.util.Scanner;


public class ConfigurationParser {
    public static boolean is2D;
    public static int xLim;
    public static int yLim;
    public static int zLim = 1;
    public static List<char[][]> board;

    /**
     * Parses the files given with the static and dynamic information in order to configure the initial state of GOL
     *
     * @param staticFileName  File path for the static file
     * @param dynamicFileName File path for the dynamic file
     */
    public static void ParseConfiguration(String staticFileName, String dynamicFileName) throws FileNotFoundException {
        ParseStaticData(staticFileName);
        ParseDynamicData(dynamicFileName);
    }

    private static void ParseStaticData(String staticFileName) throws FileNotFoundException {
        File file = new File(staticFileName);
        Scanner sc = new Scanner(file);

        // Parsing the dimension configuration
        is2D = sc.nextInt() == 2;

        // Parsing the x limit of the area
        xLim = sc.nextInt();

        // Parsing the y limit of the area
        yLim = sc.nextInt();

        // Parsing the limit of the area if it has any
        if (!is2D) {
            zLim = sc.nextInt();
        }
    }

    private static void ParseDynamicData(String dynamicFileName) throws FileNotFoundException {
        File file = new File(dynamicFileName);
        Scanner sc = new Scanner(file);

        for (int z = 0; z < zLim; z++) {
            board.add(new char[xLim][yLim]);
            for (int x = 0; x < xLim; x++) {
                for (int y = 0; y < yLim; y++) {
                    board.get(z)[x][y] = 0;
                }
            }
        }

        // Skipping the time of the file which is 0
        sc.nextInt();

        while (sc.hasNext()){
            // Parsing the x position
            int x = sc.nextInt();

            // Parsing the y position
            int y = sc.nextInt();

            // Setting the z in case it is only 2D
            int z = 0;

            // Parsing the z position if analyzing 3D
            if (!is2D) {
                z = sc.nextInt();
            }
            // Setting the board cell (x, y, z) as alive
            board.get(z)[x][y] = 1;
        }
    }
}
