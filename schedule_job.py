from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone
import subprocess
import time

def download_data():
    strategy_list = ['KDJ_GAP','RSI']
    for strategy in strategy_list:
        subprocess.run(["python",f"{strategy}/downloader.py"], check=True)
        print(f"{strategy} data downloaded")
def equity_record():
    print("Equity Record will be implemented")

# Create a scheduler instance
scheduler = BackgroundScheduler()

# Assuming US Eastern Time for example, use 'America/New_York'
us_eastern = timezone('America/New_York')
hong_kong = timezone("Asia/Hong_Kong")
# Schedule jobs to run at midnight and 8 AM Eastern Time
scheduler.add_job(download_data, 'cron', hour=9, minute=56, second=0, timezone=us_eastern)
scheduler.add_job(equity_record, 'cron', hour=0, minute=0, second=0, timezone=hong_kong)

scheduler.start()

try:
    # Simulate application activity (keep the main thread alive)
    while True:
        time.sleep(2)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()