import csv
import os
from tabulate import tabulate


class PriceMachine:

    def __init__(self):
        self.data = []

    def load_prices(self, file_path='price_lists/'):
        for file in os.listdir(file_path):
            if 'price' in file.lower():
                with open(file_path + file, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f, delimiter=',')
                    for row_num, row in enumerate(reader):
                        if row_num == 0:
                            col = row
                            name_col = next((i for i, col_name in enumerate(col) if
                                             col_name.lower() in ['название', 'продукт', 'товар', 'наименование']))
                            price_col = next(
                                (i for i, col_name in enumerate(col) if col_name.lower() in ['цена', 'розница']))
                            weight_col = next((i for i, col_name in enumerate(col) if
                                               col_name.lower() in ['фасовка', 'масса', 'вес']))
                        else:
                            name = row[name_col]
                            price = row[price_col]
                            weight = row[weight_col]
                            self.data.append({'name': name, 'price': price, 'weight': weight, 'file': file})

    def export_to_html(self, fname='output.html'):
        result = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Позиции продуктов</title>
        </head>
        <body>
            <table>
                <tr>
                    <th>Номер</th>
                    <th>Название</th>
                    <th>Цена</th>
                    <th>Фасовка</th>
                    <th>Файл</th>
                    <th>Цена за кг.</th>
                </tr>
        '''
        self.data = sorted(self.data, key=lambda x: float(x['price']) / float(x['weight']))
        for i, item in enumerate(self.data):
            result += '<tr>'
            result += f'<td>{i + 1}</td>'
            result += f'<td>{item["name"]}</td>'
            result += f'<td>{item["price"]}</td>'
            result += f'<td>{item["weight"]}</td>'
            result += f'<td>{item["file"]}</td>'
            result += f'<td>{float(item["price"]) / float(item["weight"]):.2f}</td>'
            result += '</tr>'
        result += '</table></body></html>'

        with open(fname, 'w', encoding='utf-8') as f:
            f.write(result)

    def find_text(self, text):
        result = []
        text_lower = text.lower()
        for item in self.data:
            if text_lower in item['name'].lower():
                result.append(item)
        result = sorted(result, key=lambda x: float(x['price']) / float(x['weight']))
        print(tabulate([(i + 1, item['name'], item['price'], item['weight'], item['file'],
                         float(item['price']) / float(item['weight'])) for i, item in enumerate(result)],
                       headers=['№', 'Название', 'Цена', 'Вес', 'Файл', 'Цена за кг.'], tablefmt='grid'))


pm = PriceMachine()
pm.load_prices()
pm.export_to_html('output.html')
while True:
    user_input = input('Введите текст для поиска или "exit" для выхода: ')
    if user_input.lower() == 'exit':
        print('Работа завершена')
        break
    pm.find_text(user_input)
