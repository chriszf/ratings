#!/usr/bin/env python
from math import sqrt

def pearson(pairs):
    # Takes in a list of pairwise ratings and produces a pearson similarity
    series1 = [float(pair[0]) for pair in pairs]
    series2 = [float(pair[1]) for pair in pairs]

    sum1 = sum(series1)
    sum2 = sum(series2)

    squares1 = sum([ n*n for n in series1 ])
    squares2 = sum([ n*n for n in series2 ])

    product_sum = float(sum([ n * m for n,m in pairs ]))

    size = len(pairs)

    numerator = product_sum - ((sum1 * sum2)/size)
    denominator = sqrt((squares1 - (sum1*sum1) / size) * (squares2 - (sum2*sum2)/size))


    if denominator == 0:
        return 0
    
    return numerator/denominator

if __name__ == "__main__":
    movies = { 
        "Wall-E": { "Ebert": 5.0, "Siskel": 4.0, "LeBron": 5.0, "Moses": 3.7, "Shaq": 4.5, "Bartholomew": 4.8 },
        "The Hangover": { "Ebert": 4.5, "Siskel": 4.2, "LeBron": 4.8, "Moses": 3.5, "Shaq": 4.6, "Bartholomew": 4.7 },
        "The Notebook": { "Ebert": 1.0, "Siskel": 4.5, "LeBron": 3.2, "Moses": 5.7, "Shaq": 0.5, "Bartholomew": 1.2 } }

    print pearson([(5,5), (3,3), (3,3)])
    print pearson([(5,5), (3,3), (3,2)])
    print pearson([(5,1), (3,3), (1,5)])
    print pearson([(1,3), (3,4), (3,2), (4,4)])
    print pearson([(1,3), (3,5)])
