from pyspark import SparkContext

"""
Quick example docker run that returns the hostname of the docker container
For bigger programs it's best to create a Dockerfile and build/run your docker container from that dockerfile.
Make sure to always use the signal handler as otherwise docker containers will keep running when the application is killed or preempted by yarn.
"""
def dockerFunc(f):
    import signal
    import docker

    # Do not put any output to stderr/stdout here as this will crash the handler (so no print statements)
    def handle_signal(signal, frame):
        container.kill()

    # catch signals to update PID state when job is killed
    # trapping SIGKILL and SIGSTOP is not possible
    signal.signal(signal.SIGHUP, handle_signal) # in case job is killed via Yarn
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGQUIT, handle_signal)

    client = docker.from_env()
    # Detach the container as it will be running in the background.
    container = client.containers.run("centos:7", "/bin/bash -c 'hostname; echo " + str(f) + "; sleep 5;'", detach=True)
    # This will attach to the docker log output and will log this in the Spark executor logs
    for line in container.logs(stream=True):
        print(line.strip())


if __name__ == '__main__':
    sc = SparkContext(appName='docker-sample')
    try:
        # As this is just an example there's no input to distribute, so we just parallelize over a range
        sc.parallelize(range(1,5)).foreach(lambda f : dockerFunc(f))
    finally:
        sc.stop()

