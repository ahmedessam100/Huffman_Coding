import heapq, timeit, json
from .helper import generateMetrics
from .node import Node
from bitstring import BitArray
import pickle, os
import deepdish
def compress(path, folder=0):
    if folder == 1:
        first = 0
        for filename in os.listdir(path):
            startTime = timeit.timeit()
            # Read input file
            bytes = readFile(path+'/'+filename)

            # Build dict of frequency
            charFrequency = countChars(bytes)

            # Build Huffman tree
            treeRoot = buildHuffmanTree(charFrequency)

            # Build dict of key codes
            compressionKeys = generateCodes(treeRoot)

            # Replace char with its code
            encodedText = replaceCodes(bytes, compressionKeys)

            # Output binary file
            writeCompressedFile(encodedText, compressionKeys, filename, folder, path, first)
            # Remove file after compressing it
            os.remove(path+'/'+filename)
            finishTime = timeit.timeit()
            first = 1
            # Generate metrics
            generateMetrics(bytes, compressionKeys, finishTime - startTime, path, 0)
    else:
        startTime = timeit.timeit()
        #Read input file
        bytes = readFile(path)

        #Build dict of frequency
        charFrequency = countChars(bytes)

        #Build Huffman tree
        treeRoot = buildHuffmanTree(charFrequency)

        #Build dict of key codes
        compressionKeys = generateCodes(treeRoot)

        #Replace char with its code
        encodedText = replaceCodes(bytes, compressionKeys)

        #Output binary file
        writeCompressedFile(encodedText, compressionKeys, path)
        finishTime = timeit.timeit()

        #Generate metrics
        return generateMetrics(bytes, compressionKeys, finishTime - startTime, path, 0)


def readFile(path):
    inFile = open(path, 'rb')
    bytes = list()
    byte = inFile.read(1)
    while(len(byte) > 0):
        bytes.append(byte)
        byte = inFile.read(1)
    return bytes


def countChars(bytes):
    frequency = dict()
    for byte in bytes:
        if byte not in frequency:
            frequency[byte] = 0
        frequency[byte] += 1
    return frequency


def buildHuffmanTree(charFrequency):
    minHeap = []
    #Make heap
    for key, value in charFrequency.items():
        heapq.heappush(minHeap, Node(key, value))

    while(len(minHeap)>1):
        #Pop smallest two elements
        left = heapq.heappop(minHeap)
        right = heapq.heappop(minHeap)

        #Merge them into one node
        sum = Node(None, left.freq + right.freq)
        sum.left = left
        sum.right = right

        #Push back to heap
        heapq.heappush(minHeap, sum)

    #Return the root of huffman tree
    return heapq.heappop(minHeap)


def generateCodes(treeRoot):
    codeDict = dict()
    initialCode = ""
    #PreorderTraversal
    traverseTree(treeRoot, initialCode, codeDict)
    return codeDict


def traverseTree(treeNode, currentCode, codeDict):
    if(treeNode): #Not leaf child
        if(treeNode.char): #leaf node
            codeDict[treeNode.char] = currentCode
        else: #Non leaf node
            traverseTree(treeNode.left, currentCode + "0", codeDict)
            traverseTree(treeNode.right, currentCode + "1", codeDict)


def replaceCodes(bytes, compressionKeys):
    encodedText = ""
    for char in bytes:
        encodedText += compressionKeys[char]
    return encodedText

def padding(binary):
    to_pad = 8 - len(binary)
    remain = "0" * to_pad
    return (remain + binary)

def writeCompressedFile(encodedText, compressionKeys, path, folder=0, folder_path='', first=0):
    extension = os.path.splitext(path)[1]
    file_name = str(os.path.splitext(path)[0])
    if folder == 1:
        if first == 0:
            output_path = folder_path+'/Compressed.bin'
            output = open(output_path, "wb")
        else:
            output_path = folder_path + '/Compressed.bin'
            output = open(output_path, "ab")
    else:
        output_path = file_name + '_Compressed.bin'
        output = open(output_path, "wb")
    compressionKeys = {k:v for k,v in compressionKeys.items()}
    compressionKeys['file_ext'] = extension
    compressionKeys['file_name'] = file_name

    pickle.dump(compressionKeys, output, protocol=pickle.HIGHEST_PROTOCOL)
    b = bytearray()
    for i in range(0, len(encodedText), 8):
        byte = encodedText[i:i+8]
        b.append(int(byte,2))
    pickle.dump(bytes(b), output, protocol=pickle.HIGHEST_PROTOCOL)
    output.close()
