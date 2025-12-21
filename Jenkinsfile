
pipeline {
    agent any
    
    environment {
        DOCKERHUB_CREDENTIALS = credentials('docker_hub')
        DOCKERHUB_USERNAME = 'sia21'
        FRONTEND_IMAGE = "${DOCKERHUB_USERNAME}/react-frontend"
        BACKEND_IMAGE = "${DOCKERHUB_USERNAME}/flask-backend"
        MONGODB_IMAGE = "mongo:4.4"
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Cloning repository from GitHub...'
                git branch: 'main', url: 'https://github.com/Assia-Elguerch/react-flask-mongodb-app.git'
            }
        }
        
        stage('Build Images') {
            steps {
                echo 'Building Docker images...'
                script {
                    // Build frontend
                    sh 'docker build -t ${FRONTEND_IMAGE}:latest ./frontend'
                    
                    // Build backend
                    sh 'docker build -t ${BACKEND_IMAGE}:latest ./backend'
                }
            }
        }
        
        stage('Test & Run Locally') {
            steps {
                echo 'Running application locally...'
                script {
                    // Stop existing containers
                    sh 'docker-compose down || true'
                    
                    // Start application
                    sh 'docker-compose up -d'
                    
                    // Wait for services to be ready
                    sh 'sleep 20'
                    
                    // Test API
                    sh 'docker-compose exec -T api curl -f http://localhost:5000/api/tasks || exit 1'
                    
                    echo 'Application is running successfully!'
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                echo 'Logging into Docker Hub...'
                script {
                    sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
                    
                    echo 'Pushing images to Docker Hub...'
                    sh 'docker push ${FRONTEND_IMAGE}:latest'
                    sh 'docker push ${BACKEND_IMAGE}:latest'
                    
                    echo 'Images pushed successfully!'
                }
            }
        }
        
        stage('Cleanup') {
            steps {
                echo 'Cleaning up...'
                sh 'docker logout'
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline completed successfully! ✅'
            echo "Frontend image: ${FRONTEND_IMAGE}:latest"
            echo "Backend image: ${BACKEND_IMAGE}:latest"
        }
        failure {
            echo 'Pipeline failed! ❌'
        }
        always {
            echo 'Pipline Finished.'
        }
    }
}
    
