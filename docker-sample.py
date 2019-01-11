from pyspark import SparkContext

"""
The code in the __main__ block will be executed on a single node, the 'driver'. It describes the different steps that need
to be executed in parallel.
"""
#As we're not taking any input parameters in dockerFunc, we need to generate a dummy input
def dockerFunc(abc):
    import signal
    import docker
    #Quick example docker run that returns the hostname of the docker container (the volume is just to show that it is possible to map a volume of the underlying OS)
    #For bigger programs it's best to create a Dockerfile and build/run your docker container from that dockerfile.

    def handle_signal(signal, frame):
        print("Caught signal %d Killing executor and docker container now" % signal)
        container.kill()

    # catch all catchable signals
    #catchable_sigs = set(signal.Signals) - {signal.SIGKILL, signal.SIGSTOP}
    #for sig in catchable_sigs:
    #    signal.signal(sig, handle_signal)

    # catch signals to update PID state when job is killed
    # trapping SIGKILL and SIGSTOP is not possible
    signal.signal(signal.SIGHUP, handle_signal) # in case job is killed via Yarn
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGQUIT, handle_signal)

    client = docker.from_env()
    print('starting docker container')
    container = client.containers.run("centos", "/bin/bash -c 'hostname; sleep 600'", detach=True)
    for line in container.logs(stream=True):
        print(line.strip())
    return str(container.id)

	
if __name__ == '__main__':
#    dockerFunc(1)
    #The SparkContext is our entry point to bootstrap parallel operations.
    sc = SparkContext(appName='docker-sample')

    try:
        #As we're not actually distributing anything we create a dummy list to distribute
        programs_input = sc.parallelize(range(1,10))
        #Run the dockerFunc on all executors and collect all the outputs in programs_output
        programs_output = programs_input.map(dockerFunc).collect()
        result = "".join(map(str,programs_output))
        print("The result is: " + result)
    finally:
        sc.stop()

