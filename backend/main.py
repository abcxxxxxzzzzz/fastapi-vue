from api import create_app
import uvicorn



app = create_app()



if __name__ == '__main__':
    uvicorn.run(
            'main:app',
            host='0.0.0.0', 
            port=8001, 
            reload=True,
            # log_config=log_config,
            # access_log=True,
            # workers=8, 
            # use_colors=True
        )

# nohup gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --timeout 120 --bind 0.0.0.0:8000 &