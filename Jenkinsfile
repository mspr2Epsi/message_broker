pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: '*/main']], userRemoteConfigs: [[url: 'https://github.com/mspr2Epsi/message_broker.git']]])
            }
        }
        stage('Run Tests') {
            steps {

                bat 'python --version'


                bat 'venv\\Scripts\\activate.bat'


                bat 'pip install -r requirements.txt'

                bat 'python -m py_compile  message_broker.py'
            }
        }
    }
}
