import re
import json

with open("raw.txt", encoding="utf-8") as f:
    text = f.read()

prices = re.findall(r"Стоимость\s*\n\s*([\d\s]+,\d+)", text)
products = re.findall(r"\d+\.\n(.+)", text)
total = sum(float(p.replace(' ', '').replace(',', '.')) for p in prices)
datetime = re.search(r"Время:\s*([\d\.]+\s[\d:]+)", text)
paymethod = re.search(r"(Банковская карта|Наличные)", text)


data = {
    "prices": prices,
    "products": products,
    "total": total,
    "datetime": datetime.group(1),
    "paymethod": paymethod.group(1)
}

print(json.dumps(data, ensure_ascii=False, indent=3))