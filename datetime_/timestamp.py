from datetime import datetime
import pytz

ts1 = datetime.utcnow().timestamp()   # 错误写法
ts2 = datetime.now().timestamp()
ts3 = datetime.utcnow().replace(tzinfo=pytz.timezone('UTC')).timestamp()
print(int(ts1), int(ts2), int(ts3))