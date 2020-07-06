#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 6 13:58:00 2020

@author: Lchuang

last update: 07/06/2020

"""
import os
from os import path
from obspy import read
import glob
import json

def creat_mseed_from_daily_sac(input_dir='sac_file',
                               stations_json= "station_list.json",
                               output_dir="msee_file"):
    """

        To convert daily based SAC files to station based mseed format

        Parameters
        ----------
        input_dir: str
            Directory name containing daily based SAC files
        stations_json: str
            Path to a JSON file containing station information.
        output_dir: str
            Output directory that will be generated.
    """

    # ---- check if directories and files exist
    if not path.exists(input_dir): # check input directory
        raise FileExistsError(f'Input directory {input_dir} not exists')
    if not path.exists(output_dir): # check output directory
        print(f'Create output directory {output_dir}')
    if not path.exists(stations_json):
        raise FileExistsError(f'file {stations_json} not found')
    else:
        with open(stations_json) as f:
            stations = json.load(f)

    # ---- match sac files and convert them to mseed files
    # ---- loop over list of station
    for station, meta in stations.items():

        # ---- check and/or create output directories for each station
        output_dir_per_station = f'{output_dir}/{station}'
        if not path.exists(output_dir_per_station):
            print(f'create directory {output_dir_per_station}')
            os.makedirs(output_dir_per_station)
        else:
            print(f'{output_dir_per_station} exists, writing mimiseed files')

        # ---- loop over channels
        network = meta["network"]
        for channel in meta["channels"]:
            # ---- search sac files recursively in the input folder
            all_sac_files = glob.glob(f'{input_dir}/**/*.{station}.{channel}.SAC', recursive=True)
            # ---- convert files to miniseed files
            for single_sac_file in all_sac_files:
                st = read(single_sac_file)
                btime = str(st[0].stats.starttime.datetime)
                etime = str(st[0].stats.starttime.endtime)
                mseed_file_name = f'{network}.{station}.{channel}__{btime}__{etime}.mseed'
                st.write(mseed_file_name)