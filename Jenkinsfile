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
    git 'https://github.com/PPerminov/TMG_Logs.git'
    stage('Build Docker image') {
      container('ubuntu') {
        sh "pwd"
        sh "git merge -m '' $ghprbActualCommit"
        sh "cat Jenkinsfile"
        sh "printenv | sort -u"
      }
    }
  }
}
