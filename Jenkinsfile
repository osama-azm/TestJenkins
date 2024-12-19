pipeline {
    agent any

    parameters {
        choice(name: 'SERVICE_NAME', choices: ['shipr-payment', 'shipr-inventory', 'shipr-frontend', 'shipr-inventory-consumer', 'shipr-payment-consumer'], description: 'Select the service to deploy')
    }

    environment {
        DOCKER_HUB_REPO = 'osamaazm/test-repo'
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
                    curl -fsSL https://get.helm.sh/helm-v3.16.4-linux-amd64.tar.gz -o helm.tar.gz
                    tar -zxvf helm.tar.gz
                    mv linux-amd64/helm ./helm
                    chmod +x ./helm
                    ./helm version
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
