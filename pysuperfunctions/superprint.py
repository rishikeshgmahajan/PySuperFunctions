__all__ = ["superprint","b","u","e","fg","bg"]

b = '\033[1m'
u = '\033[4m'
e = '\033[0m'

def fg(hex_code: str):
    hex_code = hex_code.lstrip('#')
    r, g, b = tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))
    return f"\033[38;2;{r};{g};{b}m"

def bg(hex_code: str):
    hex_code = hex_code.lstrip('#')
    r, g, b = tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))
    return f"\033[48;2;{r};{g};{b}m"

class FormatWholeString:
    def __init__(self, content):
        self.content = content
        self.styles = []

    def b(self):
        self.styles.append(b)
        return self

    def u(self):
        self.styles.append(u)
        return self

    def fg(self, hex_code):
        self.styles.append(fg(hex_code))
        return self

    def bg(self, hex_code):
        
        self.styles.append(bg(hex_code))
        return self
    
    def if_(self, condition):
        result = condition() if callable(condition) else condition
        if result:
            return self
        else:
            self.content = ""
            return self
        
    def if_not(self, condition):
        result = condition() if callable(condition) else condition
        if result:
            self.content = ""
            return self
        else:
            return self

    def __del__(self):
        style_prefix = "".join(self.styles)
        print(f"{style_prefix}{self.content}{e}")

    def __str__(self):
        style_prefix = "".join(self.styles)
        return f"{style_prefix}{self.content}{e}"

    def __repr__(self):
        return str(self)
    
def superprint(*objects, sep=" ", end="\n", flush=False):
    string_to_be_formatted = sep.join(map(str, objects))
    return FormatWholeString(string_to_be_formatted)
