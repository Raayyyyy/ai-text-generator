ai-text-generator/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   └── generation.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   └── generate.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── helpers.py
│   ├── config.py
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   │   ├── Header.vue
│   │   │   └── TextGenerator.vue
│   │   ├── views/
│   │   │   ├── Home.vue
│   │   │   ├── Login.vue
│   │   │   └── Generate.vue
│   │   ├── router/
│   │   │   └── index.js
│   │   ├── store/
│   │   │   └── index.js
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json
│   └── vite.config.js
├── docker/
│   ├── backend.Dockerfile
│   └── frontend.Dockerfile
├── docker-compose.yml
└── README.md 