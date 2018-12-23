import os

def generateMetrics(bytes, compressionKeys, elapsedTime, inputFile, variation):
    print("Elapsed time:", str(abs(round(elapsedTime, 5))) + " seconds")
    if variation == 0:
        calculateCompressionRatio(inputFile)
        generateCodeTable(bytes, compressionKeys)


def calculateCompressionRatio(inputFile):
    inputFileSize = os.path.getsize(inputFile)
    outputFileSize = os.path.getsize("output.bin")
    ratio =  str(round(outputFileSize / inputFileSize * 100, 2)) + "%"
    print("Compression ratio:", ratio)


def generateCodeTable(bytes, compressionKeys):
    print("Byte\t\tCode\t\tNew code")
    for i, byte in enumerate(bytes):
        print(i,"\t\t",bin(ord(byte))[2:].rjust(8, '0'),"\t\t",compressionKeys[byte])
