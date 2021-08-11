#!/usr/bin/env python
"""
Written by Hugo Andrés Vázquez
Github: https://github.kyndryl.net/hvazquez
Email: Hugo.Andres.Vazquez@kyndryl.com

List all Vms at targeted host by name
Based on Vmware SDK
"""
from tools import cli, service_instance

MAX_DEPTH = 10


def print_vminfo(vm, depth=1):
    """
    Print information for a particular virtual machine or recurse into a folder
    with depth protection
    """

    # if this is a group it will have children. if it does, recurse into them
    # and then return
    if hasattr(vm, 'childEntity'):
        if depth > MAX_DEPTH:
            return
        vmlist = vm.childEntity
        for child in vmlist:
            print_vminfo(child, depth+1)
        return

    summary = vm.summary
    print(summary.config.name)


def main():
    """
    Simple command-line program for listing the virtual machines on a host.
    """

    parser = cli.Parser()
    args = parser.get_args()
    si = service_instance.connect(args)

    content = si.RetrieveContent()
    for child in content.rootFolder.childEntity:
        if hasattr(child, 'vmFolder'):
            datacenter = child
            vmfolder = datacenter.vmFolder
            vmlist = vmfolder.childEntity
            for vm in vmlist:
                print_vminfo(vm)


# Start program
if __name__ == "__main__":
    main()
