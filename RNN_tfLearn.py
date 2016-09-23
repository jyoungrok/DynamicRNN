from __future__ import division, print_function, absolute_import

from InputGenerator import *
from DataSet import *
import tflearn
from tflearn.data_utils import to_categorical, pad_sequences
from tflearn.datasets import imdb
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.embedding_ops import embedding
from tflearn.layers.recurrent import bidirectional_rnn, BasicLSTMCell
from tflearn.layers.estimator import regression


class RNN:


    def __init__(self,trainingFilePath,testingFilePath):
        self.trainingData = DataSet(trainingFilePath)
        self.testingData = DataSet(testingFilePath)
        self.numClasses = 2

    def learning(self,numHidden=100):

        # Network building
        net = input_data(shape=[None, MAXIMUM_LENGTH_DATA, NUM_FEATURES])
        # net = embedding(net, input_dim=20000, output_dim=128)
        net = tflearn.lstm(net, numHidden, dropout=0.8)
        net = dropout(net, 0.5)
        net = fully_connected(net, 2, activation='softmax')
        net = regression(net, optimizer='adam', loss='categorical_crossentropy')

        # Training
        model = tflearn.DNN(net, tensorboard_verbose=0)
        model.fit(self.trainingData.data, self.trainingData.label, validation_set=0.1, show_metric=True, batch_size=100)