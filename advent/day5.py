import re

class Parse:
    def __init__(self, rows):
        self._page_rules = []
        prog = re.compile("(\d+)\|(\d+)")
        for row in rows:
            row = row.strip()
            if len(row)==0: break
            m = prog.match(row)
            self._page_rules.append(( int(m.group(1)), int(m.group(2)) ))
        self._page_dict = {}
        for x,y in self._page_rules:
            if x not in self._page_dict:
                self._page_dict[x] = set()
            self._page_dict[x].add(y)
        self._books = []
        for row in rows:
            self._books.append([int(x) for x in row.strip().split(",")])

    @property
    def rules(self):
        return self._page_rules
    
    @property
    def rules_dict(self):
        return self._page_dict

    @property
    def books(self):
        return self._books
    
    def is_ordered(self, book):
        for index in range(len(book)):
            current = book[index]
            # Check all following pages are ordered
            if index < len(book)-1 and current in self._page_dict:
                if not set(book[index+1:]) <= self._page_dict[current]:
                    return False
            # Check nothing before should be after
            if current in self._page_dict:
                befores = set(book[:index])
                if befores & self._page_dict[current]:
                    return False
        return True
    
    def sum_middles_of_ordered(self):
        count = 0
        for book in self._books:
            if self.is_ordered(book):
                middle = book[(len(book)-1)//2]
                count += middle
        return count
    
    class Page:
        def __init__(self, value, parent):
            self._parent = parent
            self._value = value

        def __lt__(self, other):
            if self._value in self._parent.rules_dict:
                smaller_than = self._parent.rules_dict[self._value]
                return other._value in smaller_than
            return False
        
        @property
        def page(self):
            return self._value

    def reorder(self, book):
        pages = [self.Page(v, self) for v in book]
        pages.sort()
        return [page.page for page in pages]
    
    def sum_middles_needed_reordering(self):
        count = 0
        for book in self._books:
            if not self.is_ordered(book):
                new_book = self.reorder(book)
                middle = new_book[(len(new_book)-1)//2]
                count += middle
        return count


def main(second_flag):
    with open("input5.txt") as f:
        pages = Parse(f)
    if not second_flag:
        return pages.sum_middles_of_ordered()
    return pages.sum_middles_needed_reordering()
