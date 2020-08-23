import org.apache.commons.cli.*;

public class OptionsParser {
    protected static RuleSet ruleSet = RuleSet.DEFAULT_RULE;
    protected static Integer timeInterval = 100;

    private static final String PARAM_T = "t";
    private static final String PARAM_R = "r";
    private static final String PARAM_H = "h";

    /**
     * Generates the options for the help.
     *
     * @return Options object with the options
     */
    private static Options GenerateOptions() {
        Options options = new Options();
        options.addOption(PARAM_H, "help", false, "Shows the system help.");
        options.addOption(PARAM_T, "time_iteration", true, "Amount of iterations (or time) to run the Game Of Life for.");
        options.addOption(PARAM_R, "rule_set", true, "Id of the rule set to apply to the Game Of Life");
        return options;
    }

    /**
     * Public
     *
     * @param args
     */
    public static void ParseOptions(String[] args) {
        // Generating the options
        Options options = GenerateOptions();

        // Creating the parser
        CommandLineParser parser = new DefaultParser();

        try {
            // Parsing the options
            CommandLine cmd = parser.parse(options, args);

            // Parsing the help
            if (cmd.hasOption(PARAM_H)){
                help(options);
            }

            // Parsing the rule set id
            if (cmd.hasOption(PARAM_R)){
                ruleSet = RuleSet.fromId(Integer.parseInt(cmd.getOptionValue(PARAM_R)));
                if (ruleSet == null) {
                    System.out.format("Non existing rule set. Choose a number between %d and %d\n", RuleSet.minRule(), RuleSet.maxRule());
                    System.exit(1);
                }
            }

            // Checking if the time amount is present
            if (!cmd.hasOption(PARAM_T)){
                System.out.println("A time frame amount must be specified");
                System.exit(1);
            }
            // Retrieving the amount of "time" to iterate with
            timeInterval = Integer.parseInt(cmd.getOptionValue(PARAM_T));

        } catch (ParseException e) {
            System.out.println("Unknown command used");

            // Display the help again
            help(options);
        }
    }

    /**
     * Prints the help for the system to the standard output, given the options
     *
     * @param options Options to be printed as help
     */
    private static void help(Options options) {
        HelpFormatter formatter = new HelpFormatter();
        formatter.printHelp("Main", options);
        System.exit(0);
    }
}
