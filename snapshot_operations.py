#!/usr/bin/env python
"""
Written by Hugo Andrés Vázquez
Github: https://github.kyndryl.net/hvazquez
Email: Hugo.Andres.Vazquez@kyndryl.com

Based on Vmware SDK
"""

import sys
from tools import cli, pchelper, service_instance
from pyVmomi import vim
from pyVim.task import WaitForTask

def get_snapshots_by_name_recursively(snapshots, snapname):
    snapitem = []
    for snapshot in snapshots:
        if snapshot.name == snapname:
            snapitem.append(snapshot)
        else:
            snapitem = snapitem + get_snapshots_by_name_recursively(
                                    snapshot.childSnapshotList, snapname)
    return snapitem


def get_current_snapitem(snapshots, snapob):
    snapitem = []
    for snapshot in snapshots:
        if snapshot.snapshot == snapob:
            snapitem.append(snapshot)
        snapitem = snapitem + get_current_snapitem(
                                snapshot.childSnapshotList, snapob)
    return snapitem

def list_snapshots_recursively(snapshots):
    snapshot_data = []
    for snapshot in snapshots:
        snap_text = "Nombre: %s; Description: %s; CreateTime: %s; State: %s" % (
                                        snapshot.name, snapshot.description,
                                        snapshot.createTime, snapshot.state)
        snapshot_data.append(snap_text)
        snapshot_data = snapshot_data + list_snapshots_recursively(
                                        snapshot.childSnapshotList)
    return snapshot_data


def main():

    print("Connecting to ESX/vCenter.....")
    parser = cli.Parser()
    parser.add_optional_arguments(
        cli.Argument.VM_NAME, cli.Argument.SNAPSHOT_OPERATION, cli.Argument.SNAPSHOT_NAME)
    args = parser.get_args()
    si = service_instance.connect(args)

    print("Connected to ESX/vCenter!")

    content = si.RetrieveContent()

    vm = pchelper.get_obj(content, [vim.VirtualMachine], args.vm_name)

    if args.snapshot_operation != 'create' and vm.snapshot is None:
        print("VM %s doesn't have a snapshot" % vm.name)
        sys.exit()

    if args.snapshot_operation == 'create':
        snapshot_name = args.snapshot_name
        description = "Test snapshot"
        dump_memory = False
        quiesce = False

        print("Creating snapshot %s for virtual machine %s" % (
                                        snapshot_name, vm.name))
        WaitForTask(vm.CreateSnapshot(
            snapshot_name, description, dump_memory, quiesce))

    elif args.snapshot_operation in ['remove', 'revert']:
        snapshot_name = args.snapshot_name
        snapitem = get_snapshots_by_name_recursively(
                            vm.snapshot.rootSnapshotList, snapshot_name)
        # if len(snapitem) is 0; then no snapshots with specified name
        if len(snapitem) == 1:
            snapitem = snapitem[0].snapshot
            if args.snapshot_operation == 'remove':
                print("Removing snapshot %s" % snapshot_name)
                WaitForTask(snapitem.RemoveSnapshot_Task(True))
            else:
                print("Reverting to snapshot %s" % snapshot_name)
                WaitForTask(snapitem.RevertToSnapshot_Task())
        else:
            print("No snapshots found with name: %s on VM: %s" % (
                                                snapshot_name, vm.name))

    elif args.snapshot_operation == 'list_all':
        print("Display list of snapshots on virtual machine %s" % vm.name)
        snapshot_paths = list_snapshots_recursively(
                            vm.snapshot.rootSnapshotList)
        for snapshot in snapshot_paths:
            print(snapshot)

    elif args.snapshot_operation == 'list_current':
        current_snapref = vm.snapshot.currentSnapshot
        current_snapitem = get_current_snapitem(
                            vm.snapshot.rootSnapshotList, current_snapref)
        current_snapshot = "Name: %s; Description: %s; " \
                           "CreateTime: %s; State: %s" % (
                                current_snapitem[0].name,
                                current_snapitem[0].description,
                                current_snapitem[0].createTime,
                                current_snapitem[0].state)
        print("Virtual machine %s current snapshot is:" % vm.name)
        print(current_snapshot)

    elif args.snapshot_operation == 'remove_all':
        print("Removing all snapshots for virtual machine %s" % vm.name)
        WaitForTask(vm.RemoveAllSnapshots())

    else:
        print("Specify operation in "
              "create/remove/revert/list_all/list_current/remove_all")


# Start program
if __name__ == "__main__":
    main()
