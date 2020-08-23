import com.sun.xml.internal.bind.v2.schemagen.xmlschema.Particle;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.List;
import java.util.Scanner;


public class ConfigurationParser {
    public static boolean is2D;
    public static int xLim;
    public static int yLim;
    public static int zLim;
    public static List<int[]> livingCells;

    /**
     * Parses the files given with the static and dynamic information in order to configure the initial state of GOL
     *
     * @param staticFileName  File path for the static file
     * @param dynamicFileName File path for the dynamic file
     */
    public static void ParseParticles(String staticFileName, String dynamicFileName) throws FileNotFoundException {
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

        // Skipping the time of the file which is 0
        sc.nextInt();

        while (sc.hasNext()){
            // Parsing the x position
            int x = sc.nextInt();

            // Parsing the y position
            int y = sc.nextInt();

            // Parsing the x velocity
            if (is2D) {
                livingCells.add(new int[]{x, y});
            } else {
                int z = sc.nextInt();
                livingCells.add(new int[]{x, y, z});
            }
        }
    }
}
