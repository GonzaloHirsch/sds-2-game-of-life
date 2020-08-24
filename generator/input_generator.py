from numpy import random
import math

# Name of the configuration file with the inner configuration
INPUT_CONFIGURATION_FILE = "./generator/input_configuration.txt"

# Generates the static file configuration given:
#   - filename -> Name of the static file to be used
#   - area_length -> Total length of the area of study
#   - layers -> Amount of layers for the inner configuration
def generate_static_file(filename, area_length, layers, fill_percentage):
    f = open(filename, 'w')

    if layers > 1:
        layers = 3
    else:
        layers = 2

    # Adding the amount of dimensions
    f.write('{}\n'.format(layers))

    # Adding the dimensions of the area
    if layers == 3:
        f.write('{} {} {}\n'.format(area_length, area_length, area_length))
    else:
        f.write('{} {}\n'.format(area_length, area_length))

    # Adding the fill fill percentage
    f.write('{}\n'.format(fill_percentage))

    f.close()

# Generates the dynamic file configuration given:
#   - filename -> Name of the dynamic file to be used
#   - area_length -> Total length of the area of study
def generate_dynamic_file(filename, area_length, points):
    f = open(filename, 'w')

    # We provide only the dynamic configuration at time 0
    f.write('0\n')

    # Adding the randomly generated
    for p in points:
        if len(p) == 3:
            f.write('{} {} {}\n'.format(p[0], p[1], p[2]))
        else:
            f.write('{} {}\n'.format(p[0], p[1]))
    f.close()

# Generates both the dynamic and the static file
def generate_files(area_length, layers, points, fill_percentage):
    generate_static_file('./parsable_files/static.txt', area_length, layers, fill_percentage)
    generate_dynamic_file('./parsable_files/dynamic.txt', area_length, points)

# Given the total length of the area and an inner configuration file, generates a list of points offseted to be in the middle of the area of study
def obtain_points_from_matrix(area_length):
    # Reading from the input configuration to determine the amount of dimensions, we only need the first line, so we break after that
    ic = open(INPUT_CONFIGURATION_FILE, "r")

    extracted_points, generated_points = [], []

    # index is the line index
    # dim is the current dimension being processed
    # dim is the total amount of dimensions, 2 or 3
    # l_count is the index of the line for the inner square
    # l_expected is the total number of lines for the inner square
    index, dim, dims, l_count, l_expected, total_points = 0, 0, 2, 0, 0, 0
    for line in ic:
        if index == 0:
            layers = int(line.rstrip("\n"))
            if layers > 1:
                dims = 3
        else:
            # Extract the matrix
            points = [int(x) for x in line.rstrip("\n").split(" ")]
            # Add to the total points
            total_points += len(points)
            # Determine the length of the matrix
            if l_expected == 0:
                l_expected = len(points)
            # Determine change in layer
            if l_count == l_expected:
                l_count = 0
                dim += 1
            # Generate the points
            if dims == 2:
                generated_points = generate_2d_points(points, area_length, l_count)
            else:
                generated_points = generate_3d_points(points, area_length, l_count, dim)
            # Add the points to the list
            for p in generated_points:
                extracted_points.append(p)
            # Increase the processed line count
            l_count += 1
        index += 1

    return extracted_points, total_points

def generate_2d_points(points, area_length, line):
    # Calculating the offsets for each axis
    x_offset = area_length - int((area_length - len(points))/2) - len(points)
    y_offset = x_offset

    generated_points = []

    index = 0
    for p in points:
        if p == 1:
            generated_points.append([x_offset + index, y_offset + line])
        index += 1

    return generated_points

def generate_3d_points(points, area_length, line, dim):
    # Calculating the offsets for each axis
    x_offset = area_length - int((area_length - len(points))/2) - len(points)
    y_offset = x_offset
    z_offset = x_offset

    generated_points = []

    index = 0
    for p in points:
        if p == 1:
            generated_points.append([x_offset + index, y_offset + line, z_offset + dim])
        index += 1

    return generated_points

# Reading from the input configuration to determine the amount of dimensions, we only need the first line, so we break after that
ic = open(INPUT_CONFIGURATION_FILE, "r")
index = 0
for line in ic:
    if index == 0:
        layers = int(line.rstrip("\n"))
        break
    else:
        break
    index += 1

area_length = int(input("Dimensión del area de estudio(Cubo de NxNxN/Cuadrado de NxN, espera un N): "))

# Obtains the usable points placed in the middle of the area of study
points, total_points = obtain_points_from_matrix(area_length)
fill_percentage = (len(points)/total_points) * 100
generate_files(area_length, layers, points, fill_percentage)