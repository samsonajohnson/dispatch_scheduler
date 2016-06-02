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
import simbad_reader

class simulation:
    def __init__(self,config_file,base_directory='.'):
        self.base_directory = base_directory
        self.config_file = config_file
        self.dt_fmt = '%Y%m%dT%H:%M:%S'
        self.load_config()
        self.create_class_objects(tel_num=1)
        self.init_infofile(self.scheduler)
        self.current_time = self.starttime

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
            self.sitename = config['Setup']['SITENAME']
        except:
            print('ERROR accessing configuration file: ' + self.config_file)
            sys.exit()
    def create_class_objects(self,tel_num=1):
        # create a scheduler for the sim
        self.scheduler = scheduler.scheduler('scheduler.ini')

        # create the telescopes
        self.telescopes = []
        for ind in range(tel_num):
            self.telescopes.append(telescope.telescope('telescope.ini',ind+1))
                                   
    def init_infofile(self,sheduler):
        """
        a file that contains all the info for the simulation
        """
        self.sim_ind = self.get_sim_index()
        today_str = datetime.datetime.utcnow().strftime('%Y%m%d')
        self.sim_name = today_str+'.%05d'%self.sim_ind
        self.sim_path = './results/'+self.sim_name+'/'
        try: os.stat(self.sim_path)
        except: os.mkdir(self.sim_path)
        with open(self.sim_path+self.sim_name+'.txt','w') as wfile:
            wfile.write('DATE RUN: '+today_str+'\n')
            wfile.write('STARTTIME: '+self.starttime.strftime(self.dt_fmt))
            wfile.write('ENDTIME: '+self.endtime.strftime(self.dt_fmt))
        
    def get_sim_index(self):
        # see if there is a place to put the sim results, make one if not
        try:
            os.stat('./results')
        except:
            os.mkdir('./results')
        # get the index for the simulation
        files = glob.glob('./results/*')
        ind_number = len(files)+1
        return ind_number
    
    def check_tele_list(self,tele_list):
        if type(tele_list) is int:
            if (tele_list < 1) or (tele_list > len(self.telescopes)):
                tele_list = [x+1 for x in range(len(self.telescopes))]
            else:
                tele_list = [tele_list]
        tele_list = [x-1 for x in tele_list]
    
    def write_target_file(self,target):
        header = 'obs_start \t obs_end \t duration'
        with open(self.sim_path+target['name']+'.txt','w') as target_file:
            target_file.write(header+'\n\n')
    def calc_exptine(self,target):
        1./60. + exp_time*pow(10,(kappa/cos(M_PI/2-alt*M_PI/180)))/60.;
    def record_observation(self,target,telescopes):
        obs_start = self.current_time
        exptime = self.calc_exptime(target['exptime'])
        obs_end = self.current_time + exptime
        duration = (obs_end-obs_start).total_seconds()
        try: os.stat(self.sim_path+target['name']+'.txt')
        except: self.write_target_file(target)
        target_alt_az = self.scheduler.radectoaltaz(target)
        with open(self.sim_path+target['name']+'.txt','a') as target_file:
            obs_string = obs_start.strftime(self.dt_fmt)+'\t'+\
                obs_end.strftime(self.dt_fmt)#+'\t'+
            
        
            
            
        pass
        target_file = 3
                                   
                      

     
                       

if __name__ == '__main__':
    import ipdb
    tlist = simbad_reader.read_simbad('sample_list.txt')
    ipdb.set_trace()
    sc = scheduler.scheduler('scheduler.ini')
    s = simulation('simulation.ini')
    s.write_target_file(tlist[0])
    pass
