import paramiko
import console
from binascii import hexlify
import os

known_hosts = os.path.expanduser('~/.ssh/known_hosts')

class PromptHost (paramiko.MissingHostKeyPolicy):
    def missing_host_key(self, client, hostname, key):
        choice = console.alert('Add Unknown Key', 'Accept key: {key} for host: {host}: {fingerprint}'.format(key=key.get_name(), host=hostname, fingerprint = hexlify(key.get_fingerprint())), 'Yes', 'Not Now', 'No', hide_cancel_button=True)
        if choice == 1:
            client._host_keys.add(hostname, key.get_name(), key)
            if client._host_keys_filename is not None:
                client.save_host_keys(client._host_keys_filename)
            client._log(paramiko.client.DEBUG, 'Adding %s host key for %s: %s' %
                    (key.get_name(), hostname, hexlify(key.get_fingerprint())))
        
        if choice == 2:
            paramiko.client.warnings.warn('Unknown {} host key for {}: {}'.format(key.get_name(), hostname, hexlify(key.get_fingerprint())))
                      
        if choice == 3:
            client._log(paramiko.client.DEBUG, 'Rejecting {} host key for {}: {}'.format(key.get_name(), hostname, hexlify(key.get_fingerprint())))
            raise paramiko.client.SSHException('Server {} not found in known_hosts'.format(hostname))
        
        
class LocalSSH (object):
    def __init__(self, host='127.0.0.1', port=9022, user='mobile', passwd=None, privatekey=None):
        '''LocalSSH session
        :host: the default is localhost (127.0.0.1)
        :port: can't be the default 22 since iOS doesn't allow that
        :user: user to login in as
        passwd: can be ignored will be prompted for later
        pirvatekey: 
        '''
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.load_host_keys(known_hosts)
        self.client.set_missing_host_key_policy(PromptHost())
        if not passwd:
            passwd = console.password_alert('SSH password for {user}@{host}'.format(user=user, host=host))
            
        if not privatekey:
            self.client.connect(host,
                                    username=user,
                                    password=passwd,
                                    port=port)
        else:
            try:
                self.client.connect(host,
                                    username=username,
                                    password=passwd,    
                                    port=port,
                                    key_filename=privatekey)
            except paramiko.SSHException as e:
                print('Failed to login with SSH Keys: {}'.format(repr(e)))
        

if __name__ == '__main__':
    s = LocalSSH(user='root')
