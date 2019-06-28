FILE_DIR = "Files"
SCRIPT_HEADER_1 = """<?xml version='1.0' encoding='utf-8'?>
            <html xmlns="http://www.w3.org/1999/xhtml">
            <head>
              <title>"""
SCRIPT_HEADER_2 = """</title>
              <link rel="stylesheet" href="script.css" />
            </head>
            <body>"""
SCRIPT_FOOTER = """</div></body></html>"""
TOC_HEADER = """<?xml version='1.0' encoding='utf-8'?>
                <ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="en">
                  <head>
                    <meta content="be2d5873-0d20-46f6-93a2-5253d7a9c50a" name="dtb:uid"/>
                    <meta content="3" name="dtb:depth"/>
                    <meta content="calibre (3.28.0)" name="dtb:generator"/>
                    <meta content="0" name="dtb:totalPageCount"/>
                    <meta content="0" name="dtb:maxPageNumber"/>
                  </head>
                  <docTitle>
                    <text>Game of Thrones - Season 8 Scripts</text>
                  </docTitle>
                  <navMap>"""
TOC_FOOTER = """  </navMap>
                </ncx>
                """
NAV_POINT_EPISODE = """<navPoint id="num_{}" playOrder="{}">
                          <navLabel>
                            <text>{}</text>
                          </navLabel>
                          <content src="{}.xhtml"/>
                          {}
                        </navPoint>"""
NAV_POINTS_SUBCHAPTER = """<navPoint id="num_{}" playOrder="{}">
                            <navLabel>
                              <text>{}</text>
                            </navLabel>
                            <content src="{}.xhtml"/>
                          </navPoint>"""
METADATA_HEADER = """<?xml version='1.0' encoding='utf-8'?>
                        <package xmlns="http://www.idpf.org/2007/opf" unique-identifier="uuid_id" version="2.0">
                          <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
                            <dc:identifier opf:scheme="calibre" id="calibre_id">1220ec95-41b4-4bb4-b84e-ba3ff45f156d</dc:identifier>
                            <dc:identifier opf:scheme="uuid" id="uuid_id">be2d5873-0d20-46f6-93a2-5253d7a9c50a</dc:identifier>
                            <dc:title>Game of Thrones - Season 8 Scripts</dc:title>
                            <dc:creator opf:file-as="Unknown" opf:role="aut">Alice Shipwise</dc:creator>
                            <dc:contributor opf:file-as="calibre" opf:role="bkp">calibre (3.28.0) [https://calibre-ebook.com]</dc:contributor>
                            <dc:language>eng</dc:language>
                            <meta name="cover" content="cover"/>
                          </metadata>"""

STYLE_FILENAME = """script.css"""
METADATA_FILENAME = """metadata.opf"""
TOC_FILENAME = """toc.ncx"""

METADATA_FOOTER = """<guide>
                        <reference href="titlepage.xhtml" title="Cover" type="cover"/>
                        </guide>
                      </package>"""
MANIFEST_START = """<manifest>"""
MANIFEST_ITEM = """<item href="{}" id="{}" 
                    media-type="{}"/>"""
MANIFEST_TYPE_XHTML = """application/xhtml+xml"""
MANIFEST_TYPE_CSS = """text/css"""
MANIFEST_TYPE_NCX = """application/x-dtbncx+xml"""
MANIFEST_END = """</manifest>"""

SPINE_START = """<spine toc="ncx">"""
SPINE_ITEM = """<itemref idref="{}"/>"""
SPINE_END = """</spine>"""

NUMBER_OF_RELEVENT_LINKS = 52
STYLE_TO_DELETE = 'margin-bottom: 2em;'

MIMETYPE_FILE = """mimetype"""
MIMETYPE = """application/epub+zip"""

META_INF_DIR = """META-INF"""
META_INF_FILE = """container.xml"""
META_INF_FILE_CONTENTS = """<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
   <rootfiles>
      <rootfile full-path="metadata.opf" media-type="application/oebps-package+xml"/>
   </rootfiles>
</container>
    """

START_FILENAME = """start.xhtml"""
START_CONTENTS = """<?xml version='1.0' encoding='utf-8'?>
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">

<head>
  <title>Game of Thrones - Season 8 Scripts</title>
</head>

<body>

  <h1>Game of Thrones - Season 8 Scripts</h1>
  <h2>by Alice Shipwise</h2>
  <p>Based on the book series "A Song of Ice and Fire" by George R.R. Martin 
  and the TV series "A Game of Thrones"</p>
  <p style="color: gray; size: 8pt">Compiled to e-book format by 
  u/CanzonELaLa</p>

</body>

</html>"""

STYLE = """
#script {
    margin-left: auto;
    margin-right: auto;
    width: 100%;
    max-width: 615px;
    font-size: 16px;
    line-height: 16px;
    font-family: "Courier Prime", "Courier New", monospace;
    word-wrap: break-word;
    padding: 1em 0em 2em 0em;
}

@media screen and (max-width: 615px) {
    #script {
        margin-left: 0;
        margin-right: 0;
        padding: 1em 1em 2em 1em;
    }
}

.Slugline { font-weight: bold; text-transform: capitalize;}

.Action, .Slugline, .Shot, .Act, .Transition, .Text, .Character, .Paren, .Dialog {
    white-space: pre-wrap;
}


.Slugline, .Shot, .Act, .Transition, .Character  { text-transform: uppercase; }
.Act { text-align: center; text-decoration: underline; }

.Action, .Text, .Act, .Slugline, .Shot, .Transition { margin-top: 1em; max-width: 615px; width: 100%; }
.Character { margin-top: 1em; max-width: 385px; }
.Slugline, .Shot, .Transition, .Discussion { margin-top: 2em; }
/*.Transition { text-align: right; }*/
.Paren { margin-left: 15%; max-width: 245px; }
.Dialog { max-width: 355px; }

.Character { margin-left: 34%; }
.Paren { margin-left: 23.5%; margin-right: 15%; }
.Dialog { margin-left: 17%; margin-right: 10%; }

.Clear { clear: both; }
.Dual { float: left; width: 48%; }
.Left { padding-right: 2%; }
.Right { padding-right: 2%; }

.Dual .Character { margin-left: 0; text-align: center; }
.Dual .Paren { margin-left: 9%; margin-right: 9%; }
.Dual .Dialog { margin-left: 0; margin-right: 0; }

.page_num {
    text-align: right;
    height: 0px;
    top: -12px;
    position: relative;
}

"""
