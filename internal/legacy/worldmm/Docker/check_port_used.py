#!/usr/bin/python3.6
import os
import subprocess
def get_ports():
    result = []
    _tmp1 = subprocess.check_output("docker ps -a --format {{.Ports}} | grep '/tcp'", shell=True)
    if type(_tmp1) == bytes:
        _tmp2 = _tmp1.decode('utf-8').split(' ')
    elif type(_tmp1) == str:
        _tmp2 = _tmp1.split(' ')
    for _t in _tmp2:
        result += _t.split('\n')
    return result
def normalize(data):
    result = []
    errors = []
    for line in data:
        line_ports = line.replace('\n', '').replace(',', '').split(' ')
        for continuous_ports in line_ports:
            _tmp = continuous_ports.split('/')[0]
            if '->' in _tmp:
                _tmp = _tmp.split('->')[-1]
                if '-' in _tmp:
                    _tmp = _tmp.split('-')
                    _from, _to = int(_tmp[0]), int(_tmp[1])
                    result += list(range(_from, _to+1))
                else:
                    result.append(int(_tmp))
            else:
                errors.append(continuous_ports)
    return sorted(result), errors
def check_ports(used_ports):
    errors = []
    resource = list(range(8801, 8900))
    for port in used_ports:
        if port in resource:
            resource.remove(port)
        else:
            errors.append(port)
    return resource, errors
def main():
    ports = get_ports()
    used_ports, err1 = normalize(ports)
    unused_ports, err2 = check_ports(used_ports)
    err = err1 + err2
    print('\nAbnormal or Duplicate Ports: {}\n\t{}'.format(len(err), err))
    print('\nUsing ports: {}\n\t{}'.format(len(used_ports), used_ports))
    print('\nUnused ports: {}\n\t{}\n'.format(len(unused_ports), unused_ports))
if __name__=='__main__':
    main()
