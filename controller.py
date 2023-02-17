from apscheduler.schedulers.blocking import BlockingScheduler
from open_weather_api import getData

getData()
scheduler = BlockingScheduler()
scheduler.add_job(getData, 'interval', hours=1)
scheduler.start()