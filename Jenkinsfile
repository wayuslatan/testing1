pipeline {
  environment {
    registry1 = "wayuslatan/test-app1"
    registry2 = "wayuslatan/test-app2"
    registryCredential = 'docker/wayuslatan'
    dockerImage = ''
  }

  agent { node { label 'docker-agent' } } 
//  agent any
  stages {
    stage('Cloning Git') {
      steps {
        git 'https://github.com/wayuslatan/testing1.git'
      }
    }
    stage('Building image1') {
      steps{
        script {
          //dockerImage = docker.build registry1 + ":$BUILD_NUMBER"
          dockerImage= docker.build(registry1, "./test1/.")
        }
      }
    }
    stage('Push Image1') {
      steps{
        script {
          docker.withRegistry( '', registryCredential ) {
            dockerImage.push()
          }
        }
      }
    }
    stage('Building image2') {
      steps{
        script {
          //dockerImage = docker.build registry2 + ":$BUILD_NUMBER"
          dockerImage= docker.build(registry2, "./test2/.")
        }
      }
    }
    stage('Push Image2') {
      steps{
        script {
          docker.withRegistry( '', registryCredential ) {
            dockerImage.push()
          }
        }
      }
    }
    stage('Remove Unused docker image1') {
      steps{
        //sh "docker rmi $registry1:$BUILD_NUMBER"
        sh "docker rmi $registry1"
      }
    }
    stage('Remove Unused docker image2') {
      steps{
        //sh "docker rmi $registry2:$BUILD_NUMBER"
        sh "docker rmi $registry2"
      }
    }

    stage('MetalLB Configmap') {
        agent { label 'master' }
        steps {
          script {  
            sh 'hostname';
            sh 'kubectl apply -f metallb-configmap.yml';
          }
        }
    }

    stage('Deployment DB + Service') {
        agent { label 'master' }
        steps {
          script {  
            sh 'hostname';
            try {
              sh 'kubectl rollout restart -f elasticsearch-deployment.yml';
            }
            catch (err) {
              echo err.getMessage()
            }
            sh 'kubectl apply -f elasticsearch-deployment.yml';
            sh 'kubectl apply -f elasticsearch-service.yml';
          }
        }
    }

    stage('Deployment Kibana + Service') {
        agent { label 'master' }
        steps {
          script {
            sh 'hostname';
            try {
              sh 'kubectl rollout restart -f kibana-deployment.yml 2> /dev/null';
            }
            catch (err) {
              echo err.getMessage()
            }
            sh 'kubectl apply -f kibana-deployment.yml';
            sh 'kubectl apply -f kibana-lb.yml';
            //sh 'kubectl apply -f kibana-service.yml';
          }
        }
    }
    
    stage('Deployment APP1') {
        agent { label 'master' }
        steps {
          script {
            sh 'hostname';
            try {
              sh 'kubectl rollout restart -f test-app1-deployment.yml 2> /dev/null';
            }
            catch (err) {
              echo err.getMessage()
            }
            sh 'kubectl apply -f test-app1-deployment.yml';
            sh 'kubectl apply -f vote-lb.yml';
            //sh 'kubectl apply -f vote-service.yml';
          }
        }
    }
    stage('Deployment APP2') {
        agent { label 'master' }
        steps {
          script {
            try {
              sh 'kubectl rollout restart -f test-app2-deployment.yml 2> /dev/null';
            }
            catch (err) {
              echo err.getMessage()
            }
            sh 'kubectl apply -f test-app2-deployment.yml';
            sh 'kubectl apply -f result-lb.yml'
            //sh 'kubectl apply -f result-service.yml'
          }
        }
    }
  }
}