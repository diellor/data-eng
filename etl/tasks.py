from celery import shared_task

from etl.services import VikingsShowService, NorsemenShowService
from scraping.services import VikingsShowRawDataService, NorsemenShowRawDataService


@shared_task
def run_vikings_show_service():
    """Run the VikingsShowService task."""
    VikingsShowRawDataService().handle()
    VikingsShowService().handle()


@shared_task
def run_norsemen_show_service():
    """Run the NorsemenShowService task."""
    NorsemenShowRawDataService().handle()
    NorsemenShowService().handle()
