from bs4 import BeautifulSoup


class Node:
    def __init__(self):
        self.header_text = []
        self.table_str = None
        self.table_data = []
        self.tail_text = []
        self.page_index = None
        self.imgs = []
        self.imgs_with_bbox = []
        self.table_with_bbox = []

    def add_table(self, html_content):
        """将HTML表格内容解析并存储到table_data"""
        self.table_str = html_content
        self.table_data = []

        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find('table')
        if not table:
            return

        rows = table.find_all('tr')
        if not rows:
            return

        headers = self._parse_table_headers(rows)
        if not headers:
            return

        self._parse_table_data(rows, headers)

    def _parse_table_headers(self, rows):
        if not rows:
            return []
        first_row = rows[0].find_all(['th', 'td'])
        head_depth = max(int(c.get('rowspan', 1)) for c in first_row) if first_row else 1
        canvas = []
        col_cnt = 0

        for c in first_row:
            if int(c.get('colspan', 1)) > 1:
                canvas.append([c.get_text(strip=True)])
            else:
                canvas.append(c.get_text(strip=True))
            col_cnt += 1

        for r_idx in range(1, head_depth):
            if r_idx >= len(rows):
                break
            c_idx = 0
            for cell in rows[r_idx].find_all(['th', 'td']):
                while type(canvas[c_idx]) == str:
                    c_idx += 1
                    if c_idx >= col_cnt:
                        break
                if c_idx >= col_cnt:
                    break
                txt = cell.get_text(strip=True)
                canvas[c_idx].append(txt)

        flat = []
        for c in range(col_cnt):
            if type(canvas[c]) == list:
                if len(canvas[c]) > 1:
                    for i in canvas[c][1:]:
                        flat.append(i)
                else:
                    flat.append(canvas[c][0])
            else:
                flat.append(canvas[c])
        print(flat)
        return flat

    def _parse_table_data(self, rows, headers):
        """解析表格数据，支持单元格合并"""
        data_rows = rows[self._get_header_rows(rows):]

        rowspan_tracker = {}
        is_header_row = False
        for row_idx, row in enumerate(data_rows):
            cells = row.find_all(['th', 'td'])
            row_data = {}
            col_idx = 0

            if row_idx in rowspan_tracker:
                for col_name, value in rowspan_tracker[row_idx].items():
                    if col_name in headers:
                        row_data[col_name] = value

            for cell in cells:
                if cell.name == 'th':
                    is_header_row = True
                else:
                    is_header_row = False

                while col_idx < len(headers) and headers[col_idx] in row_data:
                    col_idx += 1

                if col_idx >= len(headers):
                    break

                text_content = cell.get_text(separator=' ', strip=True)

                images = cell.find_all('img')
                if images:
                    img_list = [{'src': img.get('src', '')} for img in images]
                    cell_value = {
                        'text': text_content,
                        'images': img_list
                    }
                else:
                    cell_value = text_content

                rowspan = int(cell.get('rowspan', 1))
                if rowspan > 1:
                    for i in range(1, rowspan):
                        next_row = row_idx + i
                        if next_row not in rowspan_tracker:
                            rowspan_tracker[next_row] = {}
                        rowspan_tracker[next_row][headers[col_idx]] = cell_value

                colspan = int(cell.get('colspan', 1))
                for i in range(colspan):
                    if col_idx + i < len(headers):
                        row_data[headers[col_idx + i]] = cell_value

                col_idx += colspan

            for header in headers:
                if header not in row_data:
                    row_data[header] = ""

            if not is_header_row:
                self.table_data.append(row_data)

    def _get_header_rows(self, rows):
        """识别表头行数"""
        if not rows:
            return 1

        max_span = 1
        min_span = 100

        first_row_cells = rows[0].find_all(['th', 'td'])

        for cell in first_row_cells:
            rowspan = int(cell.get('rowspan', 1))
            colspan = int(cell.get('colspan', 1))

            if max_span < rowspan:
                max_span = rowspan
            if max_span < colspan:
                max_span = colspan
            if min_span > rowspan:
                min_span = rowspan
            if min_span > colspan:
                min_span = colspan

        if max_span != min_span:
            return 0

        return max_span

    def to_dict(self):
        """将节点数据转换为字典格式"""
        return {
            "table_str": self.table_str,
            "table_data": self.table_data,
            "tail_text": self.tail_text,
            "header_text": self.header_text,
            "page_index": self.page_index,
            "imgs": self.imgs
        }
