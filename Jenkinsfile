pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
       
                checkout([$class: 'GitSCM', branches: [[name: '*/main']], userRemoteConfigs: [[url: 'https://github.com/mspr2Epsi/message_broker.git']]])
                

            }
        }
        stage('Verify Python Installation') {
            steps {
  
                bat 'python --version'
            }
        }
        stage('Setup Python Environment') {
            steps {
                bat 'python -m venv venv'
                bat 'venv\\Scripts\\activate && pip install -r requirements.txt'
            }
        }
        stage('Check compilation') {
            steps {

                bat 'venv\\Scripts\\activate && python -m py_compile message_broker.py'
            }
        }
    }
}
