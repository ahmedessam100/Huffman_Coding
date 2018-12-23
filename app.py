from Huffman.compress import compress
from Huffman.decompress import decompress
import os

print("\t\t\t\t\t\t#### Huffman Coding App ####")
type = input("1- Compress File\t2- Decompress File\t3- Compress Folder\t4- Decompress Folder\t")
filePath = input("Please enter file name inside the project folder\t")

if(int(type)==1):
    compress(filePath)
elif(int(type)==2):
    decompress(filePath)
elif(int(type)==3):
    compress(filePath, folder=1)
elif(int(type)==4):
    decompress(filePath, folder=1)
else:
    print("Wrong input format")