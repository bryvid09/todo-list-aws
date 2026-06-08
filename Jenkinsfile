pipeline {
    agent any

    stages {
        stage('Get Code') {
      steps {
        checkout scm
        sh 'ls -la'
        sh 'pwd'
      }
        }
    }
}
