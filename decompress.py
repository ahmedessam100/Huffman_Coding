import os, pickle, timeit
from .helper import generateMetrics
import re
def revert_text(tree, compressed_text):
    decoded_text = ''
    temp = ''
    for ch in compressed_text:
        temp += str(ch)
        if tree.__contains__(temp):
            decoded_text += tree[temp]
            temp = ''
            
    ## Return the decoded text
    return decoded_text


def decompress(path, folder=0):
    startTime = timeit.timeit()
    
    ## Read compressed file
    dir = os.getcwd()
    if folder == 1:
            filename = os.listdir(path)
            input_file = open(path + '/' + filename[0], "rb")
            while(True):
                tree = {}
                try:
                    tree = pickle.load(input_file)
                except (EOFError):
                    break
                tree = dict(tree)
                file_ext = str(tree['file_ext'])
                file_name = str(tree['file_name'])
                del tree['file_ext']
                del tree['file_name']
                output_path = path + '/' +file_name + file_ext
                
                ## Reversing the tree
                tree = {str(v): str(k).replace('b\'', '', 1).replace('b\"', '', 1).replace('\'', '', 1) for k, v in
                        tree.items()}
                
                ## Load the compressed text
                try:
                    text = pickle.load(input_file)
                except (EOFError):
                    break
                compressed_text = ''
                n = len(text)
                for t in text:
                    if n == 1:
                        compressed_text += '{0:b}'.format(t)
                        break
                    compressed_text += '{0:08b}'.format(t)
                    n -= 1
                # Decoding the text
                decoded_text = revert_text(tree, compressed_text)
                finishTime = timeit.timeit()
                decoded_text = decoded_text.replace('\\r','').split('\\n')
                output_file = open(output_path, 'w+')
                for t in decoded_text:
                    output_file.write(t)
                    output_file.write('\n')
                output_file.close()
                generateMetrics(bytes, tree, finishTime - startTime, path, 1)
            os.remove(path + '/' + filename[0])
            input_file.close()
            return
        
    file_name = os.path.join(dir, path)
    input_file = open(file_name, "rb")
    
    ## Read The Tree
    tree = pickle.load(input_file)
    tree = dict(tree)
    file_ext = str(tree['file_ext'])
    file_name = str(tree['file_name'])
    file_name += '_Decompressed'
    del tree['file_ext']
    del tree['file_name']
    output_path = file_name + file_ext
    
    ## Reversing the tree
    tree = {str(v) : str(k).replace('b\'','',1).replace('b\"','',1).replace('\'', '', 1) for k,v in tree.items()}
    
    ## Load the compressed text
    text = pickle.load(input_file)
    compressed_text = ''
    n = len(text)
    for t in text:
        if n==1:
            compressed_text += '{0:b}'.format(t)
            break
        compressed_text += '{0:08b}'.format(t)
        n-=1
    input_file.close()
    
    # Decoding the text
    decoded_text = revert_text(tree, compressed_text)
    finishTime = timeit.timeit()
    decoded_text = decoded_text.replace('\\r','').split('\\n')
    if file_ext == '.txt':
        output_file = open(output_path, 'w')
        for t in decoded_text:
            output_file.write(t)
            output_file.write('\n')
    output_file.close()
    return generateMetrics(bytes, tree, finishTime - startTime, path, 1)







