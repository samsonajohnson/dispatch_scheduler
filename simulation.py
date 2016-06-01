"""
The main framework for the dispatch scheduler simulation. 
"""
import scheduler
import telescope
import datetime
from configobj import ConfigObj

class simulation:
    def __init__(self,config_file,base_directory='.'):
        self.base_directory = base_directory
        self.config_file = config_file
        self.load_config()
        self.dt_fmt = '%Y%m%dT%H%M%S'
    def load_config(self):
        
        try:
            config = ConfigObj(self.base_directory+'/config/'+self.config_file)
            self.starttime = datetime.strptime(config['Setup']['STARTTIME'],\
                                                   self.dt_fmt)
            self.endtime = datetime.strptime(config['Setup']['ENDTIME'],\
                                                 self.dt_fmt)
            self.latitude = config['Setup']['LATITUDE']
            self.longitude = config['Setup']['LONGITUDE']
            self.elevation = float(config['Setup']['ELEVATION'])
            self.logger_name = config['Setup']['LOGNAME']
        except:
            print('ERROR accessing configuration file: ' + self.config_file)
            sys.exit()



if __name__ == '__main__':
    pass
