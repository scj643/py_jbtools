__doc__ = '''Lib for managing dropbear instances
'''
import plistlib
import os
LAUNCH_DAEMONS = '/Library/LaunchDaemons/'

TEMPLATE_SETTINGS = {'Program': '/usr/local/bin/dropbear', 'RunAtLoad': True, 'KeepAlive': True, 'Label': 'DropBear', 'ProgramArguments': ['/usr/local/bin/dropbear', '-F', '-R', '-p', '127.0.0.1:22']}

class DropbearSettings (object):
    def __init__(self, plistdict):
        if plistdict['Program'] != '/usr/local/bin/dropbear':
            raise TypeError('Not a dropbear service')
        else:
            self.plistdict=plistdict
            if self.plistdict['Label'] == 'ShaiHulud':
                self.isDefault = True
            else:
                self.isDefault = False
        
    @property
    def ip_port(self):
        return self.plistdict['ProgramArguments'][-1]
        
    @ip_port.setter
    def ip_port(self, ip_string):
        if not self.isDefault:
            self.plistdict['ProgramArguments'][-1] = ip_string
        else:
            raise OSError('Not allowed to change default dropbear settings')
            
    @property
    def label(self):
        return self.plistdict['Label']
        
    @label.setter
    def label(self, name):
        if not self.isDefault:
            self.plistdict['label'] = name
        else:
            raise OSError('Not allowed to change default dropbear settings')
            
    def save(self, fname):
        plistlib.dump(self.plistdict, open(fname, 'wb'), ort_keys=False)
        
    def __repr__(self):
        return '<DropbearSettings label: {}, ip_port: {}>'.format(self.label, self.ip_port)


class DropbearItem (object):
    def __init__(self, filename, settings=None):
        self.file = LAUNCH_DAEMONS+filename
        if settings:
            if os.path.exists(self.file):
                raise AttributeError('File already exists')
            self.settings = DropbearSettings(settings)
            self.isNew = True
        else:
            self.settings = DropbearSettings(plistlib.load(open(self.file, 'rb')))
            self.isNew = False
            
            
    def save(self):
        '''save the object'''
        self.settings.save(self.file)
        
    def __repr__(self):
        return '<DropbearItem path: {}, isNew: {}>'.format(self.file, self.isNew)

def find_dropbear_services():
    matches = []
    for i in os.listdir(LAUNCH_DAEMONS):
        try:
            matches += [DropbearItem(i)]
        except:
            pass
            
    return matches


def find_dropbear_names():
    names = []
    for i in find_dropbear_services():
        names += [i.settings.label]
    return names
    
def make_new_dropbear(name, port, ip='127.0.0.1'):
    if name in find_dropbear_names():
        raise NameError("can't use name, pick another")
    settings = TEMPLATE_SETTINGS
    settings['Label'] = name
    settings['ProgramArguments'][-1] = '{}:{}'.format(ip, port)
    return DropbearItem(name+'.plist', settings=settings)
