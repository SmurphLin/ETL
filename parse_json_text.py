import os
import sys
import io
import contextlib


class DataStream(object):
    """read in text json stream"""

    def __init__(self, file_name):
        """constructor"""
        try:
            if os.path.isfile(file_name):
                self.file = file_name
        except FileNotFoundError:
            print("ERROR: File not found\n")
        except FileExistsError:
            print("ERROR: File does not exist\n")
        except OSError:
            print("ERROR: OS error was raised\n")
        except Exception:
            print("ERROR: Uncaught exception was raised\n")

        self.read_FILE = None
        self.is_open = False
        self.ordered_structs_list = []
        self.ordered_sub_structs_list = []


    def __enter__(self):
        """open the file-stream"""
        if self.is_open is False:
            self.is_open = True
            try:
                self.read_FILE = open(self.file, 'r')
            except BufferError:
                print("READ FILE ERROR: could not open file for reading\n")
            except Exception:
                print("ERROR: Uncaught exception was thrown\n")
        else:
            print("Stream is already opened for reading\n")

    def close_stream(self):
        """close the file-stream"""
        if self.is_open is True:
            self.read_FILE.close()
            print("closing the file stream\n")
            self.is_open = False
        else:
            print("File stream is already closed \n")

    def parse_text_stream(self):
        """parse through text stream"""
        while True:
            try:
                brkt_cntr = 0
                c = self.read_FILE.read(1)
                if c == '{' and brkt_cntr == 0:
                    brkt_cntr += 1
                    STRUCT = Structure()
                    sub_struct = STRUCT.children
                    temp = []
                    sub_list = []
                    while c!= ':':
                        c = self.read_FILE.read(1)

                        temp.append(*c)
                        formatted_key = ''.join(temp).rstrip(':')
                        STRUCT.fill(formatted_key)
                        self.ordered_structs_list.append(STRUCT.Struct)
                        break

                    while brkt_cntr != 0:
                        c = self.read_FILE.read(1)
                        sub_list.append(*c)
                        if c == "{":
                            brkt_cntr += 1
                        if c == "}" and brkt_cntr > 1:
                            brkt_cntr-= 1
                        if c == "}" and brkt_cntr <= 1:
                            brkt_cntr -= 1
                            sub_list.append(*c)
                            formatted_sub_list = ''.join(sub_list)
                            self.ordered_sub_structs_list.append(sub_struct.append(formatted_sub_list))
                            break
                    break
            except StopIteration as e:
                break




class Structure(object):
    """Structure is a data structure
    that holds the text processed json stream"""

    def __init__(self):
        """init method"""
        self.Struct = []
        self.children = []

    def fill(self, data: str):
        """append characters into the Struct"""
        self.Struct.append(data)

    def fill_sub_struct(self, data: str):
        self.children.append(data)

    def __len__(self):
        """return the size of the Struct"""
        return len(self.Struct)

    def is_empty(self):
        if self.Struct.__len__() == 0:
            return True
        else:
            return False


