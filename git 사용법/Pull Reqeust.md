# 협업을 위한 Git 사용법

>  PR(Pull Reqeust)이 익숙해질 때 까지 이 글이 도움이 되길 바라는 마음에서 작성합니다.
>
> 
>
> 참고 사이트
>
> - [깃 배우기_Atlassian](https://www.atlassian.com/ko/git/tutorials/setting-up-a-repository/git-config)
> - [위키독스_git,github](https://wikidocs.net/book/14452)





Git은 협업을 위한 버전 컨트롤 시스템(`VCS`)으로  많이 사용된다.

깃을 사용하는 이유는 아래와 같다고 보면 된다.

1. 협업하는 모두가 프로젝트 최신화 가능 (fork, clone, pull)
2. 원본을 파괴하지 않고 기능 추가하기 (PR, push)
3. 에러가 발생하면 이전 버전으로 돌아가기 (revoke, reset)



### 개요

1. Fork
2. clone, remote설정
3. branch 생성
4. 수정 작업 후 add, commit, push
5. Pull Request 생성
6. 코드리뷰, Merge Pull Reqest
7. Merge 이후 branch 삭제 및 동기화



## 1. Fork

- 프로젝트 레포지토리를 내 계정의 레포지토리로 가져오는 것

포크를 하는 이유는, 원본을 보존하기 위해서이다.

내 저장소에 먼저 변경을 준 후 PR을 통해 원본에 반영하는 프로세스로 진행하게 된다.

![fork_1](./assets/fork_1.jpg)

원본 repository에 접근하여 fork를 눌러주면



![fork_2](./assets/fork_2.jpg)

이렇게 내 저장소로 fork 되었다는 것을 볼 수 있다.



## 2. Clone, remote

이제 원격 저장소의 레포지토리를, 내 로컬 PC로 가져오는 작업을 한다.

git이라는 원격 저장소 안의 내용들을 내 PC로 가져온 후, 작업을 하게 된다.

- fork로 생성한 내 레포지토리 안에 가서, code - url 카피를 해보자.

![clone_1](./assets/clone_1.jpg)

##### `git clone <url>`

bash창(터미널) 실행 후, 로컬 저장소에 추가해주자.

```bash
git clone https://github.com/JHyuk2/nalanhi.git
```



##### `git remote -<option>`

보통 클론을 통해 생성한 저장소는 main origin이란 이름의 branch로 알아서 연결되어 있다.

```bash
# remote 확인 방법
git remote -v

# output
origin  https://github.com/<user_name>/<repo_name> (fetch)
origin  https://github.com/<user_name>/<repo_name> (push)
```



## 3. Branch

현재 우리는 main이라는 원형 브랜치를 갖고 있는데,

작업을 위한 별도의 브랜치를 나누어 작업을 진행하게 되어야 git의 기능을 비로소 이해할 수 있다.



#### 브랜치의 이점

- 병렬 개발: 팀 멤버들이 서로 충돌 없이 작업할 수 있음
- 기능별 분리: 각 기능 또는 버그 수정을 별도의 브랜치에서 관리할 수 있어 코드 베이스를 깔끔하게 유지 할 수 있다.
- 실험 및 테스트: 새로운 기능을 추가하고 테스트해보고 싶을 때, main(origin)브랜치에 영향을 주지 않고 실험할 수 있는 공간으로써 사용 가능하다.



#### 명령어

- 브랜치 확인 - 로컬 머신의 브랜치를 확인

``` bash
git branch
```

- 리모트 브랜치 확인 - 연결된 리모트 저장소의 브랜치 목록을 보여준다.

```bash
git branch -r
```



### 중요 - 가장 많이 쓰이는 명령어로, git checkout은 꼭 기억해두자

- **브랜치 생성** - 새로운 브랜치를 생성한다. name같은 경우 보통 기능의 이름을 따라간다.

```bash
# 브랜치 생성
git branch <branch_name>

# 브랜치 생성과 동시에 이동
git checkout -b <branch_name>
```

- **브랜치 이동**

```bash
git checkout <branch_name>
```



- 브랜치 간의 차이 비교

```bash
git diff <branch1>..<branch2> -- <file_path>
```

`file path` 의 경우, 확인하고 싶은 파일의 상대 경로 혹은 절대 경로이다.

만약 모든 파일을 비교하고 싶은 경우 와일드카드(예:  `*.ipynb`)를 사용할 수 있다.

#### 

#### 원격 브랜치에서 git checkout

팀과 함께 작업을 할 때 원격 레포지토리를 활용하는 것이 일반적이고, 원격 브랜치를 체크아웃 하려면 먼저 브랜치의 컨텐츠들을 가져와야 한다.

```bash
git fetch -all
```





## 4. 수정 작업 후 add, commit, push



## 5. Pull Request 생성





## 6. 코드리뷰, Merge Pull Reqest



## 7. Merge 이후 branch 삭제 및 동기화