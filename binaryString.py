__author__ = 'Finch ThinkPad'

from random import choice, random, seed, Random
from datetime import datetime
from math import e

NUMBER_OF_NEURONS_IN_STRING = 10
NUMBER_OF_INPUTS_IN_STRING = 4
LENGTH_OF_NEURON = 8*NUMBER_OF_NEURONS_IN_STRING + 8*NUMBER_OF_INPUTS_IN_STRING + 8 + 8

NEURON_WEIGHT_BOUNDARY = [-0.25, 0.25]
INPUT_WEIGHT_BOUNDARY = [-0.25, 0.25]
TIME_CONSTANT_BOUNDARY = [0.01, 0.2]
NEURON_BIAS_BOUNDARY = [-0.25, 0.25]


TIME_STEP = 0.1

neuron_init_samples = 20

rnd = Random()
rnd.seed(datetime.microsecond)

class BinaryStringDna():
    def __init__(self, data=None):
        if data == None:
            binaryList = [rnd.choice(['0','1']) for x in range(NUMBER_OF_NEURONS_IN_STRING*LENGTH_OF_NEURON)]
            self.dataString = "".join(binaryList)
        else:
            self.dataString = data

    def getFlipMutant(self, chance):
        dataString = ""
        for i, item in enumerate(self.dataString):
            if(random() < chance):
                entryAsInt = int(item)
                mutatedEntry = (entryAsInt + 1) % 2
                dataString += str(mutatedEntry)
            else:
                dataString += item
        return BinaryStringDna(dataString)

    def getRandomPosition(self):
        position = mapTo(rnd.random(), 0, 1, 0, len(self.dataString))
        return position

    def getCrossBreed(self, otherBinaryStringDNA, position):
        length1 = len(self.dataString)
        length2 = len(otherBinaryStringDNA.dataString)
        if length1 != length2:
            print("Cross breed failed, lengths don't match")
            return None

        dataString = self.dataString[:position]
        dataString += otherBinaryStringDNA.dataString[position:]
        return BinaryStringDna(dataString)


    def getNeurons(self):
        neuronBinStrList = [self.dataString[i:i+LENGTH_OF_NEURON] for i in range(0, len(self.dataString), LENGTH_OF_NEURON)]
        for index, item in enumerate(neuronBinStrList):
            neuronBinStrList[index] = Neuron(item)
        return neuronBinStrList

class Neuron():
    def __init__(self, data=None):
        if data == None:
            self.dataString = [rnd.choice(['0','1']) for x in range(LENGTH_OF_NEURON)]
        else:

            self.dataString = data
        self.neuronWeights = self.getNeuronWeights()
        self.inputWeights = self.getInputWeights()
        self.timeConstant = self.getTimeConstant()
        self.bias = self.getBias()
        self.value = 0
        self.newValue = 0
        self.score = 0

    def getNeuronWeights(self):
        neuronWeights = []
        for i in range(NUMBER_OF_NEURONS_IN_STRING):
            rawNeuronWeight = int(self.dataString[i*8:(i+1)*8], 2)
            mappedNeuronWeight = mapTo(rawNeuronWeight, 0, 255, NEURON_WEIGHT_BOUNDARY[0],NEURON_WEIGHT_BOUNDARY[1])
            neuronWeights.append(mappedNeuronWeight)
        return neuronWeights

    def getInputWeights(self):
        inputWeights = []
        dataString = self.dataString[NUMBER_OF_NEURONS_IN_STRING:]
        for i in range(NUMBER_OF_INPUTS_IN_STRING):
            rawInputWeight = int(dataString[i*8:(i+1)*8],2)
            mappedInputWeight = mapTo(rawInputWeight, 0, 255, INPUT_WEIGHT_BOUNDARY[0], INPUT_WEIGHT_BOUNDARY[1])
            inputWeights.append(mappedInputWeight)
        return inputWeights

    def getBias(self):
        rawBias = int(self.dataString[NUMBER_OF_NEURONS_IN_STRING*8+NUMBER_OF_INPUTS_IN_STRING*8+8:NUMBER_OF_NEURONS_IN_STRING*8+NUMBER_OF_INPUTS_IN_STRING*8+8+8],2)
        mappedBias = mapTo(rawBias, 0, 255, NEURON_BIAS_BOUNDARY[0], NEURON_BIAS_BOUNDARY[1])
        return mappedBias

    def getTimeConstant(self):
        rawTimeConstant = int(self.dataString[NUMBER_OF_NEURONS_IN_STRING*8+NUMBER_OF_INPUTS_IN_STRING*8:NUMBER_OF_NEURONS_IN_STRING*8+NUMBER_OF_INPUTS_IN_STRING*8+8],2)
        mappedTimeConstant = mapTo(rawTimeConstant, 0, 255, TIME_CONSTANT_BOUNDARY[0], TIME_CONSTANT_BOUNDARY[1])
        return mappedTimeConstant

def mapTo(num, minimum, maximum, minimumMap, maximumMap):
    if num < minimum:
        return minimumMap
    elif num > maximum:
        return maximumMap
    else:
        return float(num)*(maximumMap-minimumMap)/(maximum-minimum)+minimumMap

def mapInputsToZeroOneRange(inputs):
    x = []
    x.append(mapTo(inputs[0], -32800, 32800, 0, 1))
    x.append(mapTo(inputs[0], -32800, 32800, 0, 1))
    x.append(mapTo(inputs[0], -32800, 32800, 0, 1))
    x.append(mapTo(inputs[0], -0, 32800, 0, 1))
    return x

def sigma(x):
    return 1/(1+e**(-x))

def step(neurons, inputs, deltaTime):
    for i, neuron in enumerate(neurons):
        neuronWeightSum = 0
        for j, neuron2 in enumerate(neurons):
            A = sigma(neuron2.value - neuron2.bias)
            neuronWeightSum += neuron.neuronWeights[j]*A

        inputWeightSum = 0
        for j, signal in enumerate(inputs):
            inputWeightSum += neuron.inputWeights[j]*signal
        #print("delta time: {}".format(deltaTime))
        #print("Time constant: {}".format(neuron.timeConstant))
        #print("DeltaTime/timeConstant {}".format(deltaTime/neuron.timeConstant))
        neuron.newValue = max(-1, min(1, neuron.value + min((deltaTime/neuron.timeConstant), 1)*(-neuron.value + neuronWeightSum + inputWeightSum)))

        if neuron.newValue > 1:
            print("Neuron has exceeded 1!")
            quit()

    for neuron in neurons:
        neuron.value = neuron.newValue

#Go through each sample time, sum error and divide by sample num
def evaluateDNA(binaryStringDNA, sampleInputs):
    if len(sampleInputs) <= 1:
        print("Not enough sample data points!")
        return None

    #Initialise neuron values through repetition
    neurons = binaryStringDNA.getNeurons()
    for i in xrange(neuron_init_samples):
        step(neurons, sampleInputs[0][1:], sampleInputs[0][0])

    #Run through these
    accumulatedError = 0
    for i in xrange(len(sampleInputs)-1):
        remappedInputs = mapInputsToZeroOneRange(sampleInputs[i][1:])
        remappedInputsFuture = mapInputsToZeroOneRange(sampleInputs[i+1][1:])
        deltaTime = sampleInputs[i][0]
        step(neurons, remappedInputs, deltaTime)
        predicted = currentPrediction(neurons)
        accumulatedError += evaluateError(remappedInputsFuture, predicted)
    avgError = accumulatedError/(len(sampleInputs)-1)
    return avgError

#Takes the first four neurons as predictors
def currentPrediction(neurons):
    list = [neurons[i].value for i in xrange(NUMBER_OF_INPUTS_IN_STRING)]
    return list


def evaluateError(inputs, predicted):
    if len(inputs) != len(predicted):
        print("Error in evaluating error, inputs are different lengths")
        return None
    errorInPrediction = 0
    for i in range(len(inputs)):
        errorInPrediction += abs(predicted[i] - inputs[i])/len(inputs)
    #print("error in final input {}".format(abs(predicted[-1] - inputs[-1])/len(inputs)))

    return errorInPrediction
# DNA = BinaryStringDna()
# evaluateDNA(DNA, )

