from openshift.api_client import APIClient
import time

client = APIClient(task.pythonScript.getProperty("client"))

buildNumber = task.pythonScript.getProperty('buildNumber')
command="describe buildconfig {}".format(task.pythonScript.getProperty('buildConfName'))
print "command is {}".format(command)
output = client.execute_openshift_command_only(command)
stdout = output.stdout
stderr = output.stderr
#print "------"
#print "BM stdout", stdout
#print "BM stderr", stderr
#print "---"


for line in stdout.split('\n'):
    if line.startswith(buildNumber):
        buildStatus = line.split('\t')[1].strip()
        break


print "BUILD STATUS is {}".format(buildStatus)
consoleURL = "{}/console/project/{}/browse/builds/{}/{}?tab=logs".format(
        task.pythonScript.getProperty("client").getProperty('serverUrl'),
        task.pythonScript.getProperty('project'),
        task.pythonScript.getProperty('buildConfName'),
        task.pythonScript.getProperty('buildNumber'))
print("Running {}: {} - view [Console Output]({})".format(buildNumber, buildStatus, consoleURL))
task.setStatusLine("Running {}: {} ".format(buildNumber, buildStatus))


if 'complete' == buildStatus:
    APIClient.add_comment('{} is completed successfully.'.format(buildNumber))
    sys.exit(0)
if 'failed' == buildStatus:
    APIClient.add_comment('{} is failed.'.format(buildNumber))
    sys.exit(1)
if 'cancelled' == buildStatus:
    APIClient.add_comment('{} is cancelled.'.format(buildNumber))
    sys.exit(2)
else:
    task.schedule("openshift/Build.wait-for-build.py")

