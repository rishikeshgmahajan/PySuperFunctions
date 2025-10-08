from pysuperfunctions import *

list_ = {"name":"Rishi","age":24,"skills":[f"{b}Python{e}","PyQt5","Markdown","C++","HTML","CSS","JavaScript"],"projects":[{"title":"Markdown Editor","features":["syntax highlighting","preview","templates","dark mode"],"language":"Python"},{"title":"Station Master Game","features":["signals","tracks","switches","control panel"],"language":"Python"}],"education":{"degree":"B.Tech","branch":"Computer Science","year":2025},"experience":[{"company":"TechNova","role":"Software Engineer","duration":"1 year"},{"company":"DevForge","role":"Intern","duration":"6 months"}],"social":{"github":"https://github.com/rishi","linkedin":"https://linkedin.com/in/rishi"},"preferences":{"theme":"dark","font":"JetBrains Mono","autosave":"true"},"achievements":["Hackathon Winner 2024","Top 1% Pythonist"],"status":"active"}

superprint(list_).indent(10).indent(-5)
superprint("hello",f"{ded(1)}world","and", f"{ind(-1)}python")