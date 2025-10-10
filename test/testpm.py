from pysuperfunctions import *
import pprint

json = {"name":"Rishi","age":25,"skills":["Python","C++","PyQt5"],"projects":[{"title":"Markdown Editor","year":2024},{"title":"Station Master Game","year":2025}],"active":"true"}

superprint(json).indent(3)

pprint.pprint(json)