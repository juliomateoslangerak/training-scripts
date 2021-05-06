import subprocess, os

# my_env = os.environ.copy()
# my_env["OMERODIR"] = "/opt/OMERO.server-5.6.3-ice36-b228"

my_env = {"OMERODIR": "/opt/OMERO.server-5.6.3-ice36-b228"}


# def subprocess_cmd(command):
#     process = subprocess.run(command, stdout=subprocess.PIPE, shell=True, env=my_env)
#     proc_stdout = process.communicate()[0].strip()
#     print(proc_stdout)


cmd = ['echo', '$OMERODIR']
    #; omero login -u root -w ChangeMe -s 192.168.56.107 ; omero download Image:51 test1"

try:
    process = subprocess.run(cmd, stdout=subprocess.PIPE, env=my_env)
except subprocess.CalledProcessError as e:
    print(f'Error: {e.output}')
    print(f'Command: {e.cmd}')

print(process.stdout)


# cmd = "omero download Image:51 test2"
#
#
# subprocess_cmd(cmd)

