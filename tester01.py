import psutil as pea

procCount = pea.cpu_count()   ## These three values should remain static in my use cases; 
mem = pea.virtual_memory()    ## processor and memory won't ever (!!!) be changed, and I won't likely be 
parts = pea.disk_partitions() ## hot-plugging drives on the relavent systems. 
                              ##    Still, note to self: filter out removable media/just update drives in loop? 

count = 0 

def main():
    global count
    while(count < 10):
        loop()
        count += 1
    
    
def loop():
    global procCount
    global mem
    global parts
    
    procUse = pea.cpu_percent(1, True)
    diskUse = pea.disk_usage('/') #forEach partition get use
    
    totalMem = mem.total/(1024*1024) # in MB
    freeMem = mem.free/(1024*1024)


    marq = ""
    marq += "Processor cores: {0}\n".format(procCount)
    
    for x in range(procCount):
        marq += "    Core {0}: {1}%\n".format(x, procUse[x])
    marq += "Installed RAM: {0} MB".format(totalMem)

    #print("Cores: {0}\nProcessor use: {1}\nTotal Installed RAM: {2} MB".format(procCount, procUse, totalMem))
    print(marq)

main()