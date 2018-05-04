from openshift.api_client import APIClient
import time

client = APIClient(task.pythonScript.getProperty("host"), task.pythonScript.getProperty('ocPath'))

command="describe  bc {} | grep {}".format(task.pythonScript.getProperty('buildConfName'), task.pythonScript.getProperty('buildNumber'))
#print "command is {}".format(command)
output = client.execute_openshift_command_only(command).stdout
#print output
buildStatus = output.split('\t')[1].strip()
buildNumber = task.pythonScript.getProperty('buildNumber')
#print "BUILD STATUS is {}".format(buildStatus)
output = output.replace('\t', '').replace(' ', '')
#print output
masterUrl = client.execute_openshift_command_only("version | grep -i server").stdout.split(' ')[1].strip()


consoleURL = "{}/console/project/{}/browse/builds/{}/{}?tab=logs".format(
        masterUrl,
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
    APIClient.add_comment('{} is failed.'.format(buildNumber))
    sys.exit(2)
else:
    task.schedule("openshift/Build.wait-for-build.py")

