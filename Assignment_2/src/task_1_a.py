from csv import DictReader, DictWriter
from os import path
from collections import defaultdict

# set directory for data
src_dir = path.join(path.dirname(path.realpath(__file__)), '..', 'data')

# dictionary to load data into
dictionary_red_wine = []

with open(path.join(src_dir, 'winequality-red.csv'), 'r') as f_in:
    # the delimiter for the data is semi-colon in the CSV
    data_red_wine = DictReader(f_in, delimiter=';')

    # default dict yields a default value if the key is not present
    min_dict = defaultdict(lambda: +1e10)
    max_dict = defaultdict(lambda: -1e10)

    # iterating every entry in the data
    for index, vals in enumerate(data_red_wine):
        dictionary_red_wine.append(vals)
        for key in vals.keys():
            # handle quality as per the given conditions
            if key == 'quality':
                if int(vals['quality'])<=6:
                    dictionary_red_wine[index]['quality'] = 0
                else:
                    dictionary_red_wine[index]['quality'] =  1
            # find min and max of other columns for scaling
            else:
                min_dict[key] = min(min_dict[key], float(vals[key]))
                max_dict[key] = max(max_dict[key], float(vals[key]))

# apply scaling
for index, vals in enumerate(dictionary_red_wine):
    for key in vals.keys():
        # exclude quality attribute
        if key != 'quality':
            # apply min-max scaling
            dictionary_red_wine[index][key] = (float(dictionary_red_wine[index][key]) - min_dict[key])/(max_dict[key]-min_dict[key])

with open(path.join(src_dir, 'dataset_A.csv'), 'w') as f_out:
    writer = DictWriter(f_out, fieldnames=dictionary_red_wine[0].keys(), delimiter=';')
    writer.writeheader()
    writer.writerows(dictionary_red_wine)