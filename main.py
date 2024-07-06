from modules.json import JsonLoad
from modules.GUI import Application


config = JsonLoad.__create_config__()

Application().mainloop()