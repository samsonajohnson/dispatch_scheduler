"""
The main framework for the dispatch scheduler simulation. 
"""
import scheduler
import telescope
import datetime
import sys
import os
import glob
from configobj import ConfigObj

class simulation:
    def __init__(self,config_file,base_directory='.'):
        self.base_directory = base_directory
        self.config_file = config_file
        self.dt_fmt = '%Y%m%dT%H:%M:%S'
        self.load_config()

    def load_config(self):
        
        try:
            config = ConfigObj(self.base_directory+'/config/'+self.config_file)
            self.starttime = datetime.datetime.strptime(\
                config['Setup']['STARTTIME'],self.dt_fmt)
            self.endtime = datetime.datetime.strptime(\
                config['Setup']['ENDTIME'],self.dt_fmt)
            self.latitude = config['Setup']['LATITUDE']
            self.longitude = config['Setup']['LONGITUDE']
            self.elevation = float(config['Setup']['ELEVATION'])
            self.logger_name = config['Setup']['LOGNAME']
        except:
            print('ERROR accessing configuration file: ' + self.config_file)
            sys.exit()

    def write_infofile(self,sheduler):
        """
        a file that contains all the info for the simulation
        """
        self.sim_ind = self.get_sim_index()
        today_str = datetime.datetime.utcnow().strftime('%Y%m%d')
        self.sim_name = today_str+'.%05d'%self.sim_ind
        with open(self.sim_name+'.txt') as wfile:
            wfile.write('DATE RUN: '+today_str+'\n')
            wfile.write('STARTTIME: '+self.starttime.strftime(self.dt_fmt)
            wfile.write('ENDTIME: '+self.endtime.strftime(self.dt_fmt)
        
    def get_sim_index(self):
        # see if there is a place to put the sim results, make one if not
        try:
            os.stat('./simulation_results')
        except:
            os.mkdir('./simulation_results')
        # get the index for the simulation
        files = glob.glob('./simulation_results/*')
        ind_number = len(files)+1
        return ind_number

if __name__ == '__main__':
    import ipdb
    ipdb.set_trace()
    sc = scheduler.scheduler('scheduler.ini')
    s = simulation('simulation.ini')
    s.write_infofile(sc)
    pass
