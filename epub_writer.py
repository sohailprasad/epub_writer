#!/usr/bin/python

import sys , os , tempfile , shutil , zipfile , re
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

    tmpdir = tempfile.mkdtemp()
    os.makedirs( os.path.join(tmpdir , "OEBPS") )
    os.makedirs( os.path.join(tmpdir , "OEBPS" , "images")  )
    os.makedirs( os.path.join(tmpdir , "OEBPS", "text")  )
    os.makedirs( os.path.join(tmpdir ,"META-INF") )
    
    create_mimetype(outdir=tmpdir,)
    create_container(outdir=os.path.join( tmpdir , "META-INF") )
    images = copy_images(images=images,outdir=os.path.join( tmpdir , "OEBPS" , "images") )
    contents = create_text_contents(images=images,outdir=os.path.join( tmpdir , "OEBPS" , "text" ) )
    create_ncx(filename=filename , images=images , outdir=os.path.join( tmpdir , "OEBPS") ,contents=contents )
    create_opf(filename=filename,images=images,contents=contents,outdir=os.path.join(tmpdir , "OEBPS") )
    dst_path = create_zip(filename=filename,tmpdir=tmpdir,outdir="/home/mizzu/tmp/")

    os.rename( dst_path , re.compile("\.zip$").sub( ".epub" , dst_path )  )

    rmdirs = []
    for root,dirs,files in os.walk( tmpdir ):
        for file in files :
            os.remove( os.path.join( root , file ) )
        rmdirs.append( os.path.join( root ,file ) )

    rmdirs.reverse()
    for dir in rmdirs :
        os.rmdir( "/".join( [ str(x) for x in dir.split("/")[0:-1] ] ) )

def create_zip(*args,**kwargs):
    path = kwargs.get("outdir") + kwargs.get("filename") + ".zip"
    zip = zipfile.ZipFile( path  ,"w" , zipfile.ZIP_DEFLATED )
    reg = None
    for root,dirs,files in os.walk( kwargs.get("tmpdir") ):
        if not reg : reg = re.compile( str( root )  ) 
        for file in files :
            relative = re.compile("^/").sub("" , reg.sub("" , root ) )
            zip.write( os.path.join(root,file) , os.path.join( relative , file ) )
    zip.close()
    return path


def create_opf(*args,**kwargs):
    opfDocument = models.OpfDocument(kwargs)
    f = open( os.path.join( kwargs.get("outdir") , opfDocument.filename ) , "w")
    f.write( opfDocument.doc.toxml() )
    f.close()

def create_text_contents(*args,**kwargs):
    contents = []
    i = 1
    for image in kwargs.get("images"):
        contentXHTML = models.ContentXHtml(i , image.split("/").pop() )
        i+=1
        
        f = open( os.path.join(  kwargs.get("outdir") , contentXHTML.filename ) , "w")
        f.write( contentXHTML.doc.toxml() )
        f.close()
        contents.append( contentXHTML.filename )
    return contents

def copy_images(*args,**kwargs):
    images = []
    for img in kwargs.get("images"):
        fname = img.split("/").pop()
        shutil.copyfile( img , os.path.join( kwargs.get("outdir") , fname)  )
        images.append( kwargs.get("outdir") + "/" + fname )

    return images

def create_container(*args,**kwargs):
    containerDocument = models.ContainerDocument()
    f = open( os.path.join( kwargs.get("outdir") ,  containerDocument.filename ) , "w")
    f.write( containerDocument.doc.toxml() )
    f.close()

def create_mimetype(*args,**kwargs):
    f = open( os.path.join( kwargs.get("outdir") , "mimetype" ) , "w" )
    f.write("application/epub+zip")
    f.close()

def create_ncx(*args,**kwargs):
    ncxDocument = models.NCXDocument(kwargs)
    f = open( os.path.join( kwargs.get("outdir") , ncxDocument.filename ) , "w")
    f.write( ncxDocument.doc.toxml() )
    f.close()

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
                images.append( root + "/" + file )
    return filename , images



if __name__ == "__main__":
    main()
