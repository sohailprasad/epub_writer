from xml.dom.minidom import getDOMImplementation

class DocumentRoot():
    def __init__(self):
        self.impl = getDOMImplementation()
        
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
        docTitle = doc.createElement("docTitle")
        text = doc.createElement("text")
        text.appendChild( doc.createTextNode( kwargs.get("filename") ) )
        docTitle.appendChild( text ) 
        root.appendChild( head )
        root.appendChild( docTitle )

        print doc.toxml()
