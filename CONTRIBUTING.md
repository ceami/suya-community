# Contribution을 위한 준비

본 프로젝트는 `pyenv` 와 `poetry`를 사용합니다.


- `pyenv`  [맥/리눅스](https://github.com/pyenv/pyenv#installation) 또는 [윈도우 버전](https://github.com/pyenv-win/pyenv-win#installation)을 설치하는 방법
- `poetry` [설치 방법](https://python-poetry.org/docs/#installing-with-the-official-installer)



<span style="color:red;font-size:20px">__반드시 사용방법 숙지 후 진행 해 주시면 됩니다.__</span>

<span style="color:red;font-size:20px">__애매한 것은 항상 질문 후 진행합니다.__</span>

## Contribute 방법

 
1. suya-community 레포지토리 fork
2. fork 한 자신의 레포지토리로 이동 후 로컬에 clone

3. 오너 레포지토리와 연결  
    ```bash
    git remote add upstream https://github.com/ceami/suya-community.git
    ```

4. 개발 (자신의 레포지토리 에서 개발)
5. 개발 완료 후 suya-community에 기여 하고자 한다면 자신의 레포에서 pull requests 발행
    - new pull request 클릭 후 변경 내용이나 description 작성 후 제출

6. 최종 적으로 merge 되면 다음 개발 출발~

7. 개발 시작 전 자신의 레포에서 오너 레포와 동기화
    ```bash
        git fetch upstream
        git merge upstream/main # main 브랜치에서 할것
    ```

## 개발 진행 방법

작업 디렉토리 구조는 다음과 같습니다

```bash
.
└─apps
    ├─base
    └─your_project_name
.gitignore
LICENSE

```



1. `apps/`자신의 프로젝트 명으로 폴더 __생성__ 
2. `base`폴더 안 `pyproject.toml` __복사__ 후 자신의 프로젝트 폴더에 __붙여넣기__
3. 자신의 프로젝트 폴더 안 `pyproject.toml` 내용 중 아래 내용 변경

    ```toml
    [tool.poetry]
    name = "{your_project_name}"
    version = "0.1.0"
    description = ""
    authors = ["Yshgodd <kyun20087@naver.com>"]
    readme = "README.md"
    ```
4. 명령창에서 자신의 프로젝트로 이동 후 다음 명령어 입력
    ```bash
        cd your_project_name
        poetry config virtualenvs.in-project true --local
    ```
5. 자신의 프로젝트에서 다음 실행 
    ```bash
        poetry install
    ```

6. 원하는 라이브러리 add 후 개발 



