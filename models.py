from xml.dom.minidom import getDOMImplementation
from getimageinfo import getImageInfo

class DocumentRoot():
    def __init__(self):
        self.impl = getDOMImplementation()

class ContentXHtml(DocumentRoot):
    def __init__(self,i,image):
        self.filename = "contents%s.xhtml" % ( str(i).zfill(5)  )
        super = DocumentRoot()
        doctype = super.impl.createDocumentType("html" , "-//W3C//DTD XHTML 1.0 Strict//EN" , "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd" )
        doc = super.impl.createDocument("html","html",doctype)
        html = doc.documentElement
        html.setAttribute("xmlns" , "http://www.w3.org/1999/xhtml")
        head = doc.createElement("head")
        html.appendChild( head )

        body = doc.createElement("body")
        div = doc.createElement("div")
        h1 = doc.createElement("h1")
        h1.setAttribute("title" , "title")
        h1.setAttribute("id" , "page%s" % ( i ) )
        img = doc.createElement("img")
        img.setAttribute("src" , "../images/%s" % ( image ) )
        h1.appendChild( img )
        div.appendChild( h1 )
        body.appendChild( div )
        html.appendChild( body )

        self.doc = doc

        
class OpfDocument(DocumentRoot):
    filename = "content.opf"
    
    def __init__(self,kwargs):
        super = DocumentRoot()
        doc = super.impl.createDocument("package","package",None)
        package = doc.documentElement
        package.setAttribute("xmlns" , "http://www.idpf.org/2007/opf")
        package.setAttribute("unique-identifier" , "BookID")
        package.setAttribute("version" , "2.0")
        metadata = doc.createElement("metadata")
        metadata.setAttribute("xmlns:dc" , "http://purl.org/dc/elements/1.1/")
        metadata.setAttribute("xmlns:opf" , "http://www.idpf.org/2007/opf")
        package.appendChild( metadata ) 
        dc = doc.createElement("dc:title")
        dc.appendChild( doc.createTextNode( kwargs.get("filename") ) )
        metadata.appendChild(dc)
        if kwargs.get("creator"):
            dc = doc.createElement("dc:creator")
            dc.setAttribute("opf:role" , "aut")
            dc.appendChild( doc.createTextNode( kwargs.get("creator") ) )
            metadata.appendChild(dc)

        if kwargs.get("language"):
            dc = doc.createElement("dc:language")
            dc.appendChild( doc.createTextNode( kwargs.get("language") ) )
            metadata.appendChild(dc)

        if kwargs.get("identifier"):
            dc = doc.createElement("dc:identifier")
            dc.setAttribute("id" , "BookID")
            dc.setAttribute("opf:scheme" , "UUID" )
            dc.appendChild( doc.createTextNode( kwargs.get("identifier") ) )
            metadata.appendChild(dc)

        meta = doc.createElement("meta")
        meta.setAttribute("name" , "Sigil Version")
        meta.setAttribute("content","0.1.8")
        metadata.appendChild( meta )

        manifest = doc.createElement("manifest")
        item = doc.createElement("item")
        item.setAttribute("id" , "ncx")
        item.setAttribute("href" , "toc.ncx")
        item.setAttribute("media-type" , "application/x-dtbncx+xml")
        manifest.appendChild( item )

        for image in kwargs.get("images") :
            info = getImageInfo( open(image,"r").read() ) 
            filename = image.split("/").pop()
            item = doc.createElement("item")
            item.setAttribute("id" , filename)
            item.setAttribute("href" , "images/" + filename )
            item.setAttribute("media-type" , info[0] )
            manifest.appendChild( item )


        for content in kwargs.get("contents") :
            item = doc.createElement("item")
            item.setAttribute("id" , content )
            item.setAttribute("href" , "text/" + content )
            item.setAttribute("media-type" , "application/xhtml+xml" )
            manifest.appendChild( item )

        package.appendChild( manifest ) 

        spine = doc.createElement("spine")
        spine.setAttribute("toc" , "ncx")

        for content in kwargs.get("contents") :
            itemref = doc.createElement("itemref")
            itemref.setAttribute("idref" , content )
            spine.appendChild( itemref )

        package.appendChild( spine )

        guide = doc.createElement("guide")
        reference = doc.createElement("reference")
        reference.setAttribute("type" , "cover")
        reference.setAttribute("title" , kwargs.get("filename") )
        reference.setAttribute("href" , "text/" + kwargs.get("contents").pop(0) )
        guide.appendChild( reference )
        package.appendChild( guide )
        self.doc = doc


class ContainerDocument(DocumentRoot):
    filename = "container.xml"

    def __init__(self):
        super = DocumentRoot()
        doc = super.impl.createDocument("container","container",None)
        container = doc.documentElement
        container.setAttribute("version" , "1.0")
        container.setAttribute("xmlns" , "urn:oasis:names:tc:opendocument:xmlns:container")
        rootfiles = doc.createElement("rootfiles")
        rootfile = doc.createElement("rootfile")
        rootfile.setAttribute("full-path" , "OEBPS/content.opf")
        rootfile.setAttribute("media-type" , "application/oebps-package+xml")
        rootfiles.appendChild( rootfile )
        container.appendChild( rootfiles ) 
        self.doc = doc

        
class NCXDocument(DocumentRoot):
    filename = "toc.ncx"

    def __init__(self,kwargs):
        super = DocumentRoot()
        doctype = super.impl.createDocumentType("ncx" , "-//NISO//DTD ncx 2005-1//EN" , "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd" )
        doc = super.impl.createDocument("ncx","ncx",doctype)
        root = doc.documentElement
        root.setAttribute("xmlns","http://www.daisy.org/z3986/2005/ncx/")
        root.setAttribute("version" , "2005-1")
        head = doc.createElement("head")
        meta = doc.createElement("meta")
        meta.setAttribute("name" , "dtb:uid")
        meta.setAttribute("content" , "c3a45484-0e73-45c2-a17f-a1b1a6d7c145")
        head.appendChild( meta )
        meta = doc.createElement("meta")
        meta.setAttribute("name" , "dtb:depth")
        meta.setAttribute("content" , "1")
        head.appendChild(meta)
        meta = doc.createElement("meta")
        meta.setAttribute("name" , "dtb:totalPageCount")
        meta.setAttribute("content" , "0")
        head.appendChild(meta)
        meta = doc.createElement("meta")
        meta.setAttribute("name" , "dtb:maxPageNumber")
        meta.setAttribute("content" , "0")
        head.appendChild(meta)
        root.appendChild( head )

        docTitle = doc.createElement("docTitle")
        text = doc.createElement("text")
        text.appendChild( doc.createTextNode( kwargs.get("filename") ) )
        docTitle.appendChild( text ) 
        root.appendChild( docTitle )
        
        navMap = doc.createElement("navMap")
        i = 1
        #for imgsrc in kwargs.get("images"):
        for content in kwargs.get("contents") :
            navPoint = doc.createElement("navPoint")
            navPoint.setAttribute("id" , "navPoint-%s" % ( i ) )
            navPoint.setAttribute("playOrder" , "%s" % ( i ) )
            navLabel = doc.createElement("navLabel")
            text = doc.createElement("text")
            text.appendChild( doc.createTextNode( "page%s" % (i)  ) )
            navLabel.appendChild( text ) 
            navPoint.appendChild( navLabel )
            cont = doc.createElement("content")
            cont.setAttribute("src" , "text/" + content ) 
            navPoint.appendChild( cont ) 
            navMap.appendChild( navPoint )
            i+=1
        root.appendChild( navMap )

        self.doc = doc
