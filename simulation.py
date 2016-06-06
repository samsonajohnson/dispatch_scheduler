"""
The main framework for the dispatch scheduler simulation. 
"""
import scheduler
import telescope
import datetime
import math
import random
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
        self.update_time(self.starttime)

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
        
    def update_time(self,time):
        """
        A dinky function that can be used to update the time for all class 
        objects to make sure everything is in sync
        """
        self.time = time
        self.scheduler.time = time
        self.scheduler.obs.date=time
        
            
                                   
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
            wfile.write('STARTTIME: '+self.starttime.strftime(self.dt_fmt)+\
                            '\n')
            wfile.write('ENDTIME: '+self.endtime.strftime(self.dt_fmt)+\
                            '\n')
        
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
        header = 'obs_start \t obs_end \t duration \t altitude \t azimuth'
        with open(self.sim_path+target['name']+'.txt','w') as target_file:
            target_file.write(header+'\n\n')
    def calc_exptime(self,target):
        return target['exptime']

    def record_observation(self,target,telescopes=None):
        obs_start = self.time
        exptime = self.calc_exptime(target)
        obs_end = self.time + datetime.timedelta(minutes=exptime)
        duration = (obs_end-obs_start).total_seconds()
        try: os.stat(self.sim_path+target['name']+'.txt')
        except: self.write_target_file(target)
        self.scheduler.obs.date=self.time
        target['fixedbody'].compute(self.scheduler.obs)
        alt = target['fixedbody'].alt
        azm = target['fixedbody'].az
#        if target['fixedbody'].alt < 0:
#            ipdb.set_trace()
        with open(self.sim_path+target['name']+'.txt','a') as target_file:
            obs_string = obs_start.strftime(self.dt_fmt)+'\t'+\
                obs_end.strftime(self.dt_fmt)+'\t'+\
                '%.2f'%duration+'\t'+\
                '%.3f'%math.degrees(alt)+'\t'+\
                '%.3f'%math.degrees(azm)+'\t'+\
                '\n'         
            print(target['name']+': '+obs_string)
            target_file.write(obs_string)
        pass

    def record_target(self,target):
        self.scheduler.obs.horizon=str(self.scheduler.target_horizon)
        target['fixedbody'].compute(self.scheduler.obs)
        if  target['fixedbody'].neverup:
            return
        if  target['fixedbody'].circumpolar:
            return
        with open(self.sim_path+target['name']+'set.txt','a') as targetfile:
            tstime = self.scheduler.obs.next_setting(\
                target['fixedbody'],start=self.time).datetime()
            targetfile.write(tstime.strftime(self.dt_fmt+'\n'))
        with open(self.sim_path+target['name']+'rise.txt','a') as targetfile:
            trtime = self.scheduler.obs.next_rising(\
                target['fixedbody'],start=self.time).datetime()
            targetfile.write(trtime.strftime(self.dt_fmt+'\n'))

                      
    def record_sun(self):
        with open(self.sim_path+'sunset.txt','a') as sunfile:
            # the time the sunsets
            sstime = self.scheduler.nextsunset(sim.time)
            sunfile.write(sstime.strftime(self.dt_fmt+'\n'))
        with open(self.sim_path+'sunrise.txt','a') as sunfile:
            # the time the sunsets
            srtime = self.scheduler.nextsunrise(sim.time)
            sunfile.write(srtime.strftime(self.dt_fmt+'\n'))
            
     
                       

if __name__ == '__main__':
    import ipdb

#    ipdb.set_trace()
    # start off by making a simulation class
    sim = simulation('simulation.ini')
    ipdb.set_trace()
    random.shuffle(sim.scheduler.target_list)
    sim.scheduler.target_list=sim.scheduler.target_list[:40]
#    targetlist=simbad_reader.read_simbad('./secret/eta_list.txt')
#    for target in targetlist:
#        sim.write_target_file(target)
#    sim.update_time(datetime.datetime.utcnow())
    sim.scheduler.prep_night()
    # just a holder for last obs, two days prior to start to make irelevant
    for target in sim.scheduler.target_list:
        target['last_obs'] = sim.starttime-datetime.timedelta(days=2)
    sim.scheduler.calculate_weights()
    weights = []
    magvs = []
    i=1
    obs_count=0
    total_exp = 0
    setimes = []
    ipdb.set_trace()
    # while we are still in the simulation time frame
    while sim.time < sim.endtime:
        sim.update_time(sim.time)
        # if the current time is before the next sunset and the previous
        # sunrise is greater than the previous sunset, it is daytime
        if sim.time < sim.scheduler.nextsunset(sim.time) and\
                sim.scheduler.prevsunset(sim.time)<\
                sim.scheduler.prevsunrise(sim.time):
            # record the next sunrise and set times
            sim.record_sun()
            for target in sim.scheduler.target_list:
                sim.record_target(target)
            # change the current time to the time of sunset and add one second
            sim.time = sim.scheduler.nextsunset(sim.time)+\
                datetime.timedelta(seconds=1)
            sim.update_time(sim.time)
            sim.scheduler.prep_night()
            # end iteration
            continue
        # if the current time is before the next sunrise and the previous
        # sunset is greater than the previous sunrise, it is nighttime
        
        if sim.time < sim.scheduler.nextsunrise(sim.time) and \
                sim.scheduler.prevsunrise(sim.time)<\
                sim.scheduler.prevsunset(sim.time):
            # (re)calculate the weights, which also orders them by weight
            sim.scheduler.calculate_weights()
#            for target in sim.scheduler.target_list:
#                print target['weight']
#            ipdb.set_trace()
            for target in sim.scheduler.target_list:
                # if the top target is still less than zero, wait five minutes
                if target['weight']<0.:
                    sim.time+=datetime.timedelta(minutes=5)
                    break
                if sim.scheduler.is_observable(target):
                    total_exp += sim.calc_exptime(target)
                    target['observed']+=1
#                    if target['observed']>1:
#                        ipdb.set_trace()
                    target['last_obs']=sim.time
                    sim.record_observation(target)
                    obs_count+=1
#                    ipdb.set_trace()
                    sim.scheduler.is_observable(target)
                    sim.time+=datetime.timedelta(minutes=target['exptime'])
                    break
            sim.time+=datetime.timedelta(minutes=5)
    print obs_count
    ipdb.set_trace()
        
    pass
    # plan
    # if current time between last rising and next setting of sun
    #     change current time to next setting
    # if current time between last setting and next rising
    #     try: observe a star
    #     else: change time to next rising if we can't?
    # if out of simulation time frame
    #     end observation
        
    print 'Completed simulation '+sim.sim_name
