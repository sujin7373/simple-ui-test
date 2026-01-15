pipeline {
    agent any

    triggers {
        githubPush()
    }

    stages {
        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    npm install
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
