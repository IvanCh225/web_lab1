import requests
from flask import Flask
app = Flask(__name__)

code = input("Введи ISO-2 код країни: ")
@app.route("/")
def home():
    url = f"http://api.worldbank.org/v2/country/{code}?format=json"
    response = requests.get(url)

    if response.status_code != 200:
        return f"Помилка HTTP: {response.status_code}<br>URL: {url}"
    try:
        data = response.json()
    except Exception:
        return "Не вдалося розпізнати JSON-відповідь від API."

    if not isinstance(data, list) or len(data) < 2 or not data[1]:
        return f"Країну за кодом '{code}' не знайдено.<br>Перевір URL: {url}"

    country = data[1][0]

    name = country.get("name", "—")
    capital = country.get("capitalCity", "—")
    region = country.get("region", {}).get("value", "—")
    income = country.get("incomeLevel", {}).get("value", "—")
    lending = country.get("lendingType", {}).get("value", "—")
    iso2 = country.get("iso2Code", "—")
    longitude = country.get("longitude", "—")
    latitude = country.get("latitude", "—")
    return (f"ISO-2 код: {iso2}<br>Країна: {name}<br>Столиця: {capital}<br>Регіон: {region}<br>Рівень доходу: {income}<br>"
            f"Тип кредитування: {lending}<br>Координати: lat={latitude}, lon={longitude}<br>")

if __name__ == "__main__":
    app.run()