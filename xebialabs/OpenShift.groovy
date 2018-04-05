xld {
    scope(
            forInfrastructure: 'Infrastructure/Containers/OpenShift'
    ) {
        infrastructure('minishift.local', 'openshift.Server') {
            serverUrl = 'https://192.168.64.8:8443' //set your own value
            openshiftToken = 'gacIAMp-Ql3rXovhhSZ0t3ZZQinC6vk_HDjseHGEwMo' //oc whoami -t
            verifyCertificates = false
        }
        infrastructure('mylocalhost', 'overthere.LocalHost') {
            os = com.xebialabs.overthere.OperatingSystemFamily.UNIX
            infrastructure('smoke test runner', 'smoketest.Runner') {
                host = ref('Infrastructure/Containers/OpenShift/mylocalhost')
            }
        }
    }
}