# suya-community
suya community


## Contribute 를 위한 준비

본 프로젝트는 `pyenv` 와 `poetry`를 사용합니다.


- `pyenv`  [맥/리눅스](https://github.com/pyenv/pyenv#installation) 또는 [윈도우 버전](https://github.com/pyenv-win/pyenv-win#installation)을 설치하는 방법
- `poetry` [설치 방법](https://python-poetry.org/docs/#installing-with-the-official-installer)



<span style="color:red;font-size:20px">__반드시 사용방법 숙지 후 진행 해 주시면 됩니다.__</span>

<span style="color:red;font-size:20px">__애매한 것은 항상 질문 후 진행합니다.__</span>

## Contribute 방법

1. suya-community 레포지토리 fork
2. 개발 완료 후 suya-community에 request 발행

## 개발 진행 방법

작업 디렉토리 구조는 다음과 같습니다

```bash
apps
    ├─base
    │  └─.venv
    │      ├─include
    │      │  └─site
    │      │      └─python3.10
    │      │          └─greenlet
    │      ├─Lib
    │      │  └─site-packages
    │      │      ├─aiohttp
    │      │      │  └─.hash
    │      │      ├─aiohttp-3.9.5.dist-info
    │      │      ├─aiosignal
    │      │      ├─aiosignal-1.3.1.dist-info
    │      │      ├─annotated_types
    └─your_project_name

```



1. `your_project_name` 자신의 프로젝트 명으로 폴더명 변경 \
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



