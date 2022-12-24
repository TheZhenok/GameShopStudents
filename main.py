#!/usr/bin/env python
from app import create_app
import config
import settings

# Файл для запуска приложения Flask

app = create_app(config.CONFIGS[settings.APP_SETTINGS])

if __name__ == '__main__':
    app.run()
