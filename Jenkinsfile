pipeline {
    agent {
        docker {
            image 'python:3.11-bullseye'
        }
    }

    triggers {
        githubPush()
    }

    stages {
        stage('Checkout') {
            steps {
                deleteDir()      // 🔥 기존 workspace 완전 삭제
                checkout scm     // 🔄 git clone
            }
        }
        
        stage('Install Dependencies') {
            steps {
                sh '''
                    python -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt

                    npm ci
                '''
            }
        }

        stage('Run Server & Test') {
            steps {
                sh '''
                    # 서버 백그라운드 실행
                    npm run dev &
                    SERVER_PID=$!

                    # 서버 뜰 시간 잠깐 대기
                    sleep 5

                    # pytest 실행
                    . venv/bin/activate
                    pytest tests/test_all.py

                    # 서버 종료
                    kill $SERVER_PID
                '''
            }
        }
    }
}
