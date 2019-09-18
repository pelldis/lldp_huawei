import pexpect


#Function for connecting to device
# need ip address in format 1.1.1.1 to connect
def connect_to_device(ip):
    print "Connecting to device: " + ip
    login = raw_input('login: ')
    password = raw_input('password: ')
    #login = 'admin'
    #password = 'Juniper'
    global ssh
    ssh = pexpect.spawn('ssh ' + login + '@' +ip)
    ssh.expect('\:')
    ssh.sendline(password)
    ssh.expect('>')
    
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
    if do_it == 'y':
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
    for ip in devices:
        connect_to_device(ip)
        cfg_write(generate_cfg(get_lldp_nbrs()))




