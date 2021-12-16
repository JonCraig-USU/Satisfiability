import datetime
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np


def timeFunction(function, expr, color='green', time=[], size=[]):
    for n in expr:
        startTime = datetime.datetime.now()
        function(n)
        endTime = datetime.datetime.now()
        time_diff = (endTime - startTime)
        elapsed = time_diff.total_seconds() * 1000
        # print(n)
        # print(time)
        if elapsed > 0: #sometimes the function is too fast and we get 0 time
            time.append(elapsed)
            size.append(n)

    plt.plot(size, time, color)

    slope, intercept, _, _, _ = stats.linregress([np.log(v) for v in size], [np.log(t) for t in time])
    print(str(function) + " = %.6f n ^ %.3f" % (np.exp(intercept), slope))

def buildGraph():
    plt.xlabel("n")
    plt.ylabel("time in milliseconds")
    plt.yscale('log')
    plt.xscale('linear')



    plt.rcParams["figure.figsize"] = [16,9]
    plt.show()
