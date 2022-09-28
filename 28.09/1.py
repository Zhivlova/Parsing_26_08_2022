import docx
import pandas as pd
import numpy as np
import pandas as pd

df = pd.read_excel('рейтинг 2021 корр.xlsx',
                   dtype={'сонко на 10000': np.float64, 'соцпредприятия на 10000': np.float64,
                          'налоги сонко': np.float64, 'налоги пожертвования': np.float64, 'мунСОНКО': np.float64,
                          'мунСП': np.float64, 'инфраструк': np.float64, 'работники': np.float64,
                          'соцпредподд': np.float64,'соцзаказ': np.float64, 'персонфин': np.float64,
                          'гчпнегос': np.float64, 'сайт': np.float64, 'клики': np.float64, 'публлицен': np.float64,
                          'открытданн': np.float64, 'дети': np.float64,'мед': np.float64, 'поставщики': np.float64,
                          'культура': np.float64, 'Баллы': np.float64}
                   )

column_names = list(df.columns)[2:]

def initiate_centroids(k, dset):
    '''
    Select k data points as centroids
    k: number of centroids
    dset: pandas dataframe
    '''
    centroids = dset.sample(k)
    return centroids


def rsserr(a, b):
    '''
    Calculate the root of sum of squared errors.
    a and b are numpy arrays
    '''
    return np.square(np.sum((a - b) ** 2))


def centroid_assignation(dset, centroids):
    '''
    Given a dataframe `dset` and a set of `centroids`, we assign each
    data point in `dset` to a centroid.
    - dset - pandas dataframe with observations
    - centroids - pa das dataframe with centroids
    '''
    k = centroids.shape[0]
    n = dset.shape[0]
    assignation = []
    assign_errors = []

    for obs in range(n):
        # Estimate error
        all_errors = np.array([])
        for centroid in range(k):
            err = rsserr(centroids.iloc[centroid, :], dset.iloc[obs, :])
            all_errors = np.append(all_errors, err)

        # Get the nearest centroid and the error
        nearest_centroid = np.where(all_errors == np.amin(all_errors))[0].tolist()[0]
        nearest_centroid_error = np.amin(all_errors)

        # Add values to corresponding lists
        assignation.append(nearest_centroid)
        assign_errors.append(nearest_centroid_error)

    return assignation, assign_errors


def kmeans(dset, column, k=5, tol=1e-4):
    '''
    K-means implementationd for a
    `dset`:  DataFrame with observations
    `k`: number of clusters, default k=2
    `tol`: tolerance=1E-4
    '''
    # Let us work in a copy, so we don't mess the original
    working_dset = dset.copy()

    # We define some variables to hold the error, the
    # stopping signal and a counter for the iterations

    err = []
    goahead = True
    j = 0

    # Step 2: Initiate clusters by defining centroids
    centroids = initiate_centroids(k, pd.DataFrame(dset[column]))

    while (goahead):
        # Step 3 and 4 - Assign centroids and calculate error
        working_dset['centroid'], j_err = centroid_assignation(working_dset, centroids)
        err.append(sum(j_err))

        # Step 5 - Update centroid position
        centroids = working_dset.groupby('centroid').agg('mean').reset_index(drop=True)

        # Step 6 - Restart the iteration
        if j > 0:
            # Is the error less than a tolerance (1E-4)
            if err[j - 1] - err[j] <= tol:
                goahead = False
        j += 1

    working_dset['centroid'], j_err = centroid_assignation(working_dset, centroids)
    centroids = working_dset.groupby('centroid').agg('mean').reset_index(drop=True)
    return working_dset['centroid'], j_err, centroids


def prepare_files(df, column_name):
    df = pd.DataFrame(df[['Субъект РФ', column_name]])
    df[column_name] = df[column_name].apply(float)
    np.random.seed(42)
    df['centroid'], df['error'], centroids = kmeans(df, column_name)
    df = df.sort_values(by=column_name, ascending=False)

    df.to_excel(f'{column_name}.xlsx')

    return df


for column_name in column_names:
    prepare_files(df, column_name)

