from statistics import mean
from statistics import median
from statistics import mode
from statistics import stdev
from statistics import variance

dataset = [1,2,3,4,8,9,4,11,4,12,13,11,9]

mean = mean(dataset)
print("Mean:",mean)

median = median(dataset)
print("Median:",median)

mode = mode(dataset)
print("Mode:",mode)

standard_deviation = stdev(dataset)
print("Standard Deviation:",standard_deviation)

variance = variance(dataset)
print("Varience:",variance)
