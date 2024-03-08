pipeline {
    agent any

    environment {
        DOCKERHUB_USERNAME = credentials('DOCKERHUB_USERNAME')
        DOCKERHUB_PASSWORD = credentials('DOCKERHUB_PASSWORD')
        AWS_CREDENTIALS = credentials('AWS_SSH_CREDENTIALS')
        // EC2 = credentials('EC2_INSTANCE')
    }
    
    stages {
        // stage('Checkout') {
        //     steps {
        //         checkout scm
        //     }
        // }
        
        stage('Install dependencies') {
            steps {
                
            }
        }
        
        stage('Login to Registry') {
            steps {
                sh'docker login -u $DOCKERHUB_USERNAME -p $DOCKERHUB_PASSWORD'
            }
        }
        
        stage('Build and push image') {
            steps {
                sh'docker build -t $DOCKERHUB_USERNAME/tesla_deaths_app:latest .'
                sh'docker push $DOCKERHUB_USERNAME/tesla_deaths_app:latest'
            }
        }
    }
}
