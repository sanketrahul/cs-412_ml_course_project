# -*- coding: utf-8 -*-
import csv
import random
import numpy as np
import pickle
import re
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

import time

def get_downsample_list():
    f = file('svm_rbf_allfeatures_results.txt', 'r')
    selected_features_index_list = []
    average = 0.768
    not_special_deviation = 0.0015

    for line in f:
        possible_feature = re.findall(r'Feature *(\d+)', line)
        possible_accuracy = re.findall(r'accuracy = *(\d+.\d+)', line)
        if len(possible_feature) == 1 and len(possible_accuracy) == 1:
            possible_feature = int(possible_feature[0])
	    possible_accuracy = float(possible_accuracy[0])

            if not (possible_accuracy < (average + not_special_deviation)):
                selected_features_index_list.append(possible_feature - 1)
    
    selected_features_index_list = list(set(selected_features_index_list))

    return selected_features_index_list


def downsample_features(features):
    features_to_include = get_downsample_list()
    boolean_mask = []

    for index in xrange(len(features)):
        if index in features_to_include:
            boolean_mask.append(True)
        else:
            boolean_mask.append(False)

    return features[:, np.array(boolean_mask)]
   

    
def main():
    print '[INFO, time: %s] Getting Data....' % (time.strftime('%H:%M:%S'))
    testing_file = file('test.p', 'r')
    training_file = file('train.p', 'r')

    train = pickle.load(training_file)
    test = pickle.load(testing_file)

    testing_file.close()
    training_file.close()
    
    trainX = train[:,:-1]
    trainy = train[:,-1]
    
    testX = test[:,:-1]
    testy = test[:,-1]

    print '[INFO, time: %s] Downsampling ...' % (time.strftime('%H:%M:%S'))
    trainX = downsample_features(trainX)
    testX = downsample_features(testX)

    print '[INFO, time: %s] Fitting %s ...' % (time.strftime('%H:%M:%S'), 'SVM - rbf kernel (i.e. gaussian) with default paramenters')
    clf = SVC()
    clf.fit(trainX, trainy)

    print '[INFO, time: %s] Making Predictions...' % (time.strftime('%H:%M:%S'))
    prediction = clf.predict(testX)
    print '[RESULT, time: %s] accuracy = %f' % (time.strftime('%H:%M:%S'),accuracy_score(testy, prediction))

main()






