#
# Copyright (c) 2018. All rights reserved.
#
# This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries, and licensors.
#

import sys
import urllib2
import base64
import random
import com.xebialabs.xlrelease.plugin.openshift.RemoteScript as RemoteScript
import com.xebialabs.xlrelease.script.EncryptionHelper as EncryptionHelper

class APIClient:

    def __init__(self, oc_client_config):
        self.temp_config_file = '/tmp/oc_config/xlr-oc-{0}.conf'.format(random.randint(1, 65536*1024))
        EncryptionHelper.decrypt(oc_client_config.getProperty('clientHost'))
        self.remote = RemoteScript(oc_client_config.getProperty('clientHost'))
        self.oc_path = oc_client_config.getProperty('ocPath')
        self.login(oc_client_config.getProperty('serverUrl'), oc_client_config.getProperty('username'),
                   oc_client_config.getProperty('password'), oc_client_config.getProperty('project'),
                   oc_client_config.getProperty('skipSSL'))

    def login(self, server_url, username, password, project=None, skip_ssl=False):
        command = '{} {} {}'.format(self.oc_path, 'login', server_url)
        command = ' {} -u {}'.format(command, username)
        command = ' {} -p {}'.format(command, password)
        if project:
            command = ' {} -n {}'.format(command, project)
        if skip_ssl:
            command = ' {} --insecure-skip-tls-verify'.format(command)
        response = self.remote.executeScript(self.prepare_command(command))
        APIClient.print_logs(response)
        self.remote.cleanOutputHandlers()

    def logout(self):
        self.remote.cleanOutputHandlers()
        response = self.remote.executeScript('{} && rm {}'.format(self.prepare_command('{} {}'.format(self.oc_path, 'logout')), self.temp_config_file))
        APIClient.print_logs(response)

    def execute_openshift_spec(self, spec, command ,cmd_params = None):
        response = self.remote.executeOpenshiftSpec(spec, '{} {} -f'.format(self.prepare_command('{} {}'.format(self.oc_path, command)), cmd_params if cmd_params else ''))
        APIClient.print_logs(response)
        return response

    def execute_openshift_command (self, command ,cmd_params = None, process_exit = True):
        response = self.remote.executeScript(self.prepare_command('{} {} {}'.format(self.oc_path, command, cmd_params if cmd_params else '')))
        APIClient.print_logs(response, process_exit)
        return response

    def execute_openshift_command_only (self, command ,cmd_params = None):
        response = self.remote.executeScript(self.prepare_command('{} {} {}'.format(self.oc_path, command, cmd_params if cmd_params else '')))
        return response

    def execute_command(self,command):
        response = self.remote.executeScript(self.prepare_command(command))
        APIClient.print_logs(response)
        return response

    def prepare_command(self, base_command):
        return '{} --config {} '.format(base_command, self.temp_config_file)

    @staticmethod
    def download_file(url, username, password):
        request=urllib2.Request(url)
        if (username is not None) and (password is not None):
            base64string = base64.encodestring('{}:{}'.format(username, password))[:-1]
            auth_header =  "Basic {}".format(base64string)
            request.add_header("Authorization", auth_header)

        return urllib2.urlopen(request).read()

    @staticmethod
    def add_comment(comment):
        print "```"
        print comment
        print "```"

    @staticmethod
    def print_logs(response, process_exit = True):
        output = response.stdout
        error = response.stderr
        if response.rc == 0:
            print "```"
            print output
            print "```"
        else:
            print "Exit code: "
            print response.rc
            print
            print "#### Output:"
            print "```"
            print output
            print "```"

            print "----"
            print "#### Error stream:"
            print "```"
            print error
            print "```"
            print

            if process_exit:
                sys.exit(response.rc)
