# Cell Monitoring System Demo

## Project Sturcture

```bash
.
├── README.md
├── docker-compose.yml
├── backend/
│   ├── model/
│   ├── provider/
│   ├── router/
│   ├── util/
│   ├── app.py
│   ├── back.dev.Dockerfile
│   ├── requirements.txt
│   ├── .env*
│   └── .gitignore
│
├── frontend/
│   ├── CHANGELOG.md
│   ├── ISSUES_TEMPLATE.md
│   ├── LICENSE.md
│   ├── README.md
│   ├── babel.config.js
│   ├── front.dev.Dockerfile
│   ├── node_modules/*
│   ├── package.json
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── directives/
│   │   ├── layout/
│   │   ├── plugins/
│   │   ├── views/
│   │   ├── App.vue
│   │   ├── main.js
│   │   ├── registerServiceWorker.js
│   │   └── router.js
│   ├── vue.config.js
│   └── yarn.lock
├── requirements.txt
└── .gitignore

*표시된 항목은 ignore
.env에 Camera IP, DB HOST등이 포함되니 실행시 추가
```

## how to run?

- Dockerfile로 실행

    ```bash
    $ docker-compose up --build
    ```

- 로컬 개발환경에서 실행

    ```bash
    # yarn 미설치시
    $ npm install yarn
    # frontend 폴더에서
    $ yarn install && yarn run serve
    ```

    ```bash
    # backend 폴더에서
    $ python3 -m pip virtualenv 
    $ virtualenv venv && source venv/bin/activate
    (venv) $ pip install -r requirements.txt
    (venv) $ python3 app.py
    ```
