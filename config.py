import os
SYS_CONFIG = {
    # 企业微信企业ID,必填
    "corpid": "ww3273008fc653a8d4",
    # 企业微信应用Secret,必填
    "corpsecret": "inQR78a0PjCCPpvXwDhhU",
    # 企业微信AgentId,必填
    "agentid": "1000002",
    "notionsecret": "secret_as3cj6Rg9fY5pE2NXyY9EmZe2kO8b4UlctTgI6ZKfib",
    "databaseid": "ef4eadd8f84d4dee803a2681d1749e0f"
}


def get(key: str):
    value = os.getenv(key)
    if value is None:
        if key in SYS_CONFIG:
            value = SYS_CONFIG[key]
    return value
