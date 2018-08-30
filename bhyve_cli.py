import libvirt 
import sys


#conn = libvirt.openReadOnly("bhyve:///system")
conn = libvirt.openReadOnly("bhyve+tcp://127.0.0.1:16509/system")

if conn == None:
    print("Failed to open connection to hypervisor")
    sys.exit(1)

try:
    print("All domains: ", conn.listAllDomains())
    print("Defined domains: ", conn.listDefinedDomains())

    #dom0 = conn.lookupByName("bhyve")

    host = conn.getHostname()
    print('Hostname:'+host)

    vcpus = conn.getMaxVcpus(None)
    print('Maximum support virtual CPUs: '+str(vcpus))

    nodeinfo = conn.getInfo()

    print('Model: '+str(nodeinfo[0]))
    print('Memory size: '+str(nodeinfo[1])+'MB')
    print('Number of CPUs: '+str(nodeinfo[2]))
    print('MHz of CPUs: '+str(nodeinfo[3]))
    print('Number of NUMA nodes: '+str(nodeinfo[4]))
    print('Number of CPU sockets: '+str(nodeinfo[5]))
    print('Number of CPU cores per socket: '+str(nodeinfo[6]))
    print('Number of CPU threads per core: '+str(nodeinfo[7]))
    
    print('Virtualization type: '+conn.getType())
    ver = conn.getVersion()
    print('Version: '+str(ver))

    ver = conn.getLibVersion();
    print('Libvirt Version: '+str(ver));

    uri = conn.getURI()
    print('Canonical URI: '+uri)

    print('Connection is encrypted: '+str(conn.isEncrypted()))
    alive = conn.isAlive()

    
    print("Connection is alive = " + str(alive))

    xml = '<cpu mode="custom" match="exact">' + \
        '<model fallback="forbid">kvm64</model>' + \
      '</cpu>'

    retc = conn.compareCPU(xml)

    if retc == libvirt.VIR_CPU_COMPARE_ERROR:
        print("CPUs are not the same or ther was error.")
    elif retc == libvirt.VIR_CPU_COMPARE_INCOMPATIBLE:
        print("CPUs are incompatible.")
    elif retc == libvirt.VIR_CPU_COMPARE_IDENTICAL:
        print("CPUs are identical.")
    elif retc == libvirt.VIR_CPU_COMPARE_SUPERSET:
        print("The host CPU is better than the one specified.")
    else:
        print("An Unknown return code was emitted.")


    mem = conn.getFreeMemory()

    print("Free memory on the node (host) is " + str(mem) + " bytes.")

    domainIDs = conn.listDomainsID()
    print("Domain ids: ", domainIDs)

    map = conn.getCPUMap()

    print("CPUs: " + str(map[0]))
    print("Available: " + str(map[1]))


    nodeinfo = conn.getInfo()
    numnodes = nodeinfo[4]

    memlist = conn.getCellsFreeMemory(0, numnodes)
    cell = 0
    for cellfreemem in memlist:
        print('Node '+str(cell)+': '+str(cellfreemem)+' bytes free memory')
        cell += 1



    conn.close()
    exit(0)


except:
    print("Error to fetch the domains")
    sys.exit(1)

