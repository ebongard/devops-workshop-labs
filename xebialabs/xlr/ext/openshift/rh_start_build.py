from openshift.api_client import APIClient
import time

client = APIClient(task.pythonScript.getProperty("client"))
#print "set the project {}".format(task.pythonScript.getProperty('project'))
#print client.execute_openshift_command_only(command="{} {}".format("project",task.pythonScript.getProperty('project'))).stdout

print "execute build {}".format(task.pythonScript.getProperty('buildConfName'))

execb = client.execute_openshift_command_only(
    command="{} {}".format(task.pythonScript.getProperty('command'), task.pythonScript.getProperty('buildConfName')),
    cmd_params=task.pythonScript.getProperty('cmdParams'))

#print "--------------------------------------"
#print execb
#print execb.stdout
#print execb.stderr
#print "--------------------------------------"

output = execb.stdout
buildNumber = None
for line in output.split('\n'):
    print('-{}'.format(line))
    if line.startswith('build') and line.endswith('started'):
        buildNumber = line.split('"')[1]

print "build_number {}".format(buildNumber)
task.setStatusLine("Running build : {} ".format(buildNumber))
task.schedule("openshift/Build.wait-for-build.py")


