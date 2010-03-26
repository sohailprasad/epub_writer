#!/usr/bin/python

import sys , os , simplejson
from optparse import OptionParser
import models

def main():
    usage = "usage: %prog [options] keyword"
    parser = OptionParser(usage)
    parser.add_option("-d" , "--dir" , dest="dir", type="string",action="store",
                  help = "epub convert from Directory" )
    ( options ,args ) = parser.parse_args()
    if not options.dir: 
        parser.error("requires -d")

    ( filename , images ) = open_directory( options.dir )
    if not images :
        parser.error("directory is not open . directory not exists 'images' directory ")
        
    create_ncx(filename=filename , images=images)

def create_ncx(*args,**kwargs):
    hoge = models.NCXDocument(kwargs)


def open_directory(path):
    images = []
    if not  os.access(path,os.R_OK):
        return False
    dirname = path.split("/")
    dirname.reverse()
    dirname.remove("")
    filename = dirname.pop(0)
    
    if not "images" in  os.listdir(path) :
        return False
    else:
        for root,dirs,files in os.walk( path + "/images"):
            if not len(files) > 0 : continue
            for file in files :
                images.append( file )
    return filename , images



if __name__ == "__main__":
    main()
