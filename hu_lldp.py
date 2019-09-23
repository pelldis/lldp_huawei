#!/usr/bin/python

import pexpect
import getpass

#Function for connecting to device
# need ip address in format 1.1.1.1 to connect
def connect_to_device(ip):
    print "Connecting to device: " + ip
    #login = 'admin'
    #password = 'Juniper'
    global ssh
    try:
        ssh = pexpect.spawn('ssh ' + login + '@' +ip, timeout=4)
        next_step = ssh.expect(['password\:', 'no\)?'])
        if next_step == 0:
            ssh.sendline(password)
            ssh.expect('>')
            print 'Connected'
        elif next_step == 1:
            print 'Saving new ssh key for connecting device...'
            ssh.sendline('yes')
            ssh.expect('password\:')
            ssh.sendline(password)
            ssh.expect('>')
            print 'Connected'
        return True
    except:
        print "\n\nLooks line your ssh key is too old, \nplease \
clear it in file ../.ssh/known_hosts\n\
or may be any else error...\n"
    
#function for get lldp neighbors 
def get_lldp_nbrs():
    print "Getting lldp neighbors..."
    lldp_nbrs = ssh.sendline('di lldp nei br')
    ssh.expect('<')
    display_lldp = ssh.before#.decode('utf-8')
    return display_lldp.split('\n')

def generate_cfg(lst):
   print "Generating the config file..."
   cfg_desc = []
   for line in lst:
       if len(line.split()) > 0 and '/' in line.split()[0]:
	   if 'GE' in line.split()[0]:
 	       cfg_desc.append('interface Gi' + line.split()[0][2:])
           else:
               cfg_desc.append('interface ' + line.split()[0])
           cfg_desc.append('desc T_00D000000_' + line.split()[1] + '_' + line.split()[2])
           cfg_desc.append('quit')
   print cfg_desc
   return cfg_desc


def cfg_write(lst):
    do_it = raw_input("\nWrite the configuration?(y/n):")
    if do_it in ['y', 'yes']:
        print "Writting the configuration..."
        ssh.sendline('sys')
        ssh.expect(']')
        for command in lst:
            ssh.sendline(command)
            ssh.expect(']')
        ssh.sendline('return')
        ssh.expect('>')
        ssh.sendline('save')
        ssh.expect('N]')
        ssh.sendline('y')
        ssh.expect('>')
    else:
        print "Skipping write..."
        pass
    ssh.close()

if __name__ == "__main__":
    devices = open('ip.txt').read().split()
    global login
    global password
    login = raw_input('login: ')
    password = getpass.getpass(prompt='password: ')
    for ip in devices:
        if connect_to_device(ip):
            cfg_write(generate_cfg(get_lldp_nbrs()))



