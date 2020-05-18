from poverty.celery import app


@app.task(bind=True, name='定时检查')
def celery_task(self, *args, **kwargs):
    pass
