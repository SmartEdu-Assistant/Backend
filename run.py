"""
Скрипт для запуска FastAPI приложения.
Использует uvicorn сервер с автоматической перезагрузкой
"""

import uvicorn


def main():
    """
    Запускает сервер с настройками для разработки.
    """
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True, log_level="info")


if __name__ == "__main__":
    main()
