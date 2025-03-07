#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 11:52:49 2025

@author: francescaravelli
"""

import pandas as pd

import numpy as np

from scipy.optimize import curve_fit

#import pymc3 as pm 

# Read the CSV file

#log scale data before fitting


    
def res_sum(file_path):

    try:

        # Load data
        data = pd.read_csv(file_path)
        
        # Check if required columns exist   
        if 'time' not in data.columns or 'host' not in data.columns: 
            raise ValueError("The CSV file must contain 'time' and 'host' columns.")

        # Define the exponential growth model
        
        
        def log_data(file_path):
            time=data['time']
            log_y=np.log(data['host'])
            return time, log_y
        
        time, loghost=log_data(file_path)
        
        def line_fit (t, a, b):
            return a+b*t
       
        def exponential_growth(t, y0, r):
            return y0 * np.exp(r * t)
        
        def fitting(func, time, y):

            # Fit the model to the data
            popt, pcov = curve_fit(func, time, y)
            # Extract fitted parameters
        
            a, b = popt
    
            # Generate fitted values
            
            fitted_host = func(time, a, b)
        
            return a, b, fitted_host
        
        a, b, linefitted_host = fitting(line_fit, time, loghost)
        y0, r, expfitted_host = fitting(exponential_growth, data['time'], data['host'])
        
        time = data["time"]
        actual_y = list(data['host'])
        
        residuals_linear = []
        residuals_exp = []
        
        for i in range(len(time)):
            t = time[i]  # Keep `time` unchanged
            data_y = actual_y[i]
            predicted_linear = line_fit(t, a, b)  # Use `t`, not `time`
            predicted_exp = exponential_growth(t, y0, r)
            
            residuals_linear.append(data_y - predicted_linear)
            residuals_exp.append(data_y - predicted_exp)

        print(residuals_linear)
        print(residuals_exp)
        
        
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        
    except ValueError as ve:
        print(f"Error: {ve}")

       
        
    
        
res_sum('../data/phaeocystis_control.csv')







