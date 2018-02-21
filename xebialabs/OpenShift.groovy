xld {
  scope(
    forInfrastructure: 'Infrastructure/Containers/OpenShift'
  ) {
    infrastructure('minishift.local', 'openshift.Server') {
      serverUrl = 'https://192.168.64.6:8443' //set your own value
      openshiftToken = '' //Encrypted value removed for export
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