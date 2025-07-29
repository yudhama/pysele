pipeline {
    agent any
    
    environment {
        // Python virtual environment
        VENV_NAME = 'venv'
        PYTHON_VERSION = '3.9'
        // Test reports
        HTML_REPORT = 'petstore_api_test_report.html'
        XML_REPORT = 'petstore_api_test_results.xml'
        COVERAGE_REPORT = 'htmlcov/index.html'
        SECURITY_REPORT = 'security_test.log'
    }
    
    options {
        // Keep builds for 30 days
        buildDiscarder(logRotator(daysToKeepStr: '30', numToKeepStr: '10'))
        // Timeout after 30 minutes
        timeout(time: 30, unit: 'MINUTES')
        // Add timestamps to console output
        timestamps()
    }
    
    triggers {
        // Poll SCM every 5 minutes for changes
        pollSCM('H/5 * * * *')
        // Build daily at 2 AM
        cron('0 2 * * *')
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo '🔄 Checking out source code...'
                checkout scm
                
                script {
                    // Get commit info
                    env.GIT_COMMIT_SHORT = sh(
                        script: 'git rev-parse --short HEAD',
                        returnStdout: true
                    ).trim()
                    env.GIT_BRANCH_NAME = sh(
                        script: 'git rev-parse --abbrev-ref HEAD',
                        returnStdout: true
                    ).trim()
                }
                
                echo "📋 Building commit: ${env.GIT_COMMIT_SHORT} on branch: ${env.GIT_BRANCH_NAME}"
            }
        }
        
        stage('Setup Environment') {
            steps {
                echo '🐍 Setting up Python environment...'
                
                script {
                    if (isUnix()) {
                        sh '''
                            # Create virtual environment
                            python3 -m venv ${VENV_NAME}
                            
                            # Activate virtual environment and upgrade pip
                            . ${VENV_NAME}/bin/activate
                            pip install --upgrade pip setuptools wheel
                            
                            # Install dependencies
                            pip install -r requirements.txt
                            
                            # Verify installation
                            pip list
                        '''
                    } else {
                        bat '''
                            REM Create virtual environment
                            python -m venv %VENV_NAME%
                            
                            REM Activate virtual environment and upgrade pip
                            call %VENV_NAME%\\Scripts\\activate.bat
                            pip install --upgrade pip setuptools wheel
                            
                            REM Install dependencies
                            pip install -r requirements.txt
                            
                            REM Verify installation
                            pip list
                        '''
                    }
                }
            }
        }
        
        stage('Code Quality Checks') {
            parallel {
                stage('Linting') {
                    steps {
                        echo '🔍 Running code quality checks...'
                        
                        script {
                            if (isUnix()) {
                                sh '''
                                    . ${VENV_NAME}/bin/activate
                                    
                                    echo "Running flake8..."
                                    flake8 cobaTest/ --max-line-length=88 --extend-ignore=E203,W503 || true
                                    
                                    echo "Running pylint..."
                                    pylint cobaTest/ --output-format=text --reports=no || true
                                    
                                    echo "Running mypy..."
                                    mypy cobaTest/ --ignore-missing-imports || true
                                '''
                            } else {
                                bat '''
                                    call %VENV_NAME%\\Scripts\\activate.bat
                                    
                                    echo "Running flake8..."
                                    flake8 cobaTest\\ --max-line-length=88 --extend-ignore=E203,W503 || exit /b 0
                                    
                                    echo "Running pylint..."
                                    pylint cobaTest\\ --output-format=text --reports=no || exit /b 0
                                    
                                    echo "Running mypy..."
                                    mypy cobaTest\\ --ignore-missing-imports || exit /b 0
                                '''
                            }
                        }
                    }
                }
                
                stage('Security Scan') {
                    steps {
                        echo '🔒 Running security analysis...'
                        
                        script {
                            if (isUnix()) {
                                sh '''
                                    . ${VENV_NAME}/bin/activate
                                    
                                    echo "Running bandit security scan..."
                                    bandit -r cobaTest/ -f txt -o ${SECURITY_REPORT} || true
                                    
                                    # Display security report summary
                                    if [ -f "${SECURITY_REPORT}" ]; then
                                        echo "Security scan completed. Report saved to ${SECURITY_REPORT}"
                                        tail -20 ${SECURITY_REPORT}
                                    fi
                                '''
                            } else {
                                bat '''
                                    call %VENV_NAME%\\Scripts\\activate.bat
                                    
                                    echo "Running bandit security scan..."
                                    bandit -r cobaTest\\ -f txt -o %SECURITY_REPORT% || exit /b 0
                                    
                                    REM Display security report summary
                                    if exist "%SECURITY_REPORT%" (
                                        echo "Security scan completed. Report saved to %SECURITY_REPORT%"
                                        type %SECURITY_REPORT%
                                    )
                                '''
                            }
                        }
                    }
                }
            }
        }
        
        stage('Install Browser Dependencies') {
            steps {
                echo '🌐 Setting up browser dependencies...'
                
                script {
                    if (isUnix()) {
                        sh '''
                            . ${VENV_NAME}/bin/activate
                            
                            # Install Chrome/Chromium for headless testing
                            if command -v google-chrome >/dev/null 2>&1; then
                                echo "Chrome already installed"
                                google-chrome --version
                            elif command -v chromium-browser >/dev/null 2>&1; then
                                echo "Chromium already installed"
                                chromium-browser --version
                            else
                                echo "Installing Chrome dependencies..."
                                # This will be handled by webdriver-manager
                            fi
                            
                            # Verify webdriver-manager can download drivers
                            python -c "from webdriver_manager.chrome import ChromeDriverManager; ChromeDriverManager().install()"
                        '''
                    } else {
                        bat '''
                            call %VENV_NAME%\\Scripts\\activate.bat
                            
                            REM Verify webdriver-manager can download drivers
                            python -c "from webdriver_manager.chrome import ChromeDriverManager; ChromeDriverManager().install()"
                        '''
                    }
                }
            }
        }
        
        stage('Run Tests') {
            parallel {
                stage('API Tests') {
                    steps {
                        echo '🧪 Running API tests...'
                        
                        script {
                            if (isUnix()) {
                                sh '''
                                    . ${VENV_NAME}/bin/activate
                                    
                                    # Change to API test directory
                                    cd cobaTest/tests/api
                                    
                                    # Run API tests with coverage
                                    python run_petstore_tests.py --test-type all
                                    
                                    # Move reports to workspace root
                                    mv petstore_api_test_report.html ../../../
                                    mv petstore_api_test_results.xml ../../../
                                '''
                            } else {
                                bat '''
                                    call %VENV_NAME%\\Scripts\\activate.bat
                                    
                                    REM Change to API test directory
                                    cd cobaTest\\tests\\api
                                    
                                    REM Run API tests
                                    python run_petstore_tests.py --test-type all
                                    
                                    REM Move reports to workspace root
                                    move petstore_api_test_report.html ..\\..\\..\\
                                    move petstore_api_test_results.xml ..\\..\\..\\
                                '''
                            }
                        }
                    }
                }
                
                stage('Selenium Tests') {
                    steps {
                        echo '🕷️ Running Selenium tests...'
                        
                        script {
                            if (isUnix()) {
                                sh '''
                                    . ${VENV_NAME}/bin/activate
                                    
                                    # Run Selenium tests with headless browser
                                    cd cobaTest/tests
                                    
                                    # Run main appointment test
                                    python -m pytest test_make_appointment.py -v \
                                        --html=selenium_test_report.html \
                                        --self-contained-html \
                                        --junitxml=selenium_test_results.xml || true
                                    
                                    # Move reports to workspace root
                                    mv selenium_test_report.html ../../
                                    mv selenium_test_results.xml ../../
                                '''
                            } else {
                                bat '''
                                    call %VENV_NAME%\\Scripts\\activate.bat
                                    
                                    REM Run Selenium tests
                                    cd cobaTest\\tests
                                    
                                    REM Run main appointment test
                                    python -m pytest test_make_appointment.py -v ^
                                        --html=selenium_test_report.html ^
                                        --self-contained-html ^
                                        --junitxml=selenium_test_results.xml || exit /b 0
                                    
                                    REM Move reports to workspace root
                                    move selenium_test_report.html ..\\..\\
                                    move selenium_test_results.xml ..\\..\\
                                '''
                            }
                        }
                    }
                }
            }
        }
        
        stage('Generate Coverage Report') {
            steps {
                echo '📊 Generating coverage report...'
                
                script {
                    if (isUnix()) {
                        sh '''
                            . ${VENV_NAME}/bin/activate
                            
                            # Generate coverage report if .coverage file exists
                            if [ -f ".coverage" ]; then
                                coverage html
                                coverage report
                                echo "Coverage report generated at htmlcov/index.html"
                            else
                                echo "No coverage data found"
                            fi
                        '''
                    } else {
                        bat '''
                            call %VENV_NAME%\\Scripts\\activate.bat
                            
                            REM Generate coverage report if .coverage file exists
                            if exist ".coverage" (
                                coverage html
                                coverage report
                                echo "Coverage report generated at htmlcov\\index.html"
                            ) else (
                                echo "No coverage data found"
                            )
                        '''
                    }
                }
            }
        }
    }
    
    post {
        always {
            echo '📋 Publishing test results and reports...'
            
            // Publish test results
            script {
                // Publish JUnit test results
                if (fileExists('petstore_api_test_results.xml')) {
                    publishTestResults testResultsPattern: 'petstore_api_test_results.xml'
                }
                if (fileExists('selenium_test_results.xml')) {
                    publishTestResults testResultsPattern: 'selenium_test_results.xml'
                }
                
                // Publish HTML reports
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: '.',
                    reportFiles: 'petstore_api_test_report.html',
                    reportName: 'API Test Report',
                    reportTitles: 'Petstore API Test Results'
                ])
                
                if (fileExists('selenium_test_report.html')) {
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: '.',
                        reportFiles: 'selenium_test_report.html',
                        reportName: 'Selenium Test Report',
                        reportTitles: 'Selenium Test Results'
                    ])
                }
                
                // Publish coverage report
                if (fileExists('htmlcov/index.html')) {
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report',
                        reportTitles: 'Code Coverage Results'
                    ])
                }
                
                // Archive artifacts
                archiveArtifacts artifacts: '*.html,*.xml,*.log,htmlcov/**/*', allowEmptyArchive: true
            }
            
            // Clean up virtual environment
            script {
                if (isUnix()) {
                    sh 'rm -rf ${VENV_NAME}'
                } else {
                    bat 'rmdir /s /q %VENV_NAME%'
                }
            }
        }
        
        success {
            echo '✅ Pipeline completed successfully!'
            
            // Send success notification (optional)
            script {
                if (env.BRANCH_NAME == 'master' || env.BRANCH_NAME == 'main') {
                    // Add notification logic here (email, Slack, etc.)
                    echo '📧 Sending success notification for main branch...'
                }
            }
        }
        
        failure {
            echo '❌ Pipeline failed!'
            
            // Send failure notification (optional)
            script {
                // Add notification logic here (email, Slack, etc.)
                echo '📧 Sending failure notification...'
            }
        }
        
        unstable {
            echo '⚠️ Pipeline completed with test failures!'
        }
    }
}