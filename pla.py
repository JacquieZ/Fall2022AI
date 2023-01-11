import pandas as pd
import numpy as np
import sys

def main():

    def f(weights,x):
        sum = 0
        for i in range(0,len(weights)):
            sum += weights[i]*int(x[i])
        return sum

    df = pd.read_csv('data3.csv', header=None)
    # df = pd.read_csv(sys.argv[1], header=None)
    # df1 = df.iloc[:,0:2]
    # df1[len(df1.columns)] = 1
    # df1[len(df1.columns)] = df.iloc[:,2]


    weights = [0]*(df.shape[1]-1)
    print(weights)
    print(df)
    go = True

    while go:
        go = False
        for row in range(0,df.shape[0]):
            if df.iloc[row,4]*f(weights,df.iloc[[row]]) <= 0:
                go = True
                for i in range(0,len(weights)):

                    weights[i] = round(weights[i]+df.iloc[row,4]*df.loc[row,i],1)

                # file = open(sys.argv[2],'a')
                # res = ", ".join([str(i) for i in list(weights)])
                # file.write(res + '\n')
                print(weights)
    # file.close()




if __name__ == "__main__":
    main()
