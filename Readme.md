# Zendesk order handling chatbot
## Documentation
All the explanation and performance analysis of the bot can be found [here](Documentation/doc.md).
## Setup

### Install Opik (for tracking)
```bash
# Clone the Opik repository
git clone https://github.com/comet-ml/opik.git

# Navigate to the opik/deployment/docker-compose directory
cd opik/deployment/docker-compose

# Optionally, you can force a pull of the latest images
docker compose pull

# Start the Opik platform
docker compose up --detach

# You can now visit http://localhost:5173 on your browser!
```
### Python dependencies


```bash
conda create -n zendesk_env python=3.12 -y
conda activate zendesk_env
pip install -r requirements.txt
```
### Config
Copy the .env.sample file to .env and fill in the necessary values (Azure Openai config) .

```bash
cp .env.sample .env
```
### Startup
```bash
docker compose up --detach
uvicorn app:app --port 8001
```
Type 'y' when prompted to accept the use of Opik server.
```bash
uvicorn order_endpoints:app --port 8002
```
Type 'y' when prompted to accept the use of Opik server.

## Demo
![zendesk_demo_gif.gif](demo_zendesk_chatbot_ffmpeg.gif)

## Observability
- Go to [Opik](http://http://localhost:5173/default/projects) and click on the Default project.
- To view traces -> Traces Tab
- To view Metrics (Evaluation + Token usage + Duration) -> Metrics Tab
- Detailed LLM calls -> LLM calls Tab


## Run tests
#### Before running the tests:
1. Go to root of the project directory.
2. Make sure opik server is running on port 5173.
3. Run the following command: ```export OPIK_URL_OVERRIDE="http://localhost:5173/"```
4. Run tests
```bash
pytest tests
```


