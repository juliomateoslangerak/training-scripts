import subprocess


cmd = 'omero download -k 74055b41-16bb-4f2e-aa0f-f19cd8d28f3f -s 192.168.56.107 Image:51 test1'

try:
    process = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
except subprocess.CalledProcessError as e:
    print(f'Error: {e.output}')
    print(f'Command: {e.cmd}')

print('done')

cmd = 'omero download -k 74055b41-16bb-4f2e-aa0f-f19cd8d28f3f -s 192.168.56.107 Image:51 test2'

try:
    process = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
except subprocess.CalledProcessError as e:
    print(f'Error: {e.output}')
    print(f'Command: {e.cmd}')


print(process.stdout)


# cmd = "omero download Image:51 test2"
#
#
# subprocess_cmd(cmd)

