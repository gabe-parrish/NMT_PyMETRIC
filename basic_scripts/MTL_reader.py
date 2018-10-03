# ===============================================================================
# Copyright 2018 gabe-parrish
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================

# ============= standard library imports ========================
import os

# ============= local library imports ===========================

def read_mtl(path):
    """
    This function reads in all the text file for the mtl, and based on the subheadings constructs a nested dictionary.
    :param path: A path to an mtl file for LANDSAT
    :return: A nested dictionary of mtl subheadings and variables + values
    """

    # initialize a blank list to store the keys and values
    mtl_list = []

    # Read the file, give exception if file cannot be found.
    try:
        with open(path, 'r') as mtl:
            for line in mtl:
                if "=" in line:
                    key_val = line.split(" = ")

                    key = key_val[0]
                    val = key_val[1]

                    key_val_tuple = (key, val)

                    print(key, val)
                    mtl_list.append(key_val_tuple)

                else:
                    print('end of the file {}'.format(line))

    except FileNotFoundError:
        print("file {} not found".format(path))

    # Determine the names and index positions of sub-headers.
    mtl_subheaders = []
    subheader_indices = []
    subheader_ends = []
    subheader_ends_indices = []
    for index, item in enumerate(mtl_list):
        key = item[0]
        value = item[1][0:-1]

        if key.startswith("GROUP"):
            principal_header = value

        elif key.startswith("  GROUP"):
            sub_header = value
            mtl_subheaders.append(sub_header)
            subheader_indices.append(index)

        elif key.startswith("  END_GROUP"):
            subheader_ends.append(value)
            subheader_ends_indices.append(index)

    # Store the keys and values from the mtl_list of tuples in a nested dict within the subheaders.
    mtl_dict = {}
    for index, item in enumerate(mtl_list):

        key = item[0]
        value = item[1][0:-1]

        if index in subheader_indices:
            if index not in subheader_ends_indices:
                mtl_dict[mtl_list[index][1].strip()] = {}
        if index not in subheader_ends_indices:
            for shi, ehi in zip(subheader_indices, subheader_ends_indices):
                if index > shi and index < ehi:
                    mtl_dict[mtl_list[shi][1].strip()][key.strip()] = value.strip()

    return mtl_dict, principal_header


def main():

    # TODO - Jan, enter the location of the mtl file here
    mtl_directory = "/Users/Gabe/Desktop/PyMETRIC/LC08_L1TP_033037_20180908_20180912_01_T1_MTL_highlighted_variables_for_METRIC_input.txt"

    # read the directory and output a nested dictionary
    mtl_dict, principal_header = read_mtl(mtl_directory)

    # here we print out the dictionary with all the values in the mtl and we also print the header of the mtl file
    print(' ##### mtl dict ###### \n', mtl_dict, "\n header -> {}".format(principal_header))

    # TODO - Jan, you can now get all the data in the mtl based on the GROUP subheadings and the variable you want from mtl_dict

    # ex) I want the QUANTIZE_CAL_MAX_BAND_7. It is within the GROUP subheading MIN_MAX_PIXEL_VALUE ...
    jans_value_of_interest = mtl_dict["MIN_MAX_PIXEL_VALUE"]["QUANTIZE_CAL_MAX_BAND_7"]
    print('This is what Jan was interested in \n', jans_value_of_interest)


if __name__ == "__main__":

    main()