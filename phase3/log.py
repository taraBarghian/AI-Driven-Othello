import logging
from datetime import datetime

def setup_custom_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger

class logfile:
    def __init__(self, filename):
        self.filename=filename

    def log_gene(self,txt,nextline=True , time=True):
        self.f = open(self.filename, "a")
        if nextline :
            if time:
                 self.f.write("\n{0} -- {1}".format(datetime.now().strftime("%Y-%m-%d %H:%M"), txt))
            else:
                self.f.write(txt)
        else:
            self.f.write( txt + " - ")
        self.f.close()

