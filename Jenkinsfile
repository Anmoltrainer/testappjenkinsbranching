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

        stage('Setup Python Environment') {
            steps {
                script {
                    try {
                        sh '''
                            python3 -m venv venv
                            . venv/bin/activate
                            pip3 install --upgrade pip
                            pip3 install -r requirements.txt
                        '''
                    } catch (Exception e) {
                        error "Failed to set up Python environment: ${e.message}"
                    }
                }
            }
        }

        stage('Run Flask App') {
            steps {
                script {
                    try {
                        sh '''
                            . venv/bin/activate
                            python3 github_jenkins_webhook.py &
                            echo $! > .pidfile
                        '''
                    } catch (Exception e) {
                        error "Failed to start Flask app: ${e.message}"
                    }
                }
            }
        }

        stage('Trigger Jenkins Job') {
            steps {
                script {
                    def response = httpRequest(
                        url: "${env.JENKINS_URL}/job/${env.JENKINS_JOB}/build",
                        authentication: 'jenkins-api-token',
                        httpMode: 'POST'
                    )
                    echo "Response: ${response}"
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    try {
                        sh 'curl http://localhost:5000/github-webhook/'
                    } catch (Exception e) {
                        error "Test failed: ${e.message}"
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                if (fileExists('.pidfile')) {
                    sh '''
                        kill $(cat .pidfile) || true
                        rm .pidfile
                    '''
                }
            }
            cleanWs()
        }
    }
}
