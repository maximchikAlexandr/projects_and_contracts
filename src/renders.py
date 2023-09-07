from prettytable import PrettyTable


def to_render_table(data):
    try:
        tbl = PrettyTable()
        tbl.field_names = list(data[0].keys())
        tbl.add_rows([list(dct.values()) for dct in data])
        return tbl
    except IndexError:
        return "Пустой вывод"
