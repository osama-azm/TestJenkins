pipeline {
    agent any

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


        stage('Set Up Container') {
            steps {
                script {
                    sh '''
                    # Start a container with the required image
                    docker run --rm -d --name jenkins-container -v $(pwd):/workspace -w /workspace ubuntu:20.04 sleep 3600
                    '''
                }
            }
        }

        stage('Install Helm') {
            steps {
                script {
                    sh """
                    docker exec -u root jenkins-container bash -c "
                        apt-get update && apt-get install -y curl &&
                        curl -fsSL -o helm.tar.gz https://get.helm.sh/helm-$HELM_VERSION-linux-amd64.tar.gz &&
                        tar -zxvf helm.tar.gz --strip-components=1 -C /usr/local/bin linux-amd64/helm &&
                        helm version
                    "
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
