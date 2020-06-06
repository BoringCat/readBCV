from xml.etree import ElementTree as ET
import argparse
import os

def getArgs():
    parse = argparse.ArgumentParser("组合metalink文件")
    parse.add_argument(metavar='file', dest='files', nargs='*', help='从readbcv下载的metafile文件')
    parse.add_argument('-d', '--dir', help='下载到同一目录下', dest='dirname', default=None)
    return parse.parse_args()

def _addToCompose(files, _file):
    for add_file in ET.parse(_file).getroot().find('{http://www.metalinker.org/}files'):
        files.append(add_file)

def ComposeFiles(filelist, dirname = None):
    basefile = filelist[0]
    filelist = filelist[1:]
    tree = ET.parse(basefile)
    root = tree.getroot()
    files = root.find('{http://www.metalinker.org/}files')
    for file_ in filelist:
        _addToCompose(files,file_)
    if dirname:
        for f in files:
            oname = f.get('name')
            nname = '%s/%s' % (dirname, os.path.split(oname)[-1])
            f.set('name', nname)
    return tree

if __name__ == "__main__":
    args = getArgs()
    files = tuple(filter(lambda x: os.path.exists(x) and (x.endswith('metalink') or x.endswith('meta4')), args.files))
    if not files:
        exit(1)
    print('组合 [%s] 到 compose.meta4 里面' % ', '.join(files), end='')
    if args.dirname:
        print('，同时修改下载目录为：%s' % args.dirname,end='')
    print('。')
    ctree = ComposeFiles(files, args.dirname)
    ctree.write('compose.meta4', 'UTF-8')
