# Python 가상환경(virtualenv) 설정 및 오류 해결 가이드

이 문서는 Python 가상환경(virtualenv 또는 venv)을 생성하고, 활성화하고, 자주 발생하는 오류를 해결하는 방법을 정리한 가이드입니다.

## 1. 가상환경 생성

- 기본 명령어:
  - `python -m venv venv`

프로젝트 루트에서 위 명령을 실행하면 `venv/` 폴더가 만들어집니다.

## 2. 가상환경 활성화

- macOS / Linux:
  - `source venv/bin/activate`
- Windows CMD:
  - `venv\Scripts\activate`
- Windows PowerShell:
  - `.\venv\Scripts\Activate.ps1`

활성화에 성공하면 프롬프트 앞에 `(venv)` 표시가 붙습니다.

## 3. 자주 발생하는 오류와 해결 방법

### 3-1. "command not found: python" 또는 "No such file or directory"

- Python이 설치되어 있는지, PATH에 등록되어 있는지 확인합니다.
- Windows에서는 `python` 대신 `py` 명령을 사용해 볼 수 있습니다.

### 3-2. PowerShell 스크립트 실행 정책 오류

- 오류 예: `running scripts is disabled on this system`
- 해결:
  - PowerShell을 관리자 권한으로 실행한 뒤,
  - `Set-ExecutionPolicy RemoteSigned` 명령을 실행합니다.

## 4. 패키지 설치

가상환경을 활성화한 상태에서:

- `pip install -r requirements.txt`
- 또는 필요한 패키지를 개별적으로 설치합니다.

---

이 문서는 CodeHelpBot의 RAG 엔진이 Python 가상환경 관련 질문에 답변할 때 참고하는 기본 문서입니다.
