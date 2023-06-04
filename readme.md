# Chat App with Python
Building a simple app with [Flet](https://flet.dev/) (Flutter apps with Python).

Tutorial: https://flet.dev/docs/tutorials/python-realtime-chat 

## Locally 
```shell
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python chat.py
```
## Docker
```shell
docker build -t fridge-roulette:latest .

docker run -p 8550:8550 --rm --init -it --name fridge-roulette fridge-roulette:latest

# go to http://localhost:8550/ in the browser

docker kill fridge-roulette

```
