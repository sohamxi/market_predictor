from crontab import CronTab

cron = CronTab(tab="""
  * * * * * C:/Users/soham/AppData/Local/Programs/Python/Python36-32/python.exe D:/MoneyMaker/market_predictor/Core/Experimentation/load_data.py
""")

# job = cron.new(command='python D:/MoneyMaker/market_predictor/Core/Experimentation/load_data.py', comment='Creating a cron job for loading koinex data every minute')

# job.minute.every(1)

for job in cron:
    print(job)
    print(job.is_enabled())

for result in cron.run_scheduler():
    print(result)
    print ("This was printed to stdout by the process.")