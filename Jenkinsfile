pipeline {
    agent any
    stages {
        stage('Get Code') {
            steps {
                git branch: 'develop',
                    url: 'https://github.com/bryvid09/todo-list-aws.git'
                sh 'ls -la'
            }
        }

        stage('Static Test') {
            steps {
                sh '''
                    flake8 --exit-zero --format=pylint src > flake8.out
                    bandit --exit-zero -r src -f custom -o bandit.out \
                      --msg-template "{abspath}:{line}: [{test_id}] {msg}"
                '''
                recordIssues tools: [
                    flake8(name: 'Flake8', pattern: 'flake8.out'),
                    pyLint(name: 'Bandit', pattern: 'bandit.out')
                ]
            }
        }
        
        stage('Deploy') {
            steps {
                sh '''
                    sam build
                    sam validate --region us-east-1
                    sam deploy --config-env staging --no-confirm-changeset --no-fail-on-empty-changeset
                '''
            }
        }
        
        stage('Rest Test') {
            steps {
                sh '''
                    export BASE_URL=$(aws cloudformation describe-stacks \
                      --stack-name todo-list-aws-staging \
                      --query "Stacks[0].Outputs[?OutputKey=='BaseUrlApi'].OutputValue" \
                      --output text --region us-east-1)
                    echo "Probando API en: $BASE_URL"
                    pytest test/integration/todoApiTest.py --junitxml=result-rest.xml
                '''
                junit 'result-rest.xml'
            }
        }
        
        stage('Promote') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'github-token',
                    usernameVariable: 'GIT_USER', passwordVariable: 'GIT_TOKEN')]) {
                    sh '''
                        git checkout -B master origin/master
                        git merge origin/develop -m "Stage promote OK"
                        git push https://$GIT_USER:$GIT_TOKEN@github.com/bryvid09/todo-list-aws.git master
                    '''
                }
            }
        }
    }
}