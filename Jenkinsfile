pipeline {
  environment {
    registry1 = "wayuslatan/test-app1"
    registry2 = "wayuslatan/test-app2"
    registryCredential = 'docker/wayuslatan'
    dockerImage = ''
  }

  agent { node { label 'docker-agent' } } 
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
          dockerImage= docker.build(registry1, "-f /test1/Dockerfile")
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
          dockerImage= docker.build(registry2, "-f /test2/Dockerfile")
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
        sh "docker rmi $registry1:$BUILD_NUMBER"
      }
    }
    stage('Remove Unused docker image2') {
      steps{
        sh "docker rmi $registry2:$BUILD_NUMBER"
      }
    }
    stage('Deployment APP1') {
        steps {
            sh 'kubectl apply -f test-app1-deployment.yml';
        }
    }
    stage('Deployment APP2') {
        steps {
            sh 'kubectl apply -f test-app1-deployment.yml';
        }
    }
  }
}