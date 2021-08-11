Scripts to perform tasks on ESX server

Usage:

create_vm.py -s HOST [-o PORT] -u USER [-p PASSWORD] [-nossl] [-v VM_NAME] [--datacenter-name DATACENTER_NAME] [--datastore-name DATASTORE_NAME] [--esx-ip ESX_IP]

get_vm_names.py -s HOST [-o PORT] -u USER [-p PASSWORD] [-nossl]

getallvms.py -s HOST [-o PORT] -u USER [-p PASSWORD] [-nossl] [-f FIND]

snapshot_operations.py -s HOST [-o PORT] -u USER [-p PASSWORD] [-nossl] [-v VM_NAME] [-op {create,remove,revert,list_all,list_current,remove_all}]

vm_power_on.py -s HOST [-o PORT] -u USER [-p PASSWORD] [-nossl] -v VM_NAME