import pandas as pd
import numpy as np
#code is best run on terminal with 'python3'
#make sure pandas and numpy are installed on computer

## To Do: Write the entropy(label) function
## Should find the information entropy of dataset (T) with class "label" i.e. Info(T)
def entropy(label):
    values = []
    for l in label:
        if l not in values:
            values.append(l)
    entropy_calc = 0
    for v in values:
        count = 0
        for l in label:
            if l == v:
                count += 1
        entropy_calc += -(count / len(label)) * np.log2(count / len(label))
    return entropy_calc
## To Do: Write the information_gain(feature, label) function
## Should find the information gain of "feature"(X) on dataset (T) with class "label" i.e. Gain(X,T)
def information_gain(label, dataset, feature):
    entropy_inflated = entropy(dataset[label])
    entropy2 = 0
    split_by_value = split(dataset, feature)  
    for i in range(len(split_by_value)):
        entropy2 += (len(split_by_value[i]) / len(dataset)) * entropy(split_by_value[i][label])
    information_gained = entropy_inflated - entropy2
    return information_gained
## To Do: Fill split(dataset, feature) function
## Should split the dataset on a feature
def split(dataset, feature):
    values = []
    for df in dataset[feature]:
        if df not in values:
            values.append(df)
    list = []
    for value in values:
        potential = dataset[feature]
        splitted_dataframe = dataset[potential == value]
        list.append(pd.DataFrame(splitted_dataframe))
    return list
## To Do: Fill find_best_split(dataset, label) function
## Should find the best feature to split the dataset on
## Should return best_feature, best_gain
def find_best_split(dataset, label):
    best_gain = 0
    best_feature = 0
    temp_features = list(dataset)
    temp_features.remove('INFLATED')
    for c in temp_features:
        info_gain = information_gain(label, dataset, c)
        if best_gain < info_gain:
            best_feature = c
            best_gain = info_gain
    return best_feature, best_gain


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    data = pd.read_csv('balloons.csv')
    best_feature, best_gain = find_best_split(data, "INFLATED")
    f = open("output_balloons.txt", "w")
    f.write("The Best Feature is {} with a Gain of : {}".format(best_feature, best_gain))
    f.close()
