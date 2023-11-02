import os

from webdriver_manager.chrome import ChromeDriverManager


chrome_driver_path = ChromeDriverManager().install()

if not os.path.isdir('./paths/'):
    os.mkdir('./paths/')

with open('./paths/chrome_driver_path.txt', 'wt') as file:
    file.write(chrome_driver_path)
