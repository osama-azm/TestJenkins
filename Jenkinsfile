pipeline {
    agent {
        docker {
            image 'jenkins-new-test:lts' // Replace with the container image you are using
            args '-u root' // Run as root to allow installations
        }
    }

    parameters {
        choice(name: 'SERVICE_NAME', choices: ['shipr-payment', 'shipr-inventory', 'shipr-frontend', 'shipr-inventory-consumer', 'shipr-payment-consumer'], description: 'Select the service to deploy')
    }

    environment {
        DOCKER_HUB_REPO = 'osamaazm/test-repo'
        HELM_VERSION = 'v3.12.0'
    }

    stages {
        stage('Checkout Code') {
            steps {
                script {
                    // checkout([$class: 'GitSCM', branches: [[name: "/Shipr-Containerization/${params.BRANCH_NAME}"]]])
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'GITHUB_CREDENTIALS', url: 'https://github.com/osama-azm/TestJenkins']])
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_HUB_REPO}:${params.SERVICE_NAME} ./${params.SERVICE_NAME}"
                }
            }
        }

        stage('Deploy Docker Image to DockerHub') {
            steps {
                script {
                 withCredentials([string(credentialsId: 'osamaazm', variable: 'osamaazm')]) {
                    sh 'docker login -u osamaazm -p ${osamaazm}'
            }
            sh "docker push ${DOCKER_HUB_REPO}:${params.SERVICE_NAME}"
        }
            }   
        }

        stage('Install Helm') {
            steps {
                script {
                    sh """
                    # Install curl if not already present
                    apt-get update && apt-get install -y curl
                    
                    # Download Helm binary
                    curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
                    
                    # Make the script executable
                    chmod +x get_helm.sh
                    
                    # Run the installation script
                    ./get_helm.sh
                    
                    # Verify Helm installation
                    helm version
                    """
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    sh """
                    helm upgrade --install ${params.SERVICE_NAME} ./Shipr-Helm/${params.SERVICE_NAME} \
                        --set image.repository=${DOCKER_HUB_REPO} \
                        --set image.tag=${params.SERVICE_NAME}
                    """
                }
            }
        }
    }

    post {
        success {
            echo "${params.SERVICE_NAME} has been successfully built, pushed, and deployed!"
        }
        failure {
            echo "${params.SERVICE_NAME} pipeline failed."
        }
    }
}
