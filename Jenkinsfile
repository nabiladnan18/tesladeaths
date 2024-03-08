pipeline {
    agent any

    environment {
        DOCKERHUB_USERNAME = credentials('DOCKERHUB_USERNAME')
        DOCKERHUB_PASSWORD = credentials('DOCKERHUB_PASSWORD')
        AWS_CREDENTIALS = credentials('AWS_SSH_CREDENTIALS')
    }
    
    stages {
        stage('Login to Registry') {
            sh'docker login -u $DOCKERHUB_USERNAME -p $DOCKERHUB_PASSWORD'
        }
        
        stage('Build and push image') {
            sh'docker build -t $DOCKERHUB_USERNAME/tesla_deaths_app:latest .'
            sh'docker push $DOCKERHUB_USERNAME/tesla_deaths_app:latest'
        }
    }
}
