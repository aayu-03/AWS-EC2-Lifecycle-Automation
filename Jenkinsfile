pipeline {
    agent any
    environment {
        AWS_DEFAULT_REGION = "us-east-1"
        AWS_CREDS = credentials('aws-jenkins-creds')
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/your-username/aws-ec2-lifecycle-automation.git'
            }
        }
        stage('Terraform Init & Plan') {
            steps {
                sh 'terraform init'
                sh 'terraform plan -out=tfplan'
            }
        }
        stage('Terraform Apply') {
            steps {
                input message: "Approve Terraform Apply?"
                sh 'terraform apply -auto-approve tfplan'
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'pip3 install -r requirements.txt'
            }
        }
        stage('Run EC2 Status Check') {
            steps {
                sh 'python3 scripts/ec2_status.py'
            }
        }
        stage('Run Cleanup Script') {
            steps {
                sh 'python3 scripts/cleanup.py'
            }
        }
    }
    post {
        success {
            echo "Pipeline completed successfully."
        }
        failure {
            echo "Pipeline failed. Check logs."
        }
    }
}
