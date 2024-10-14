from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()


API_KEY = "ваш-API-KEY"
BASE_URL = f"https://v6.exchangerate-api.com/v6/"


@app.get("/api/rates")
async def currency_converter(from_currency: str, to_currency: str, value: float) -> dict:
    """
    Конвертирует значение из одной валюты в другую.

    Args:
        from_currency: Исходная валюта
        to_currency: Целевая валюта
        value: Значение для конвертации

    Returns:
        Словарь с результатом конвертации, округленным до двух знаков после запятой.

    """

    url = f"{BASE_URL}/{API_KEY}/pair/{from_currency}/{to_currency}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()

            if data["result"] == "success":
                rate = data["conversion_rate"]
                result = rate * value
                return {"result": round(result, 2)}

            else:
                raise HTTPException(status_code=400, detail="Failed to get exchange rate")

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
