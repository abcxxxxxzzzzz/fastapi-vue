from datetime import datetime
from datetime import timedelta
from datetime import timezone





def get_today(hms=False):
    SHA_TZ = timezone(
        timedelta(hours=8),
        name='Asia/Shanghai',
    )

    utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)
    beijing_now = utc_now.astimezone(SHA_TZ)

    _now = beijing_now.strftime("%Y-%m-%d")
    if hms:
        _now = beijing_now.strftime("%Y-%m-%d %H:%M:%S")

    return _now
    
    