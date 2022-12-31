#!/data/data/com.termux/files/usr/bin/python

import PyPDF2
import sys
import re
import tld
from random import randint

version = 'v1.2'
buildOpts = ['-h', '-v', '-p', '-C', '-x', '-o', '--help', '--version']

## Functions
def findUrls(string):
  regex = r"\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\%\:\.-]*)*/?)\b"
  
  urls = re.findall(regex, string)
  return urls

def getFromTxtf(fname):
  txtLinks = []
  txtf = open(fname, 'r')
  rtn = findUrls(txtf.read())
  txtf.close()
  return rtn

def getFromPdf(fname):
  pdfLinks = []
  PDFFile = open(fname, 'rb')
  PDF = PyPDF2.PdfReader(PDFFile)
  pages = len(PDF.pages)
  key = '/Annots'
  uri = '/URI'
  ank = '/A'

  for page in range(pages):
    pageSliced = PDF.pages[page]
    ## Text links
    pdfText = pageSliced.extract_text()
    for textLinks in findUrls(pdfText):
      pdfLinks.append(textLinks)
  
    ## Hyper links
    pageObject = pageSliced.get_object()
    if key in pageObject.keys():
      ann = pageObject[key]
      for a in ann:
        u = a.get_object()
        if uri in u[ank].keys():
          pdfLinks.append(u[ank][uri])
  PDFFile.close()
  return pdfLinks
  
  
def saveAsFile(dlist, fname = True):
  if type(fname) is str:
    if not fname.endswith('.txt'):
      fname = fname + '.txt'
  elif fname == True:
    fname = 'links_{}.txt'.format(randint(1111111, 9999999))
  sfile = open(fname, 'w')
  sfile.writelines('%s\n' % itm for itm in dlist)
  sfile.close()
  return [fname, len(dlist)]

def printList(alist):
  for itm in alist:
    print(itm)
    
def sub_tld(dom):
  try:
    return tld.get_tld(dom, fix_protocol=True)
  except:
    return False

def domClean(dlist, clean, subdo):
  opList = []
  if clean:
    for li in dlist:
      try:
        the_tld = tld.get_tld(li, as_object=True, fix_protocol=True)
        if subdo:
          if sub_tld(the_tld.subdomain):
            opList.append(tld.get_fld(the_tld.subdomain, fix_protocol=True))
          else:
            opList.append(the_tld.fld)
        else:
          opList.append(the_tld.fld)
      except:
        pass
    return opList
  else:
    return dlist

def parseOpt(opt):
  if not opt.startswith('--') and opt.startswith('-') and len(opt) > 2:
    return ['-'+x for x in opt[1:]]
  else:
    return opt

def checkOpts(ins, build):
  notFound = False
  nfArr = []
  for i in ins:
    if i not in build:
      notFound = True
      nfArr.append(i)
    
  if notFound:
    return [False, nfArr]
  else:
    return [True]

def printHelp():
  print(f"""
Usage: exli [options] [filename.ext] [-o] [output_file_name.txt]

  Extract all links from a pdf file or any txt file.

Options:
  -p               Extract links from a pdf file
  -C               Extract only domain names from links
  -o               Save links in a file
  -x               Extract domain from subdomain
  -v, --version    Print program version
  -h, --help       Print this help page

Example usage:
  * Print link in terminal from txt file
    \033[1;32mexli file.txt\033[0m
  * Print link in terminal from pdf file
    \033[1;32mexli -p file.pdf\033[0m
  * Print clean domain names in terminal
    \033[1;32mexli -pC file.pdf\033[0m
  * Save links in a randomly generated filename
    \033[1;32mexli -o file.pdf\033[0m
  * Save clean domain names in a randomly generated filename
    \033[1;32mexli -oC file.pdf\033[0m
  * Save links from pdf to a text file from given file name
    \033[1;32mexli -p file.pdf -o output.txt\033[0m
  
Version: {version}
  """.strip())
  
  exit()
  
  

## -----------------
## Main Program

argvs = sys.argv
pdf = False
clean = False
extsd = False
otFile = False
optNotFound = False
errOpt = ""

opts = [opt for opt in argvs[1:] if opt.startswith("-")]
args = [arg for arg in argvs[1:] if not arg.startswith("-")]

if len(args) == 0:
  printHelp()


# Argument controllers

if '-h' in opts or '--help' in opts:
  printHelp()
elif '-v' in opts or '--version' in opts:
  print(version)
  exit()


if len(opts) > 0:
  if len(opts[0]) > 2:
    opts.insert(0, parseOpt(opts.pop(0)))
    
  cO1 = checkOpts(opts[1:] if type(opts[0]) is list else opts, buildOpts) 
  if cO1[0] == False:
    optNotFound = True
    errOpt = cO1[1][0]
  else:
    if type(opts[0]) is list:
      cO = checkOpts(opts[0], buildOpts)
      if cO[0] == False:
        optNotFound = True
        errOpt = cO[1][0]
      else:
        if '-p' in opts[0]:
          pdf = True
        if '-C' in opts[0]:
          clean = True
        if '-x' in opts[0]:
          extsd = True
        if '-o' in opts[0]:
          if len(args) > 1:
            otFile = args[1]
          else:
            otFile = True
    else:
      if '-p' in opts:
        pdf = True
      if '-C' in opts:
        clean = True
      if '-x' in opts:
        extsd = True
  
    if '-o' in opts:
      if not '-o' in opts[0]:
        if len(args) > 1:
          otFile = args[1]
        else:
          otFile = True
    
  if optNotFound:
    print('Unknown option: {}'.format(errOpt))
    printHelp()


if pdf:
  pdfLinksList = domClean(getFromPdf(args[0]), clean, extsd)
  
  if otFile == False:
    printList(pdfLinksList)
  else:
    opfname = saveAsFile(pdfLinksList, otFile)
    print(f'{opfname[1]} links are saved to file: \033[1;33m{opfname[0]}\033[0m')
    
else:
  txtLinksList = domClean(getFromTxtf(args[0]), clean, extsd)
  
  if otFile == False:
    printList(txtLinksList)
  else:
    opfname = saveAsFile(txtLinksList, otFile)
    print(f'{opfname[1]} links are saved to file: \033[1;33m{opfname[0]}\033[0m')
    
