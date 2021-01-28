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
    
    stage('Deployment APP1') {
        agent { kubernetes }
        steps {
            sh 'kubectl apply -f test-app1-deployment.yml';
        }
    }
    stage('Deployment APP2') {
        agent { kubernetes }
        steps {
            sh 'kubectl apply -f test-app1-deployment.yml';
        }
    }
  }
}