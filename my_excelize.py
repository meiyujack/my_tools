from openpyxl import load_workbook


def get_sheet(file_name,sheet_name):
    return load_workbook(file_name)[sheet_name]



def search_item_to_text(sheet, search_column_index, goal_column_index, item,rows=1):
    """
    类vlookup函数查询
    :param address: excel文件路径
    :param sheet_name: excel文件的工作簿
    :param rows: 表头所在行数,默认为1
    :param search_column_index: 待查找的某列索引，1开头
    :param goal_column_index: 对应某列的索引，1开头
    :param item: 待查找的信息
    :return: 目标值
    """

    for r in range(rows, sheet.max_row + 1):
        if sheet.cell(r, search_column_index).value == item:
            return sheet.cell(r, goal_column_index).value


def read_excel(excel_detail, iter=None, keys=None):
    sheet = excel_detail[0]
    rows = excel_detail[1]
    cols = excel_detail[2]
    if not keys:
        keys = []
        for c in range(1, cols + 1):
            keys.append(sheet.cell(1, c).value)
    if not iter:
        iter = rows
    for r in range(2, rows + 1):
        if iter >= r - 1:
            print(f"record{r - 1}:")
            record = []
            for c in range(1, cols + 1):
                value = sheet.cell(r, c).value
                if value:
                    if isinstance(value, str):
                        if ',' and ':' in value:
                            items = value.split(',')
                            k = []
                            v = []
                            for i in items:
                                n = i.split(':')
                                k.append(n[0])
                                v.append(n[1])
                            yield dict(zip(k, v))
                    record.append(value)
            yield dict(zip(keys, record))
