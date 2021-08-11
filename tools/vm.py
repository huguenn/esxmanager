__author__ = "VMware, Inc."


def print_vm_info(vm, depth=1, max_depth=10):
    """
    Print information for a particular virtual machine or recurse into a
    folder with depth protection
    """

    # if this is a group it will have children. if it does, recurse into them
    # and then return
    if hasattr(vm, 'childEntity'):
        if depth > max_depth:
            return
        vm_list = vm.childEntity
        for child_vm in vm_list:
            print_vm_info(child_vm, depth + 1)
        return

    summary = vm.summary
    print("Name       :", summary.config.name)
    print("Path       :", summary.config.vmPathName)
    print("Guest      :", summary.config.guestFullName)
    annotation = summary.config.annotation
    if annotation:
        print("Annotation :", annotation)
    print("State      :", summary.runtime.powerState)
    if summary.guest is not None:
        ip = summary.guest.ipAddress
        if ip:
            print("IP         :", ip)
    if summary.runtime.question is not None:
        print("Question  :", summary.runtime.question.text)
    print("")
