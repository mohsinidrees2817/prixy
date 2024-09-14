import uvicorn

# load_dotenv()

# PORT = int(os.get('PORT', 8000))
HOST = '0.0.0.0'


# Continue with the rest of your setup

if __name__ == '__main__':
    uvicorn.run('app.api:app', host = HOST, port = 8000, reload = True)