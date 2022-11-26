from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services import Services


def startScheduler(services: Services):
    scheduler = AsyncIOScheduler()
    """
      the row size of the table with the most columns (moisture_level):
        - 8 bytes for timestamp
        - 4 bytes for id
        - 8 bytes for each sensor 1-8

      8 + 4 + 8 * 8 = 72 bytes per row
      assuming the rows of each table are the same size
      with 5 tables, each reading is 5 * 72 = 360 bytes
      the free tier of azure postgres allows for 32GB of storage
      32GB / 360 bytes ≈ 89,000,000 readings (from all systems on each read)
      over a 7 day period that's 89,000,000 / 7 ≈ 12,700,000 readings per day
      which is 12,700,000 / 24 ≈ 530,000 readings per hour
      This is obviously very overkill, but it just shows that we can pretty much
      store data as often as we want without worrying about running out of space

      there may be some other hidden costs both in terms of azure and in the compute
      cost on the raspberry pi
      
      this slowest rate is light/temperature at 5 seoconds. 
    """
    scheduler.add_job(
        services.insertMoistureLevel,
        "interval",
        seconds=5,
    )
    scheduler.add_job(services.insertLight, "interval", seconds=10)
    scheduler.add_job(services.insertTemperature, "interval", seconds=10)
    scheduler.add_job(services.insertWaterLevel, "interval", seconds=5)
    scheduler.start()
