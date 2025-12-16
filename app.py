from flask import Flask, jsonify, request
import os
import requests

# Загружаем переменные окружения из файла .env
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route("/proxy-to-giga", methods=["POST"])
def proxy_to_giga():
    # Берём токен из переменных окружения
    gigachat_token = os.getenv("MDE5YjI2YTctM2I1MC03OTMwLWJmYWQtZWY4N2Y2ZmM5MWE2OjE0NjNlM2Q0LTA4YzktNGFjOS04MDlmLWZlYzdhNDE3OWY4Zg==")

    # Проверяем, передан ли токен
    if not gigachat_token:
        return jsonify({"error": "Missing GigaChat Token"}), 500

    # Формируем запрос к GigaChat
    payload = request.get_json(force=True)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {gigachat_token}"
    }

    try:
        # Делаем запрос к GigaChat
        response = requests.post(
            "https://giga.chat/api/completions",
            json=payload,
            headers=headers
        )

        # Возвратим ответ обратно клиенту
        return jsonify(response.json()), response.status_code
    except Exception as e:
        print(f"Ошибка при запросе к GigaChat: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))