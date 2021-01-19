class Huffman_Encoding():

    def __init__(self):
        self.freq=None
        self.content=None
        self.encodings={}
        self.reverseENC=None
        self.file=None
        self.root=None
        self.pad_num=None
        self.desired_name=None
        self.compressed_name=None

    def compress(self,file_path,compression_name):
        import pickle
        self.desired_name=compression_name
        self.file = My_File(file_path)
        self.content,self.freq=self.file.operate()
        self.makeEncodings(self.freq)
        self.reverseENC=dict(((x[1],x[0]) for x in self.encodings.items()))
        encoded_message=""
        for chunck in self.content.split("/EOF/"):
            if len(chunck) > 1:
                for char in chunck :
                    encoded_message = encoded_message + self.encodings[char]
                encoded_message=encoded_message+self.encodings["/EOF/"]

        self.pad_num,encoded_message=self.zero_pad(encoded_message)

        fix_pad=lambda x :"0"*(3-len(x.replace("0b","")))+x.replace("0b","") if len(x.replace("0b","")) < 3 else x.replace("0b","")
        info_byte=fix_pad(bin(self.pad_num))+str(int(self.file.isFile))
        _,info_byte=self.zero_pad(info_byte)

        if self.desired_name == None :
            raise Exception("Empty Destination")

        else:

            with open(self.desired_name+".bin","wb") as file:
                file.write(self.bitToByte(info_byte+encoded_message))
                file.write(pickle.dumps(self.reverseENC))


    def zero_pad(self,stream):

        pad_num=8 - (len(stream) % 8)

        if pad_num !=8:
            stream=stream+(pad_num*'0')

            return pad_num , stream

        else:

            return 0, stream


    def decode_bitMessage(self,bitemessage,reverse_dict):
        start=0
        end=1
        decodemess=""
        while end <= len(bitemessage):
            try:
                char=reverse_dict[bitemessage[start:end]]
                decodemess=decodemess+char
                start=end
                end=end+1

            except:
                end+=1

        return decodemess

    def decompress(self,compressed_file):

        self.compressed_name=compressed_file
        with open(self.compressed_name+".bin","rb") as f:

            import pickle
            import os
            file=f.read().split(b'\x80\x03}q\x00')
        self.reverseENC=pickle.loads(b'\x80\x03}q\x00'+file[-1]) #default pickl's byte identifier for dict , try pickle.dumps(dict())
        bitemessage=self.ByteToBit(file[0])
        info_bit=bitemessage[:8]
        isFile=int(info_bit[3])
        padding=int(info_bit[:3],2)

        if padding !=0 :

            bitemessage=bitemessage[8:-padding]
        else :

            bitemessage=bitemessage[8:]

        decodemess=self.decode_bitMessage(bitemessage,self.reverseENC)
        decodemess=decodemess.split("/EOF/")

        if isFile:

            filepath=os.path.join(os.getcwd(),decodemess[0])
            flag=True
            fullname=decodemess[0].rsplit(".",maxsplit=1)
            filname=fullname[0]
            extenssion="."+fullname[1]
            counter=1
            while flag:
                if not os.path.exists(filepath):
                    flag=False
                else :
                    fullname=filname+"Copy({})".format(counter)+extenssion
                    filepath=os.path.join(os.getcwd(),fullname)
                    counter+=1

            with open(filepath,"w") as file:
                file.write(decodemess[1])
        else :
            mydir=os.path.join(os.getcwd(),decodemess[0])
            flag=True
            counter=1
            while flag:
                try:
                    os.mkdir(mydir)
                    flag=False
                except:
                    mydir=mydir+"Copy({})".format(counter)
                    counter+=1

            numberoffiles=(len(decodemess)-2)//2
            j=1
            for i in range(1,numberoffiles+1):
                with open(os.path.join(mydir,decodemess[i]),"w") as file:
                    file.write(decodemess[i+numberoffiles])
                file.close()



    def makeMinheap(self,freq):
        import heapq
        min_heap=[]
        heapq.heapify(min_heap)
        for item in freq.items():
            heapq.heappush(min_heap,Node(item[0],item[1]))
        return min_heap

    def makeEncodings(self,freq):
        import heapq
        self.root=self.makeMinheap(freq)
        while(len(self.root)>1):

            nodeA=heapq.heappop(self.root)
            nodeB=heapq.heappop(self.root)
            parentNode=Node(key=None,freq=nodeA.freq+nodeB.freq)
            parentNode.childrenkeys= list(set(nodeA.childrenkeys+nodeB.childrenkeys))

            if nodeA<nodeB:
                nodeA.isRightNode="0"
                self.append_value_dict(nodeA.childrenkeys,nodeA.isRightNode)
                nodeB.isRightNode="1"
                self.append_value_dict(nodeB.childrenkeys,nodeB.isRightNode)
                parentNode.left=nodeA
                parentNode.right=nodeB
            else:
                nodeA.isRightNode="1"
                self.append_value_dict(nodeA.childrenkeys,nodeA.isRightNode)
                nodeB.isRightNode="0"
                self.append_value_dict(nodeB.childrenkeys,nodeB.isRightNode)
                parentNode.left=nodeA
                parentNode.right=nodeB
            nodeA.parent=nodeB.parent=parentNode
            heapq.heappush(self.root,parentNode)

        parentNode.isRightNode=None
        self.root=self.root[0]

    def append_value_dict(self,keys,ValuetoBeAdded):
        if type(keys) == list:
            for key in keys :
                self.encodings[key]=ValuetoBeAdded+self.encodings.get(key,"")
        else :
            self.encodings[keys]=ValuetoBeAdded+self.encodings.get(keys,"")

    def ByteToBit(self,byteString):

        return ''.join(format(byte, '08b') for byte in byteString)

    def bitToByte(self,bitString):
        return int(bitString, 2).to_bytes(len(bitString) // 8,byteorder='big')

    def get_compression_ratio(self):

        import os
        try:
            before=sum(os.path.getsize(f) for f in os.listdir(self.file.operating_path) if os.path.isfile(f))
        except:
            before=os.path.getsize(os.path.join(os.getcwd(),self.file.operating_path))

        after=os.path.getsize(os.path.join(os.getcwd(),self.desired_name+".bin"))
        ratio , cmp = "{:.2f}".format((before/after)), "{:.2f}%".format((after/before)*100)

        return ratio ,cmp

    def get_byte_dataframe(self):
        import pandas as pd
        df=pd.DataFrame(columns=["Character","ASCII","Frequency","Binary Representation","Huffman Representation"])
        temp=dict(((x[1],x[0]) for x in self.reverseENC.items()))
        temp.pop("/EOF/")
        temp=dict(sorted(temp.items(),key=lambda x:len(x[1])))
        for item in temp.items():
            char=item[0]
            df=df.append({"Character":char,"ASCII":ord(char),"Frequency":self.freq[char],"Binary Representation":format(ord(char), 'b'),"Huffman Representation":item[1]},ignore_index=True)
        return df

class Node():

    def __init__ (self,key,freq):
        self.freq=freq
        self.key=key
        self.parent=None
        self.left=None
        self.right=None
        self.isRightNode=""
        self.childrenkeys=[key]

    def __lt__ (self,another):

        return self.freq <= another.freq

    def __str__(self) :

        return f"Node with key =  {self.key} , freq = {self.freq} "

class My_File():

    #reads file or folder(iter and folder delimeter "/EOF/") and returns string and frequency dictionary

    def __init__(self,path):
        try:

            import os
            self.filename=path
            self.operating_path=os.path.join(os.getcwd(),self.filename)
            self.isFile=os.path.isfile(self.operating_path)
            if self.isFile:
                self.FilesNames=path
            else :
                self.FilesNames =os.listdir(self.operating_path)
                self.FilesNames.insert(0,self.filename)
        except:
            raise Exception("Target Not Found")


    def operate(self):
        import os
        if self.isFile:
            content,frequency = self.read_file(self.operating_path,self.isFile)
            return content,frequency

        else :
            contents=[]
            frequencies=[]

            for file in self.FilesNames[1:] :
                content , freq = self.read_file(os.path.join(self.operating_path,file),self.isFile)
                contents.append(content)
                frequencies.append(freq)
            content,frequency = self.combine(contents,frequencies)

            return content,frequency

    def read_file(self,path,isFile):

        with open(path,"r") as file:

            content=file.read()
            freq_dict={}

            for char in content:
                freq_dict[char]=freq_dict.get(char,0)+1

            for char in path.split("/")[-1]:
                freq_dict[char]=freq_dict.get(char,0)+1

            if isFile:
                content=self.FilesNames+"/EOF/"+content
                freq_dict["/EOF/"]=freq_dict.get("/EOF/",0)+1

            content=content+"/EOF/"
            freq_dict["/EOF/"]=freq_dict.get("/EOF/",0)+1

        return content,freq_dict

    def combine(self,contents,frequencies):
        from collections import Counter
        content= ''.join(contents)
        content="/EOF/".join(self.FilesNames)+"/EOF/"+content
        frequency={}
        for freq in frequencies:
            frequency = Counter(frequency) + Counter(freq)
        frequency=dict(frequency)
        frequency["/EOF/"]=frequency.get("/EOF/",0)+len(self.FilesNames)
        return content,frequency

class main():
    def menu(self):

        import time
        import pandas as pd
        from os import system
        import matplotlib.pyplot as plt
        system('clear')
        print("Welcome to Huffman Encoding")
        print("============================")
        try :
            x=int(input("1-Compress \n2-Decompress\n3-Quit\n"))
            my_huffman=Huffman_Encoding()
            if x not in [1, 2, 3]:
                raise Exception("Wrong Input")
        except :
            print("Please Enter a Valid Choice")
            time.sleep(3)
            self.menu()
        if x==1 :
            file_name = input("Please enter file(sample.txt)/folder(folder) name (in same directory): ")
            compression_name = input("Please enter compressed name (without .bin) (in same directory): ")
            try :
                start_time=time.time()
                my_huffman.compress(file_path=file_name,compression_name=compression_name)
                print("Time to compress : {:.2f} seconds ".format(time.time()-start_time))
                ratio, cmp = my_huffman.get_compression_ratio()
                print("Compression Ratio : {} , Compressed file is {} of the original : ".format(ratio, cmp))
                df=my_huffman.get_byte_dataframe().sort_values(by="Frequency", ascending=False)
                with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
                    print("Byte Dataframe \n",df)
                k=my_huffman.freq.copy()
                k.pop("/EOF/")
                plt.figure(figsize=(20,20))
                plt.bar(range(len(k)), list(k.values()), align='center')
                plt.title("Distribution of Characters in the File/Folder")
                plt.xticks(range(len(k)), list(k.keys()),rotation=45)
                plt.show()
                print("================")
                input("press enter to go to menu \n")
                self.menu()
            except :
                print("Error Finding the file")
                time.sleep(3)
                self.menu()

        elif x==2: #decompress
            file_name=input("Please enter filename to be decompressed (sample) without .bin (in same directory): ")
            try:
                start_time=time.time()
                my_huffman.decompress(compressed_file=file_name)
                print("Time to decompress : {:.2f} seconds ".format(time.time()-start_time))
                input("press enter to go to menu \n")
                self.menu()
            except :
                print("Error Finding the file")
                time.sleep(3)
                self.menu()
        else :
            return

s=main()
s.menu()
