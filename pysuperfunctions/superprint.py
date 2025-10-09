import re

__all__ = ["superprint",
           "b","u","e","d","bl","r","h", "i", "s", 
           "bold","underline","italic","strike","dim","blink","reverse","hide",
           "fg","bg","ind","ded"]

# SPECIFIED FORMATTING
 # FORMATTING ANSI CODES
b = bold = '\x1b[1m'
u = underline = '\033[4m'
i = italic = '\x1b[3m'
s = strike = '\x1b[9m'
d = dim = '\x1b[2m'
bl = blink = '\033[25m'
r = reverse = '\x1b[7m'
h = hide = '\x1b[8m'
e = end = '\033[0m'

def ind(spaces: int):
    return " " * spaces

def ded(spaces: int):
    return "\b" * spaces

def fg(hex_code: str):
    hex_code = hex_code.lstrip('#')
    r, g, b = tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))
    return f"\033[38;2;{r};{g};{b}m"

def bg(hex_code: str):
    hex_code = hex_code.lstrip('#')
    r, g, b = tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))
    return f"\033[48;2;{r};{g};{b}m"

class FormatWholeString:
    def __init__(self, content, end="\n", flush=False, indent_size=0):
        self.raw_content = content
        self.styles = []
        self.end = end
        self.flush = flush
        self.indent_size = indent_size

    # WHOLE FORMATTING (chaining)
    def b(self): self.styles.append(b); return self
    def u(self): self.styles.append(u); return self
    def bl(self): self.styles.append(bl); return self
    def r(self): self.styles.append(r); return self
    def h(self): self.styles.append(h); return self
    def i(self): self.styles.append(i); return self
    def s(self): self.styles.append(s); return self
    def d(self): self.styles.append(d); return self
    def fg(self, hex_code): self.styles.append(fg(hex_code)); return self
    def bg(self, hex_code): self.styles.append(bg(hex_code)); return self
    def indent(self, spaces): self.indent_size = spaces; return self

    # TABLE
    def tabulate(self):
        text = self.raw_content
        ansi_pattern = re.compile(r'\x1B\[[0-9;:]*m')
        placeholders = []
        def save_ansi(m):
            placeholders.append(m.group(0))
            return f'§§{len(placeholders)-1}§§'
        text = ansi_pattern.sub(save_ansi, text)
        rows = [r.strip() for r in text.split(";") if r.strip()]
        table_data = [r.split(",") for r in rows]
        table_data = [[c.strip() for c in row] for row in table_data]
        if not table_data:
            self.raw_content = ""
            return self
        max_cols = max(len(r) for r in table_data)
        for row in table_data:
            while len(row) < max_cols:
                row.append("")
        def visible_len(s):
            return len(re.sub(r'§§\d+§§', '', s))
        col_widths = [max(visible_len(r[i]) for r in table_data) for i in range(max_cols)]
        def fmt_row(row):
            cells=[]
            for i,c in enumerate(row):
                pad=col_widths[i]-visible_len(c)
                cells.append(c+' '*pad)
            return "| "+" | ".join(cells)+" |"
        header=fmt_row(table_data[0])
        sep="| "+" | ".join("-"*col_widths[i] for i in range(max_cols))+" |"
        body=[fmt_row(r) for r in table_data[1:]]
        out="\n".join([header,sep]+body)
        def restore_ansi(s):
            for i,p in enumerate(placeholders):
                s=s.replace(f'§§{i}§§',p)
            return s
        self.raw_content=restore_ansi(out)
        return self


    def color_header(self, hex_code):
        fg_code = fg(hex_code)
        e_code = e
        lines = self.raw_content.split("\n")
        if lines:
            lines[0] = fg_code + lines[0] + e_code
        self.raw_content = "\n".join(lines)
        return self

    # CONDITIONAL BEHAVIOR
    def if_(self, condition):
        result = condition() if callable(condition) else condition
        if result: return self
        self.raw_content = ""
        return self
    
    def if_not(self, condition):
        result = condition() if callable(condition) else condition
        if result:
            self.raw_content = ""
            return self
        return self

    # FORMATTING FUNCTION FOR LIST, TUPLES, DICTS, SETS
    def format_content(self, obj, level=0):
        space = " " * (self.indent_size * level)
        next_space = " " * (self.indent_size * (level + 1))

        if isinstance(obj, dict):
            if not obj:
                return "{}"
            items = [f"{next_space}'{k}': {self.format_content(v, level + 1)}" for k, v in obj.items()]
            return "{\n" + ",\n".join(items) + f"\n{space}}}"

        elif isinstance(obj, (list, tuple, set)):
            open_bracket = "[" if isinstance(obj, list) else "(" if isinstance(obj, tuple) else "{"
            close_bracket = "]" if isinstance(obj, list) else ")" if isinstance(obj, tuple) else "}"
            if not obj:
                return open_bracket + close_bracket

            items = []
            for i in obj:
                if isinstance(i, (list, tuple, set, dict)):
                    items.append(self.format_content(i, level + 1))
                else:
                    items.append(repr(i) if isinstance(i, str) else str(i))

            joined = ", ".join(items)
            if all(not isinstance(i, (list, tuple, set, dict)) for i in obj):
                return f"{open_bracket}{joined}{close_bracket}"
            else:
                inner = ",\n".join(f"{next_space}{self.format_content(i, level + 1)}" for i in obj)
                return f"{open_bracket}\n{inner}\n{space}{close_bracket}"

        elif isinstance(obj, str):
            return repr(obj)  # quote strings
        elif isinstance(obj, bool):
            return str(obj).lower()  # true/false instead of True/False
        else:
            return str(obj)



    # PRINTING BEHAVIOR
    def __str__(self):
        formatted = self.format_content(self.raw_content)
        style_prefix = "".join(self.styles)
        return f"{style_prefix}{formatted}{e}"

    def __repr__(self):
        return str(self)

    def __del__(self,level=0):
        space = " " * (self.indent_size * level)
        print(f'{space}{" " * self.indent_size}{str(self)}', end=self.end, flush=self.flush)

# MAIN FUNCTION
def superprint(*objects, sep=" ", end="\n", flush=False):
    if len(objects) == 1:
        content = objects[0]
    else:
        # Multiple simple objects → just join as strings
        content = sep.join(str(obj) for obj in objects)
    return FormatWholeString(content, end=end, flush=flush)
