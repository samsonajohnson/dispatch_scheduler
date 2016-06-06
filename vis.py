"""
A collection of functions for plotting and visualization.
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import datetime
import ephem
import glob
import ipdb

def singletarget(sim,target):
    pass

def get_sun(simpath):
    dt_fmt = '%Y%m%dT%H:%M:%S'
    simname = simpath.split('/')[2]
    summ = np.genfromtxt(simpath+simname+'.txt',dtype=None,delimiter=': ')
    start = datetime.datetime.strptime(summ[1,1],dt_fmt)
    strrises = np.genfromtxt(simpath+'sunrise.txt',dtype=None)
    srises = [datetime.datetime.strptime(dstr,dt_fmt) for dstr in strrises]
    sr_days = []
    sr_times = []
    for srise in srises:
        sr_days.append((srise-start).days)
        ttime = srise.time()
        sr_times.append(ttime.hour+ttime.minute/60.+ttime.second/3600.)

    sr_days=np.array(sr_days)
    sr_times=np.array(sr_times)

    strsets = np.genfromtxt(simpath+'sunset.txt',dtype=None)
    ssets = [datetime.datetime.strptime(dstr,dt_fmt) for dstr in strsets]
    ss_days = []
    ss_times = []
    for sset in ssets:
        ss_days.append((sset-start).days)
        ttime = sset.time()
        ss_times.append(ttime.hour+ttime.minute/60.+ttime.second/3600.)
    ss_days=np.array(ss_days)
    ss_times=np.array(ss_times)
    return sr_days,sr_times,ss_days,ss_times

def get_targ_rise_set(simpath,targetname):
    dt_fmt = '%Y%m%dT%H:%M:%S'
    simname = simpath.split('/')[2]
    summ = np.genfromtxt(simpath+simname+'.txt',dtype=None,delimiter=': ')
    start = datetime.datetime.strptime(summ[1,1],dt_fmt)
    strrises = np.genfromtxt(simpath+targetname+'rise.txt',dtype=None)
    srises = [datetime.datetime.strptime(dstr,dt_fmt) for dstr in strrises]
    sr_days = []
    sr_times = []
    for srise in srises:
        sr_days.append((srise-start).days)
        ttime = srise.time()
        sr_times.append(ttime.hour+ttime.minute/60.+ttime.second/3600.)

    sr_days=np.array(sr_days).astype(float)
    sr_times=np.array(sr_times)

    strsets = np.genfromtxt(simpath+targetname+'set.txt',dtype=None)
    ssets = [datetime.datetime.strptime(dstr,dt_fmt) for dstr in strsets]
    ss_days = []
    ss_times = []
    for sset in ssets:
        ss_days.append((sset-start).days)
        ttime = sset.time()
        ss_times.append(ttime.hour+ttime.minute/60.+ttime.second/3600.)
    ss_days=np.array(ss_days).astype(float)
    ss_times=np.array(ss_times)
    return sr_days,sr_times,ss_days,ss_times

def get_target(simpath,targetname):

    dt_fmt = '%Y%m%dT%H:%M:%S'
    simname = simpath.split('/')[2]
    summ = np.genfromtxt(simpath+simname+'.txt',dtype=None,delimiter=': ')
    start = datetime.datetime.strptime(summ[1,1],dt_fmt)
    temp = np.genfromtxt(simpath+targetname+'.txt',names=True,dtype=None)
    start = datetime.datetime.strptime(summ[1,1],dt_fmt)
    obs = [datetime.datetime.strptime(dstr,dt_fmt) \
               for dstr in temp['obs_start']]
#    ipdb.set_trace()
    alts = temp['altitude']
    days = []
    times = []
    for obser in obs:
        days.append((obser-start).days)
        ttime = obser.time()
        times.append(ttime.hour+ttime.minute/60.+ttime.second/3600.)    

    days = np.array(days)
    times = np.array(times)
    return days,times,alts


if __name__ == '__main__':
#    ipdb.set_trace()
    simnumber = raw_input('Enter sim number: ')
    simpath = './results/20160606.'+simnumber+'/'
    targetname = 'HD95128'


    sr_days,sr_times,ss_days,ss_times = get_sun(simpath)
    while True:
        targetname = raw_input('Enter target name: ')
        try:
            days,times,alts = get_target(simpath,targetname)
        except:
            print('Bad name?')
            continue

        plt.plot(sr_days,sr_times,label='sun rises')
        plt.plot(ss_days,ss_times,label='sun sets')

        try:
            tr_days,tr_times,ts_days,ts_times=\
                get_targ_rise_set(simpath,targetname)
            tr_discont = np.where(np.abs(np.diff(tr_times)) >= 0.5)[0]+1
            tr_days = np.insert(tr_days, tr_discont, np.nan)
            tr_times = np.insert(tr_times, tr_discont, np.nan)
            
            ts_discont = np.where(np.abs(np.diff(ts_times)) >= 0.5)[0]+1
            ts_days = np.insert(ts_days, ts_discont, np.nan)
            ts_times = np.insert(ts_times, ts_discont, np.nan)
        
            plt.plot(tr_days,tr_times,label='target rises',ms=2)
            plt.plot(ts_days,ts_times,label='target sets',ms=2)
        except:
            print('No rise/set data for target?')
        # save plotting the obs for last for cleanliness in legend
        plt.plot(days,times,'.',label='obs')
        plt.legend()
        plt.show()
        plt.plot(days,alts,'.')
        plt.show()
    ipdb.set_trace()
    ipdb.set_trace()
        
        