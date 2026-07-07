pipeline {
    agent any
    stages {
        stage('Get Code') {
            steps {
                git branch: 'master',
                    url: 'https://github.com/bryvid09/todo-list-aws.git'
                sh 'ls -la'
            }
        }
        
        stage('Deploy') {
            steps {
                sh '''
                    sam build
                    sam validate --region us-east-1
                    sam deploy --config-env production --no-confirm-changeset --no-fail-on-empty-changeset
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
                    echo "URL de aws es: $BASE_URL"
                    pytest -s -v -m readonly test/integration/todoApiTest.py --junitxml=result-rest.xml
                '''
                junit 'result-rest.xml'
            }
        }
        
    }
}