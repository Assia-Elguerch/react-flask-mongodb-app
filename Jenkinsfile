pipeline {
    agent any
    
    environment {
        // Configuration Vault
        VAULT_ADDR = 'http://192.168.11.127:8200'
        VAULT_TOKEN = credentials('vault-token')  // Token stocké dans Jenkins Credentials
        
        // Configuration Docker Hub (sera récupéré depuis Vault)
        DOCKERHUB_USERNAME = 'sia21'
        FRONTEND_IMAGE = "${DOCKERHUB_USERNAME}/react-frontend"
        BACKEND_IMAGE = "${DOCKERHUB_USERNAME}/flask-backend"
        MONGODB_IMAGE = "mongo:4.4"
    }
    
    stages {
        
        // ==========================================
        // STAGE 1: Installer Vault CLI
        // ==========================================
        stage('Setup Vault CLI') {
            steps {
                echo 'Installation de Vault CLI...'
                script {
                    sh '''
                        # Vérifier si vault est déjà installé
                        if ! command -v vault &> /dev/null; then
                            echo "Téléchargement de Vault CLI..."
                            wget -q https://releases.hashicorp.com/vault/1.15.0/vault_1.15.0_linux_amd64.zip
                            unzip -q vault_1.15.0_linux_amd64.zip
                            sudo mv vault /usr/local/bin/
                            rm vault_1.15.0_linux_amd64.zip
                            echo "Vault CLI installé"
                        else
                            echo "Vault CLI déjà installé"
                        fi
                        
                        # Vérifier la version
                        vault version
                    '''
                }
            }
        }
        
        // ==========================================
        // STAGE 2: Récupérer les secrets depuis Vault
        // ==========================================
        stage('Get Secrets from Vault') {
            steps {
                echo 'Récupération des secrets depuis Vault...'
                script {
                    sh '''
                        # Configuration Vault
                        export VAULT_ADDR=${VAULT_ADDR}
                        export VAULT_TOKEN=${VAULT_TOKEN}
                        
                        echo "Vérification de la connexion à Vault..."
                        vault status
                        
                        echo "Récupération des credentials Docker Hub..."
                        DOCKERHUB_USER=$(vault kv get -field=username secret/dockerhub)
                        DOCKERHUB_TOKEN=$(vault kv get -field=access_token secret/dockerhub)
                        
                        echo "Récupération des credentials MongoDB..."
                        MONGODB_USER=$(vault kv get -field=username secret/mongodb)
                        MONGODB_PASS=$(vault kv get -field=password secret/mongodb)
                        MONGODB_DB=$(vault kv get -field=database secret/mongodb)
                        
                        # Stocker dans un fichier .env pour les prochains stages
                        echo "DOCKERHUB_USER=${DOCKERHUB_USER}" > .env
                        echo "DOCKERHUB_TOKEN=${DOCKERHUB_TOKEN}" >> .env
                        echo "MONGODB_USER=${MONGODB_USER}" >> .env
                        echo "MONGODB_PASS=${MONGODB_PASS}" >> .env
                        echo "MONGODB_DB=${MONGODB_DB}" >> .env
                        
                        echo "Secrets récupérés depuis Vault avec succès"
                        echo "Docker Hub User: ${DOCKERHUB_USER}"
                        echo "MongoDB Database: ${MONGODB_DB}"
                    '''
                }
            }
        }
        
        // ==========================================
        // STAGE 3: Checkout du code depuis GitHub
        // ==========================================
        stage('Checkout') {
            steps {
                echo 'Cloning repository from GitHub...'
                git branch: 'main', url: 'https://github.com/Assia-Elguerch/react-flask-mongodb-app.git'
            }
        }
        
        // ==========================================
        // STAGE 4: Build des images Docker
        // ==========================================
        stage('Build Images') {
            steps {
                echo 'Building Docker images...'
                script {
                    sh '''
                        echo "Building Frontend image..."
                        docker build -t ${FRONTEND_IMAGE}:latest ./frontend
                        
                        echo "Building Backend image..."
                        docker build -t ${BACKEND_IMAGE}:latest ./backend
                        
                        echo "Images built successfully"
                        docker images | grep ${DOCKERHUB_USERNAME}
                    '''
                }
            }
        }
        
        // ==========================================
        // STAGE 5: Test & Run avec Vault
        // ==========================================
        stage('Test & Run Locally') {
            steps {
                echo 'Running application locally with Vault...'
                script {
                    sh '''
                        echo "Stopping existing containers..."
                        docker-compose down || true
                        
                        echo "Starting services with Vault configuration..."
                        docker-compose up -d
                        
                        echo "Waiting for services to be ready..."
                        sleep 20
                        
                        echo "Checking Vault connection in API..."
                        curl -f http://192.168.11.127:5000/api/health || exit 1
                        
                        echo "Testing API endpoints..."
                        curl -f http://192.168.11.127:5000/api/tasks || exit 1
                        
                        echo "Application is running successfully with Vault"
                        
                        # Afficher les logs de l'API pour voir Vault en action
                        echo "API Logs (Vault connection):"
                        docker-compose logs api | grep -i vault | tail -10
                    '''
                }
            }
        }
        
        // ==========================================
        // STAGE 6: Push vers Docker Hub avec Token
        // ==========================================
        stage('Push to Docker Hub') {
            steps {
                echo 'Pushing images to Docker Hub using Vault credentials...'
                script {
                    sh '''
                        # Charger les credentials depuis .env
                        source .env
                        
                        echo "Logging into Docker Hub with token from Vault..."
                        echo ${DOCKERHUB_TOKEN} | docker login -u ${DOCKERHUB_USER} --password-stdin
                        
                        echo "Pushing Frontend image..."
                        docker push ${FRONTEND_IMAGE}:latest
                        
                        echo "Pushing Backend image..."
                        docker push ${BACKEND_IMAGE}:latest
                        
                        echo "Images pushed successfully to Docker Hub"
                        echo "${FRONTEND_IMAGE}:latest"
                        echo "${BACKEND_IMAGE}:latest"
                    '''
                }
            }
        }
        
        // ==========================================
        // STAGE 7: Tag des images avec version
        // ==========================================
        stage('Tag Images') {
            steps {
                echo 'Tagging images with build number...'
                script {
                    sh '''
                        # Tag avec le numéro de build Jenkins
                        docker tag ${FRONTEND_IMAGE}:latest ${FRONTEND_IMAGE}:build-${BUILD_NUMBER}
                        docker tag ${BACKEND_IMAGE}:latest ${BACKEND_IMAGE}:build-${BUILD_NUMBER}
                        
                        # Push les versions taggées
                        source .env
                        docker push ${FRONTEND_IMAGE}:build-${BUILD_NUMBER}
                        docker push ${BACKEND_IMAGE}:build-${BUILD_NUMBER}
                        
                        echo "Images tagged and pushed with version: build-${BUILD_NUMBER}"
                    '''
                }
            }
        }
        
        // ==========================================
        // STAGE 8: Cleanup
        // ==========================================
        stage('Cleanup') {
            steps {
                echo 'Cleaning up...'
                script {
                    sh '''
                        # Logout Docker
                        docker logout
                        
                        # Supprimer le fichier .env contenant les secrets
                        rm -f .env
                        
                        # Nettoyer les images non utilisées (optionnel)
                        docker image prune -f
                        
                        echo "Cleanup completed"
                    '''
                }
            }
        }
    }
    
    // ==========================================
    // POST-BUILD ACTIONS
    // ==========================================
    post {
        success {
            script {
                echo '======================================'
                echo 'PIPELINE COMPLETED SUCCESSFULLY'
                echo '======================================'
                echo ''
                echo 'Images pushed to Docker Hub:'
                echo "Frontend: ${FRONTEND_IMAGE}:latest"
                echo "Backend: ${BACKEND_IMAGE}:latest"
                echo "Version: build-${BUILD_NUMBER}"
                echo ''
                echo 'Security:'
                echo 'All credentials managed by Vault'
                echo 'No secrets in code or logs'
                echo 'Token-based authentication'
                echo ''
                echo 'Access the application:'
                echo 'Frontend: http://192.168.11.127:3000'
                echo 'API: http://192.168.11.127:5000/api/tasks'
                echo 'Vault UI: http://192.168.11.127:8200'
                echo '======================================'
            }
        }
        
        failure {
            script {
                echo '======================================'
                echo 'PIPELINE FAILED'
                echo '======================================'
                echo ''
                echo 'Check the logs above for errors'
                echo ''
                echo 'Common issues:'
                echo '- Vault not accessible'
                echo '- Invalid Vault token'
                echo '- Docker Hub credentials not in Vault'
                echo '- Port conflicts'
                echo ''
                echo 'Run these commands to debug:'
                echo 'docker-compose logs vault'
                echo 'docker-compose logs api'
                echo 'curl http://192.168.11.127:8200/v1/sys/health'
                echo '======================================'
            }
        }
        
        always {
            script {
                echo ''
                echo 'Pipeline Statistics:'
                echo "Build Number: ${BUILD_NUMBER}"
                echo "Duration: ${currentBuild.durationString}"
                echo "Timestamp: ${new Date()}"
                echo ''
                echo 'Pipeline Finished.'
                
                // Nettoyer le workspace
                cleanWs()
            }
        }
    }
}