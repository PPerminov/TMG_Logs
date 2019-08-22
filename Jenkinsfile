/**
 * This pipeline will run a Docker image build
 */

podTemplate(yaml: """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: ubuntu
    image: ubuntu
    tty: true

  - name: docker
    image: docker:1.11
    command: ['cat']
    tty: true
    volumeMounts:
    - name: dockersock
      mountPath: /var/run/docker.sock
  volumes:
  - name: dockersock
    hostPath:
      path: /var/run/docker.sock
"""
  ) {

  def image = "jenkins/jnlp-slave"
  node(POD_LABEL) {
    
    stage('ENV') {
      checkout([$class: 'GitSCM', branches: [[name: '${sha1}']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[credentialsId: '32d4da0a-2aba-4cd2-874e-bf9ddffbc17a', name: 'origin', refspec: '+refs/pull/${ghprbPullId}/*:refs/remotes/origin/pr/${ghprbPullId}/*', url: 'https://github.com/PPerminov/TMG_Logs.git']]])
    }
    stage('Build Docker image') {
      container('ubuntu') {
        sh "pwd"
        sh "cat Jenkinsfile"
        sh "printenv | sort -u"
      }
    }
  }
}
