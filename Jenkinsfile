pipeline {
    agent any

    environment {
        AWS_REGION = 'ap-south-1'
	AWS_DEFAULT_REGION = 'ap-south-1'

    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv-ci
                    venv-ci/bin/pip install --upgrade pip
                    venv-ci/bin/pip install boto3 pytest pytest-mock
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    venv-ci/bin/pytest -v
                '''
            }
        }

        stage('Package Lambda') {
            steps {
                sh '''
                    rm -rf lambda-build lambda.zip
                    mkdir -p lambda-build

                    cp -r function lambda-build/

                    cd lambda-build
                    zip -r ../lambda.zip function
                    cd ..

                    ls -lh lambda.zip
                '''
            }
        }

        stage('Terraform Init') {
            steps {
                dir('terraform') {
                    sh '''
                        terraform init
                    '''
                }
            }
        }

        stage('Terraform Validate') {
            steps {
                dir('terraform') {
                    sh '''
                        terraform fmt -check
                        terraform validate
                    '''
                }
            }
        }

        stage('Terraform Plan') {
            steps {
                dir('terraform') {
                    sh '''
                        terraform plan
                    '''
                }
            }
        }

        stage('Approval') {
            steps {
                input message: 'Terraform plan looks good. Apply infrastructure?', 
                      ok: 'Apply'
            }
        }

        stage('Terraform Apply') {
            steps {
                dir('terraform') {
                    sh '''
                        terraform apply -auto-approve
                    '''
                }
            }
        }
    }

    post {
        always {
            sh 'rm -rf venv-ci lambda-build'
        }

        success {
            echo 'Serverless Task API pipeline completed successfully.'
        }

        failure {
            echo 'Pipeline failed. Check the stage logs.'
        }
    }
}
