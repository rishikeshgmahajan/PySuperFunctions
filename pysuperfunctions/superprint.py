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

    # FORMATTING FUNCTION (runs only when printing/str)
    def format_content(self, obj, level=0):
        space = " " * (self.indent_size * level)
        if isinstance(obj, dict):
            if not obj: return "{}"
            items = [f'{space}{" " * self.indent_size}"{k}": {self.format_content(v, level+1)}' for k,v in obj.items()]
            return "{\n" + ",\n".join(items) + f"\n{space}}}"
        elif isinstance(obj, list):
            if not obj: return "[]"
            items = [f'{space}{" " * self.indent_size}{self.format_content(i, level+1)}' for i in obj]
            return "[\n" + ",\n".join(items) + f"\n{space}]"
        elif isinstance(obj, tuple):
            if not obj: return "()"
            items = [f'{space}{" " * self.indent_size}{self.format_content(i, level+1)}' for i in obj]
            return "(\n" + ",\n".join(items) + f"\n{space})"
        elif isinstance(obj, set):
            if not obj: return "set()"
            items = [f'{space}{" " * self.indent_size}{self.format_content(i, level+1)}' for i in obj]
            return "{\n" + ",\n".join(items) + f"\n{space}}}"
        elif isinstance(obj, str): return obj
        else: return str(obj)

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
