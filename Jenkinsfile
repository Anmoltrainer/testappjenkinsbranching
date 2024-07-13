pipeline {
    agent any

    environment {
        JENKINS_URL = credentials('jenkins-url')
        JENKINS_JOB = credentials('jenkins-job-name')
        JENKINS_USER = credentials('jenkins-user')
        JENKINS_API_TOKEN = credentials('jenkins-api-token')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate'
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Flask App') {
            steps {
                sh 'python3 app/github_jenkins_webhook.py &'
            }
        }

        stage('Test') {
            steps {
                sh 'curl http://localhost:5000/github-webhook/'
            }
        }
    }

    post {
        always {
            sh 'pkill -f github_jenkins_webhook.py'
        }
    }
}
