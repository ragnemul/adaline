import numpy as np
import csv
import random
import sys
import matplotlib.pyplot as plt

VARS = 200

index=0                                     # row index
min = [sys.float_info.max] * (VARS + 2)     # row of maximum values
max = [0] * (VARS + 2)                      # row of minimum values




# loads the data from csv file and puts the max and min value for each column in the two firsts rows.
# csv structure: index, data...data, output. Total 202 cols per row (200 cols of data)
# the csv file requires only float numbers that uses '.' as decimal separator
def LoadData():
    _data = []
    # puts the min and max values into the first two rows respectively
    _data.insert(0, min)
    _data.insert(1, max)


    # read the csv file
    with open('DatosPracticaSolarOklahoma_v2.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
        for row in readCSV:
            _data.append(row)


            for idx, i in enumerate(row):
                # updates minimum value
                if (_data[0][idx] > row[idx]): _data[0][idx] = row[idx]

                # updates max value
                if (_data[1][idx] < row[idx]): _data[1][idx] = row[idx]


    return _data



# normalize all the variables except the output (last col)
def NormalizeData(data):

    # all the rows except the two first
    for i, row in enumerate(data[2:]):

        # all the items in row except the first (index) and last one (output)
        for j, val in enumerate(row[1:]):
        #for j, val in enumerate(row[1:-1]):
            den = (data[1][j+1] - data[0][j+1])
            num = (val - data[0][j+1])

            if (den == 0):
                VarNorm = 0;
            else:
                VarNorm =  num / den

            # for debug purposes only
            if (VarNorm > 1):
                print("[", i+2, ",", j+1, "]: (", val, "-", data[0][j+1], ") / (", data[1][j+1], "-", data[0][j+1],"): ", VarNorm)

            # updates normalized variable data
            data[i+2][j+1] = VarNorm

        # deleted the first column (record order)
        del data[i+2][0]

    # removes the two first rows (min and max rows)
    data.pop(0)
    data.pop(0)

    # random the array elements
    random.shuffle(data)

    return data



# Prepare the input dataset: normalize the data and creates the training, validation and test sets
# the input file must contain the header
def PrepareData(filename):
    _data = []
    _data.insert(0, min)
    _data.insert(1, max)


    with open(filename) as csvfile:
        txt = csvfile.read()[1:]
        header = txt.splitlines()[:1]
        lines = txt.splitlines()[1:]
        csv_rows = list(csv.reader(lines,delimiter=';'))

        for str_row in csv_rows:
            float_row = [float(w.replace(',','.')) for w in str_row]

            _data.append(float_row)
            for idx, val in enumerate(float_row):
                # updates minimum value
                if (_data[0][idx] > float_row[idx]): _data[0][idx] = float_row[idx]

                # updates max value
                if (_data[1][idx] < float_row[idx]): _data[1][idx] = float_row[idx]

    _normalized_data = NormalizeData(_data)

    records = len(_normalized_data)
    recordsTraining = int(80 * records / 100)
    recordsTest = int(20 * records / 100)

    def localize_floats(row):
        return [
            str(el).replace('.', ',') if isinstance(el, float) else el
            for el in row
        ]

    DatosTrain = _normalized_data[:recordsTraining]
    DatosTrain.insert(0,header)
    with open("DatosTrain.csv",'w') as csvFile:
        writer = csv.writer(csvFile, delimiter=';')
        for idx, row in enumerate(DatosTrain):
            if (idx == 0):
                writer.writerow(row[0].split(";"))    # writes the header
                continue
            writer.writerow(localize_floats(row))
    csvFile.close()

    DatosTest = _normalized_data[recordsTraining+1:]
    DatosTest.insert(0,header)
    with open("DatosTest.csv",'w') as csvFile:
        writer = csv.writer(csvFile, delimiter=';')
        for idx, row in enumerate(DatosTest):
            if (idx == 0):
                writer.writerow(row[0].split(";"))  # writes the header
                continue
            writer.writerow(localize_floats(row))
    csvFile.close()

    return _normalized_data


data = PrepareData('DatosPracticaSolarOklahoma.csv')

