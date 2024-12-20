pipeline {
    agent {
        kubernetes {
            yaml '''
                apiVersion: v1
                kind: Pod
                spec:
                  containers:
                  - name: tools
                    image: docker:20.10.24-dind
                    command:
                    - sleep
                    args:
                    - "infinity"
                    securityContext:
                      privileged: true
                    env:
                    - name: DOCKER_HOST
                      value: tcp://localhost:2375
                    volumeMounts:
                    - mountPath: /var/run/docker.sock
                      name: docker-sock
                  - name: kubectl-helm
                    image: bitnami/kubectl:latest
                    command:
                    - cat
                    tty: true
                volumes:
                - name: docker-sock
                  hostPath:
                    path: /var/run/docker.sock
            '''
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
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'GITHUB_CREDENTIALS', url: 'https://github.com/osama-azm/TestJenkins']])
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                container('tools') {
                    script {
                        sh "docker build -t ${DOCKER_HUB_REPO}:${params.SERVICE_NAME} ./${params.SERVICE_NAME}"
                    }
                }
            }
        }

        stage('Deploy Docker Image to DockerHub') {
            steps {
                container('tools') {
                    script {
                    withCredentials([string(credentialsId: 'osamaazm', variable: 'osamaazm')]) {
                        sh 'docker login -u osamaazm -p ${osamaazm}'
                        }
                        sh "docker push ${DOCKER_HUB_REPO}:${params.SERVICE_NAME}"
                    }
                }
            }   
        }

        stage('Deploy to Kubernetes') {
            steps {
                container('kubectl-helm') {
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
