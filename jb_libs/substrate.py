__doc__ = '''A library for looking at substrate tweaks and what they are hooking into'''
import plistlib
import os
from glob import glob
SUBSTRATE_PATH = '/Library/MobileSubstrate/DynamicLibraries'

def parse_tweak_plist(fpath):
    try:
        return plistlib.load(open(fpath, 'rb'))
    except:
        string = open(fpath, 'r').read()
        string = string.strip(';').strip('\r').strip('\n')
        return string
    
class Tweak (object):
    def __init__(self, plistpath):
        self.string = parse_tweak_plist(plistpath)
            
class TweakItems (object):
    def __init__(self):
        self.plists = glob('{}/**/*.plist'.format(SUBSTRATE_PATH), recursive=True)
        self.tweaks = [Tweak(path) for path in self.plists]
        
        
if __name__ == '__main__':
    t = TweakItems()
    pass
