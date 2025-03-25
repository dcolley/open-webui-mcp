

## Backend

```bash
cd backend

# python3 -m venv venv
uv venv --python=3.12 .venv-3.12

source .venv-3.12/bin/activate
# uv pip install -r requirements.txt

export ENABLE_OLLAMA_API=true
export OLLAMA_BASE_URLS=http://localhost:11434

export ENABLE_OPENAI_API=true
export OPENAI_API_BASE_URL=http://localhost:1234/v1
export OPENAI_API_KEY=lm-studio

# open-webui serve
```

## Dev

```bash
./dev.sh
```


Launch browser:

http://localhost:8080

## Frontend

```bash
yarn run dev
```
