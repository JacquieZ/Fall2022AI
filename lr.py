import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
from plot_db import visualize_3d,visualize_scatter

def main():
    """
    YOUR CODE GOES HERE
    Implement Linear Regression using Gradient Descent, with varying alpha values and numbers of iterations.
    Write to an output csv file the outcome betas for each (alpha, iteration #) setting.
    Please run the file as follows: python3 lr.py data2.csv, results2.csv
    """
    df = pd.read_csv(sys.argv[1], header=None)

    X = df.iloc[:,0:2]
    Y = df.iloc[:,2]


    X = X.apply(lambda exmaples: (exmaples - exmaples.mean()) / exmaples.std(), axis=0)
    n = len(X)

    df1 = df.iloc[:, 0:2].apply(lambda exmaples: (exmaples - exmaples.mean()) / exmaples.std(), axis=0)
    df1 = df1.join(df.iloc[:, 2])
    df1.columns = ['age', 'weight', 'height']



    alpha = [0.001,0.005,0.01,0.05,0.1,0.5,1,5,10]
    iterations = [100,1000]

    threshold = 0.000000001
    curr_risk = 0


    file = open(sys.argv[2], 'a')
    for rate in alpha:
        bias = 0
        b_age = 0
        b_weight = 0
        for i in range(iterations[0]):
            prediction = bias + b_age*X[0] + b_weight*X[1]
            prev_risk = curr_risk
            curr_risk = (1 / (2 * n)) * sum((prediction - Y) ** 2)

            # if abs(curr_risk - prev_risk) < threshold:
            #     break

            bias = bias - rate * (1/n) * sum(prediction - Y)
            b_age = b_age - rate * (1/n) * sum((prediction - Y) * X[0])
            b_weight = b_weight - rate * (1/n) * sum((prediction - Y) * X[1])

        l1 = [rate,iterations[0],bias,b_age,b_weight]
        # visualize_3d(df1, [bias, b_age, b_weight],
        #              feat1='age', feat2='weight', labels='height',
        #              xlim=(-2, 2), ylim=(-2, 4), zlim=(0, 1.7),
        #              alpha=0.01, xlabel='age', ylabel='weight', zlabel='height',
        #              title='Height Prediction based on Age and Weight')
        #print(str(rate) + ',' + str(curr_risk))
        file.write(", ".join([str(i) for i in l1])+'\n')

    bias = 0
    b_age = 0
    b_weight = 0
    rate = 0.6
    for i in range(iterations[1]):
        prediction = bias + b_age * X[0] + b_weight * X[1]
        prev_risk = curr_risk
        curr_risk = (1 / (2 * n)) * sum((prediction - Y) ** 2)

        # if abs(curr_risk - prev_risk) < threshold:
        #     break

        bias = bias - rate * (1 / n) * sum(prediction - Y)
        b_age = b_age - rate * (1 / n) * sum((prediction - Y) * X[0])
        b_weight = b_weight - rate * (1 / n) * sum((prediction - Y) * X[1])
    l1 = [rate, iterations[1], bias, b_age, b_weight]
    # visualize_3d(df1, [bias, b_age, b_weight],
    #              feat1='age', feat2='weight', labels='height',
    #              xlim=(-2, 2), ylim=(-2, 4), zlim=(0, 1.7),
    #              alpha=0.01, xlabel='age', ylabel='weight', zlabel='height',
    #              title='Height Prediction based on Age and Weight')
    #print(str(rate) + ',' + str(curr_risk))
    file.write(", ".join([str(i) for i in l1]) + '\n')

    file.close()




if __name__ == "__main__":
    main()