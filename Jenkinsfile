pipeline {
    agent any

    environment {
        HEADLESS = 'true' // 컨테이너 안에서 헤드리스 모드
        VENV_DIR = "${WORKSPACE}/venv"
    }

    triggers {
        githubPush()
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/sujin7373/simple-ui-test.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv $VENV_DIR
                    . $VENV_DIR/bin/activate
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
                    . $VENV_DIR/bin/activate
                    pytest tests/test_all.py

                    # 서버 종료
                    kill $SERVER_PID
                '''
            }
        }
    }
}
