import uvicorn

import settings
from apps.factory import create_app

app = create_app()

if __name__ == '__main__':
    uvicorn.run('main:app', port=8001, debug=settings.DEBUG, reload=settings.DEBUG)
