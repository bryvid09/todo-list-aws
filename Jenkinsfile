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

      stage('Static Test') {
        steps {
            sh '''
                . /var/lib/jenkins/ci-tools/bin/activate
                flake8 --format=pylint --exit-zero --output-file=flake8.out src/
                bandit --exit-zero -r src/ -f html -o bandit.out
            '''
            archiveArtifacts artifacts: 'flake8.out, bandit.out', allowEmptyArchive: false
        }
      }
    }
}
