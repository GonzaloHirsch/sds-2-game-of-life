# Simulación de Sistemas - TP2

## File Generation
There are 2 possibilities when generating input files, random input files and not random files can be generated.

The generated files are **static.txt** and **dynamic.txt**

The contents for the **static.txt** are:
```
number_of_dimensions(2/3)
x_size y_size z_size
fill_percentage
```

The contents for the **dynamic.txt** are:
```
iteration
x_1_pos y_1_pos z_1_pos
...
x_n_pos y_n_pos z_n_pos
```

**NOTE**: The contents shown here are generalized for 3 dimensions, if the simulation is 2D, the Z dimension not included

### Random Generation
Being in the root of the project, the file generator can be run in python.
```
python generator/random_input_generator.py -L 30 -l 5 -d 3 -p 50
```

The usage is:
 - **-L** -> For the size of the total area of study
 - **-l** -> For the size of the input area of study
 - **-d** -> Dimensions to be used 2 or 3 dimensions
 - **-p** -> Percentage of cell filling (0<=p<=100)

This will generate a *static.txt* and *dynamic.txt* files in the root of the project.

### Non-Random Generation
The non-random input generation is performed using a *input_configuration.txt* file in order to describe the configuration.

The script is run like this:
```
python3 generator/input_generator.py
```

It will prompt the user a number representing the total area of study

#### input_configuration.txt
Contains the initial configuration for the cells, the format to be used is:
```
NUM_OF_DIMENSIONS

MATRIX_OF_1_AND_0
```
For example a 2-dimensional arange of a 3x3 inner matrix would be:
```
1
1 0 1
0 1 0
1 0 1
```
For example a 3-dimensional arange of a 3x3x3 inner matrix would be:
```
3
1 0 1
0 1 0
1 0 1
1 0 1
0 1 0
1 0 1
1 0 1
0 1 0
1 0 1
```
**NOTE:** We assume that the inner configuration will always be a cube/square

## Simulation
Run the command to package the project:
```
mvn clean package
```
Run the command to execute the algorithm(optional flags for _Iterations_ (-t, with its corresponding iteration count) and _Ruleset_ (-r, , with its corresponding rule id) can be used):
```
java -jar ./target/sds-tp2-1.0-SNAPSHOT-jar-with-dependencies.jar -sf ./static.txt -df ./dynamic.txt -t 100 -r 2
```
This will generate a file **output.txt** in the root directory of the project with all the neighbours

## Visualization
The visualization can be done in python

For the generation fo random input **matplotlib** needs to be installed by using:
```
pip install matplotlib
```
or **matplotlib** if using OSx
```
pip3 install matplotlib
```

## Graph Visualization
After generating the initial file as specified in previous sections:

####evolution vs. time
To create this graph, the file evolution_vs_time.txt is used. The first line of the file should be manually written depending on the data you want to analyze. The format of this line must be:
```
Dimension evolutionType IntialLivingPercentage
``` 
Where evolutionType is either "Living" or "Displacent".

When you run the algorithm, the data of the run will be appended to the file. This should be the same type of data you described in the first line, it is your responsibility to ensure this.

To change the data you are collecting, head on over to Main.java and make sure the evolution lists is using the wanted data. This can be either percentage of living cells or maximum distance to center:
```
List<Double> evolution = new ArrayList<>();
evolution.add(ConfigurationParser.livingTotalPercentage);
...
evolution.add(gol.getLivingPercentage());

OR

List<Double> evolution = new ArrayList<>();
evolution.add(gol.calculateMaxDistance());
...
evolution.add(gol.getMaxDistance());
```
You can also specify whether you want the regression lines in the created graph for the plotted lines and what interval to consider for these. You can specify this in the evolution_graph_visualize.py file with the variables:
```$xslt
show_regression = False
reg_time_limit = 50     #time to consider in the regression
```
To graph, run the command:
```$xslt
python visualization/evolution_graph_visualize.py 
```

####Velocity vs. Initial Percentage
To view the graphs created with the data appended in the file stats_visualize.py, run:
```$xslt
python visualization/stats_visualize.py 
```

## Visualization
The visualization can be done in python

For the generation fo random input **matplotlib** needs to be installed by using:
```
pip install matplotlib
```
or **matplotlib** if using OSx
```
pip3 install matplotlib
```

Being inside the _visualization_ folder, run the following command to create the random input files:
```
python visualize.py
```



## Authors

Florencia Petrikovich - fpetrikovich@itba.edu.ar
Gonzalo Hirsch - ghirsch@itba.edu.ar

## Sources

[3D Rules](https://wpmedia.wolfram.com/uploads/sites/13/2018/02/01-3-1.pdf)