import numpy as np
import csv
import random
import sys
import matplotlib.pyplot as plt

VARS = 12   # variables

index=0                                     # row index
min = [sys.float_info.max] * (VARS + 2)     # row of maximum values including index and output
max = [0] * (VARS + 2)                      # row of minimum values including index and output



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




def Prepare(filename, header, _normalized_data, num_training_recs_nubes, num_training_recs_despejado, num_training_recs_multinube):
    # make a copy of the normalized data to manipulate it correctly
    dataSet = _normalized_data.copy()

    DatosTrain = []
    training_recs_nubes = 0
    training_recs_despejado = 0
    training_recs_multinube = 0


    for idx, row in enumerate(dataSet):
        if (row[len(row) - 1] == 0):
            if (training_recs_nubes <= num_training_recs_nubes):  # NUBES
                DatosTrain.append(row)
                training_recs_nubes += 1
                continue

        if (row[len(row) - 1] == 0.5):
            if (training_recs_despejado <= num_training_recs_despejado):  # DESPEJADO
                DatosTrain.append(row)
                training_recs_despejado += 1
                continue

        if (row[len(row) - 1] == 1):
            if (training_recs_multinube <= num_training_recs_multinube):  # MULTINUBE
                DatosTrain.append(row)
                training_recs_multinube += 1
                continue

        dataSet = [x for x in dataSet if x not in DatosTrain]


    DatosTrain.insert(0, header)
    with open(filename, 'w') as csvFile:
        writer = csv.writer(csvFile, delimiter=' ')
        for idx, row in enumerate(DatosTrain):
            if (idx == 0):
                writer.writerow(row[0].split(";"))  # writes the header
                continue
            writer.writerow(row)
    csvFile.close()

    # returns the remaining rows
    return dataSet


# Prepare the input dataset: normalize the data and creates the training, validation and test sets
# the input file must contain the header and the index column
def PrepareDataClas(filename):
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


    # items of each class
    NUBES = 513  # type 0 (0 norm)
    CIELO_DESPEJADO = 48  # type 1 (0.5 norm)
    MULTINUBE = 156  # type 2 (1 norm)

    dataSet = Prepare("DatosTrain.csv", header, _normalized_data,
                      int(80 * NUBES / 100), int(80 * CIELO_DESPEJADO / 100), int(80 * MULTINUBE / 100))
    dataSet = Prepare("DatosTest.csv", header, dataSet,
                      int(20 * NUBES / 100), int(20 * CIELO_DESPEJADO / 100), int(20 * MULTINUBE / 100))


    return _normalized_data





data = PrepareDataClas('DatosPracticaNubesJaen.csv')
