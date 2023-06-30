import sys
import pyRserve
import pandas as pd

port = 6311

# Connect to R server on default port 6311
conn = pyRserve.connect(host='localhost', port=port)


# col_names        : List to of pandas data frame columns
# columns          : Values of each columns of pandas data frame
# r_data_frame_args: Forms string containing arguments of R's data.frame()
def convert_to_r_dataframe(pandas_df):
    col_names = pandas_df.columns.tolist()
    columns = []
    r_data_frame_args = ""

    for i in range(0, len(col_names)):
        columns.append(pandas_df[col_names[i]].values.tolist())

        # Forms argument for R's data.frame() function
        # Adds name of columns with comma
        if i != len(col_names) - 1:
            r_data_frame_args += (col_names[i] + ",")
        else:
            r_data_frame_args += col_names[i]

        # Creates variable with column name on R's environment
        # with it's column values as a vector
        conn.r.assign(f'{col_names[i]}', columns[i])

    # Creates a data frame with the column vector with created on R environment
    conn.r(f'r_df <- data.frame({r_data_frame_args})')
    return


def dsldPyTakeALookAround(data, yName, sName, maxFeatureSize=None):
    conn.r('library(dsld)')

    convert_to_r_dataframe(data)

    # Used iris data for testing and it worked
    # When testing with iris data replace data argument inside dsldTakeALookAround to iris
    # ex: dsldTakeALookAround(iris, yName, sName)
    # Can test it with the follwoing shell command:
    # python dsldTakeLookAround_PyRServe.py iris Sepal.Length Petal.Length
    # uncomment code below before running it
    #conn.r('data(iris)')

    conn.r.assign("yName", yName)
    conn.r.assign("sName", sName)

    if maxFeatureSize is None:
        conn.r('dsld_result <- dsldTakeALookAround(data, yName, sName)')
        df_r = conn.r('dsld_result')
    else:
        conn.r.assign("maxFeatureSize", maxFeatureSize)
        conn.r('dsld_result <- dsldTakeALookAround(data, yName, sName, maxFeatureSize)')
        df_r = conn.r('dsld_result')


    df_py = pd.DataFrame(df_r)

    conn.close()

    return df_py

if __name__ == "__main__":
    args = sys.argv

    file_path = args[1]

    data = pd.read_csv(file_path)

    if len(args) != 5:
        dsldPyTakeALookAround(data, args[2], args[3])
    else:
        dsldPyTakeALookAround(data, args[2], args[3], int(args[4]))
