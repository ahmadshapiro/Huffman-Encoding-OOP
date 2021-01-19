Huffman Compression/Decompression

![](./READMEimg/20.001.png)

**Ahmad Shapiro**


INTRODUCTION

In 1951, [David A. Huffman ](https://en.wikipedia.org/wiki/David_A._Huffman)and his [MIT](https://en.wikipedia.org/wiki/MIT) [information theory ](https://en.wikipedia.org/wiki/Information_theory)classmates were given the choice of a term paper or a final [exam](https://en.wikipedia.org/wiki/Exam). The professor, [Robert M. Fano](https://en.wikipedia.org/wiki/Robert_M._Fano), assigned a [term paper ](https://en.wikipedia.org/wiki/Term_paper)on the problem of finding the most efficient binary code. Huffman, unable to prove any codes were the most efficient, was about to give up and start studying for the final when he hit upon the idea of using a frequency-sorted [binary tree ](https://en.wikipedia.org/wiki/Binary_tree)and quickly proved this method the most efficient.

In doing so, Huffman outdid Fano, who had worked with [information theory ](https://en.wikipedia.org/wiki/Information_theory)inventor [Claude Shannon ](https://en.wikipedia.org/wiki/Claude_Shannon)to develop a similar code. Building the tree from the bottom up guaranteed optimality, unlike the top-down approach of [Shannon–Fano coding](https://en.wikipedia.org/wiki/Shannon%E2%80%93Fano_coding). 

We will use the mentioned algorithm to compress/decompress files and folders , by the same methods discussed in lecture.

We will make use of the dynamic programming technique to build the tree and make the encodings, to reach an optimal and efficient code at the end.

DATA STRUCTURES USED

1. Minimum Heap  (heapq Library)
1. Tree (Implemented)
1. Dictionary (Built-In Python Hash-Maps)
1. Lists  (Built-In Python Data Structure)

METHOD

Same method as discussed in lecture , building a Huffman Tree using a minimum heap.

IMPLEMENTATION

Object Oriented Programming

![](Huffman%20.002.png)

PROCEDURE

1. Asking the user whether he/she wants to A) Compress or B) Decompress the File/Folder.

![](Huffman%20.003.png)

2. **Compression**

Reading the file/folder name from the user as an input , it must be in the same directory running the script from and including the type (test\_huffman.txt) , or if it's a Folder , it should have the same folder name (Case Sensitive).

1. Reading the name which the user wish to save the compressed file with (without any extension “huffman\_compressed” )

![](Huffman%20.004.png)

2. Huffman\_Encoding object is constructed ,and function “compress” is called with both file name and the compressed file name as parameters , the name of file  to be compressed is passed to the constructor of My\_File object to be operated on , returning it’s content as a string and a dictionary holding the frequency per each character , additional to and “/EOF/” specified delimiter.

![](Huffman%20.005.png)

3. In the construction of My\_File object , the given path is tested to check whether it’s a file or a folder, if it’s a file, the flag “isFIle” is set to 1 , and the “FileNames” attribute is set to hold the name of the file , if it’s a folder, “isFIle” is set to 0 , and the “FileNames” is constructed as a list holding all of the file names in this folder , along with the folder name at index 0 , if file/folder isn’t found it raise an Exception of **“Target Not Found”**.
4. After that , function “operate” is called , to operate on file,calling “read\_file” method that reads it’s content , adding the file name at the start of the content , separated from the message by the early specified delimiter **“/EOF/”** , then frequency of character occurrence is calculated on the whole content , except the delimiter is treated as a single character , and added to the final frequency dictionary.
5. If a folder is passed , “operate” is iterating over all files inside the folder calling “read\_file” at each iteration ,filling the list of contents , and the list of frequencies, after that function “combine” is called , to combine all of those into one content , and one frequency dictionary. The resulting content will have the following form **“FolderName//EOF//File1Name//EOF//File2Name//EOF//File1Message//EOF//File2Mess-ag e//EOF//”**
5. After that ,”makeEncodings” method is called from the compression method , with the frequency dictionary as it’s parameter.
5. “makeEncodings” method , calls “makeMinHeap” method , to build a minimum heap out of the frequency dictionary , using the Node class , as each item in the frequency dict

constructs a single node , and then nodes are pushed into the tree **O(n)** , where n = number of characters.

8. After that , “makeEncodings” , builds the huffman tree, and by the use of the dynamic programming , while building the tree , the encodings (huffman binary codes) are being constructed , by the help of the “isRightNode” boolean that belongs to each Node , while a node is constructed , if its “isRightNode”  equals True(1) , 1 is concatenated in all of it’s children encodings , similarly False (0), Including the

**“/EOF/”** delimiter also encoded. Returning a dictionary with the key as character and the

value as it’s Huffman Binary Representation.  **O(n lo gn)**

9. After that dictionary is reversed and assigned to the Huffman\_Encoding attribute reverseENC, which means that every value is a key  and it’s corresponding key became a value , we are sure that there’s no repetition in either the key or the values, since huffman encoding produce a unique code for each Character.
10. Content are being split by **“/EOF/”** and then decoded to bit streams by the use  along with **“/EOF/” encodings , eg : a:001 , b:011 , /EOF/:111 , “ab/EOF/”** → **001011111![](Huffman%20.006.png)**

![](Huffman%20.007.png)

11. After that , the encoded message is padded with zeros to be modulo 8 = 0 , to be easily converted to bytes without any information loss. .
11. **Header**
13. **Info byte** is made to specify the number of zeroes padded to the end of the bit stream , we know that maximum number of padding would be 7 , so the first 3 bits are specifying the padding number , the 4th bit is telling whether the bit stream of a folder or file (for decompression purposes).
14. A byte code of the reverse dictionary is attained with the help of pickle library , that converts any python object into a byte code to be loaded with the same library again from a binary file, each object has a 4 bytes identifier , those of a dictionary are **b'\x80\x03}q\x00'** those will be used in the decompression to split at them to get our dictionary , and we are sure that byte sequence like this **WOULD NEVER** be repeated.
14. Bit stream message is converted into byte code with the help of “**bitToByte”** function and then concatenated with the byte code of the dictionary , and then written to the .bin file user specified early.
3. **Decompression**
1. Compressed file name is taken as input from the user (without .bin) , also it should be in the same directory.
1. File is read as byte code , and then splitted at **b'\x80\x03}q\x00'**  : reverseEncoding dictionary identifier.
1. The byte code before **b'\x80\x03}q\x00'**  is converted to bit code using to “BytetoBit” Method , the byte code after **b'\x80\x03}q\x00'**  is loaded by **Pickle library**  and returned as a dictionary.
1. First 8 bits are read as info byte , identifying the padding , and whether it’s a file or a folder , the rest are decoded to characters , splitted at **“/EOF/” O(n) ,** and then written to the disk in their original form.

RESULTS

1. **16 MB Uniformly distributed txt file :-**

![](Huffman%20.008.png)

Compression Time : 3.14 Seconds .

Compression Ratio : 1.34 , Compressed file is 74.80% of the original . Decompression Time : 30 Seconds.

2. **Folder ( 16MB Uniform distributed file , 11 MB file , 2 MB file )**

![](Huffman%20.009.png)

Compression Time : 6.01 seconds

Compression Ratio : 1.62 , Compressed file is 61.89% of the original Decompression Time : 40 Seconds.

3. **Given Test File**

![](Huffman%20.010.png)

Compression Time : 0.15 seconds

Compression Ratio : 1.79 , Compressed file is 55.78% of the original Decompression Time : 1.2 Seconds.
PAGE9
