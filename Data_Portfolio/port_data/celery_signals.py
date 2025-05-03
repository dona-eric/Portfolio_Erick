from celery.signals import worker_ready
from .tasks import fetch_medium_articles_task

@worker_ready.connect
def at_start(sender, **kwargs):
    username = "koulodjiric"  
    print(f"⚙️ Tâche de récupération d'articles Medium lancée pour @{username}")
    sender.app.send_task('Data_Portfolio.port_data.tasks.fetch_medium_articles_task', args=[username])
