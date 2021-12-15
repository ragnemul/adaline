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
    recordsTraining = int(60 * records / 100)
    recordsValidation = int(20 * records / 100)
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

    DatosValid = _normalized_data[recordsTraining+1:recordsTraining+recordsValidation]
    DatosValid.insert(0,header)
    with open("DatosValid.csv",'w') as csvFile:
        writer = csv.writer(csvFile, delimiter=';')
        for idx, row in enumerate(DatosValid):
            if (idx == 0):
                writer.writerow(row[0].split(";"))  # writes the header
                continue
            writer.writerow(localize_floats(row))
    csvFile.close()

    DatosTest = _normalized_data[recordsTraining+recordsValidation+1:]
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



# weights initialization
w = [random.random() for k in range(VARS)]
w = [0.47,0.98,0.90,0.47,0.89,0.02,0.27,0.38,0.31,0.69,0.32,0.56,0.43,0.23,0.40,0.98,0.04,0.42,0.01,0.61,0.67,0.47,0.49,0.11,0.62,0.41,0.34,0.16,0.39,0.44,0.03,0.44,0.14,0.33,0.40,0.41,0.51,0.58,0.56,0.45,0.76,0.90,0.22,0.11,0.20,0.81,0.62,0.05,0.20,0.24,0.47,0.37,0.35,0.49,0.84,0.37,0.77,0.52,0.98,0.98,0.29,0.58,0.05,0.33,0.56,0.53,0.79,0.92,0.14,0.09,0.26,0.07,0.39,0.45,0.63,0.33,0.60,0.68,0.52,0.19,0.68,0.60,0.85,0.92,0.56,0.29,0.27,0.98,0.90,0.51,0.68,0.52,0.36,0.29,0.27,0.08,0.25,0.59,0.94,0.74,0.41,0.08,0.04,0.16,0.87,0.73,0.87,0.95,0.68,0.80,0.19,0.80,0.96,0.78,0.68,0.99,0.66,0.39,0.33,0.34,0.19,0.27,0.66,0.11,0.18,0.28,0.07,0.38,0.85,0.06,0.77,0.66,0.07,0.99,0.23,0.93,0.82,0.80,0.62,0.91,0.34,0.42,0.52,0.58,0.77,0.10,0.05,0.79,0.44,0.58,0.93,0.64,0.29,0.59,0.92,0.31,0.33,0.58,0.97,0.57,0.11,0.76,0.09,0.80,0.20,0.56,0.68,0.35,0.28,0.03,0.25,0.73,0.98,0.69,0.39,0.22,0.31,0.59,0.79,0.18,0.45,0.07,0.72,0.72,0.55,0.86,0.57,0.09,0.46,0.06,0.54,0.50,0.33,0.58,0.01,0.46,0.01,0.72,0.22,0.48]


# vars list contains 200 values plus the real output
# returns the ADALINE output for each groups of variables
def Y(vars):
    last_element = len(vars)-1

    list = w, vars[:-1]
    output = sum([x * y for x, y in zip(*list)]) + theta

    return output


def show_matrix_list(l):
    for row in l:
        print (*row)


data = PrepareData('DatosPracticaSolarOklahoma.csv')


data_row = LoadData()
x = NormalizeData(data_row)

TRAINING_PERCENTAJE = 60
VALIDATION_PERCENTAJE = 20
TEST_PERCENTAJE = 20
GAMA=0.005
data_records = len(x)
data_variables = len(x[0])

# the real result for the system was recorded in the last column of each record
real_output_idx = data_variables -1

theta=0.940173529

# output of the ADALINE
Yp = 0
# patron error list
Ep=[]
# cuadratic error
RMSE=[]

# for plotting the error evolution over the cycles
plots = []

# training for TRAINING_PERCENTAJE subset
total_minus_training_records = data_records - int(TRAINING_PERCENTAJE * len(x) / 100)
for n in range(200):

    # for each entry
    #for i, vars in enumerate(x[:-total_minus_training_records]):
    for i, vars in enumerate(x):
        # output of the networn
        Yp = Y(vars)
        # output of the real system
        Dp = x[i][real_output_idx]
        # comparison with the desired output
        output_delta = Dp - Yp


        # for each value in an entry (row)
        for j, val in enumerate(vars[:-1]):
            w_delta = GAMA * output_delta * x[i][j]
            w[j] = w[j] + w_delta
        theta = theta + GAMA * output_delta

        Ep.append(np.power(Dp-Yp,2))
        #print (Yp)

    # at the end of each loop calculate the error
    error = sum(Ep) / len(Ep)
    RMSE.append(error)
    #print("Error: ", error, "(",len(str(int(error))),")")



x_coordinates = list(range(1,n+2))
plt.plot(x_coordinates,RMSE)
plt.show()

print ("RMSE last 5: ", RMSE[:10])

#print(w)
#show_matrix_list(  x)
#print (Yp)


