#!/usr/bin/env python2.7
#coding=utf-8
#the raw copy from web
#author@alingse
#2016.08.1

from __future__ import with_statement

import argparse
import os

def truncate_tail(file,number,size=10240,nothalf=False,test=False):
    with open(file,'r+b') as f:
        #seek END
        f.seek(0, os.SEEK_END)
        end = f.tell()
        _end = end
        _number = number

        #only patch the last line
        last = True
        while end >0 and number > 0:
            if end < size:
                size = end

            f.seek(-1*size, os.SEEK_CUR)
            #data block
            data = f.read(size)
            lines = data.split('\n')
            
            #'wwww\nsfds\nss\nwww'
            #['wwww','sfds','ss','www']
            #通常lines最后一个半行应该算到上一次读的那一行里面,所以应该去掉
            #但是文件末尾这一个半行也算做一行,因此这里有一个patch
            if not last:
                lines.pop()
            else:
                #last line is half line
                if data[-1] != '\n' and nothalf:
                    print('last line if half line ! (not end with \'\n\' )')
                    return 2
                #last line in a completed line
                #pop the [....,'']
                if data[-1] == '\n':
                    lines.pop()
                last = False

            #lines
            count = len(lines)

            if count <= number:
                number = number - count
                end = end - size
                #seek back -- read把指针移走了了
                f.seek(-1*size, os.SEEK_CUR)
            else:
                #pop number lines
                for i in range(number):
                    lines.pop()

                back_data = '\n'.join(lines)+'\n'
                pop_size = size - len(back_data)

                #seek back from the read
                #seek back -- read把指针移走了了
                f.seek(-1*pop_size, os.SEEK_CUR)
                end = end - pop_size
                number = 0

        if end == 0 and number >= 0:
            print("No change: requested removal would leave empty file: {} bytes,{} lines".format(_end,_number - number))
            return 3
        if end >0 and number == 0:
            if test:                
                print("will Remove {} lines && {} bytes from end of file".format(_number,_end - end))
            else:
                f.truncate()
                print("Removed {} lines && {} bytes from end of file".format(_number,_end - end))
            return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='the file to truncate')
    parser.add_argument('number',type=int,help='line number to truncate')
    parser.add_argument('-s','--size',type=int,default=10240,help='read buffer size in byte')
    parser.add_argument('--nothalf',default=False,action='store_true',help='check the last line is half line')
    parser.add_argument('--test',action='store_true',help='just test and will not truncate it(help you find the right size)')
    args = parser.parse_args()
        
    file = args.file
    number = args.number
    size = args.size
    nothalf = args.nothalf
    test = args.test
    if test:
        print('It\'s just a test')
    truncate_tail(file,number,size=size,nothalf=nothalf,test=test)
