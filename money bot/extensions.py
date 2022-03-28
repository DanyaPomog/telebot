import requests
import json
from config import keys

class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException("Нельзя конвертировать одну и туже валюту.")

        try:
            quote_ticer = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticer = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать валюту {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticer}&tsyms={base_ticer}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base
