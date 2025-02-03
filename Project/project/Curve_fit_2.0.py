#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 11:51:20 2025

@author: francescaravelli
"""

import pandas as pd

import numpy as np

import matplotlib.pyplot as plt

from scipy.optimize import curve_fit

#import pymc3 as pm

# Read the CSV file

#log scale data before fitting


    
def visualize_data(file_path):

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
            popt, pcov = curve_fit(func, time, y, p0=(y.iloc[0], 0.1))
            # Extract fitted parameters
        
            a, b = popt
    
            # Generate fitted values
            
            fitted_host = func(time, a, b)
        
            return a, b, fitted_host

        # Plot the data and the fitted model

     
        def subplot(m, ax, time, y, fitted_host, y0, b, title,):        
            
            ax.scatter(time, y, alpha=0.7, edgecolors='w', s=100, label='Data')
        
            ax.plot(time, fitted_host, color='red', linewidth=2, label=f'Fit: y0={y0:.2f}, b={b:.4f}')
            
            ax.set_xlabel('Time', fontsize=14)
            
            if m>0:
                ax.set_yscale('log')  # Log scale for y-axis
            
            ax.set_ylabel('Host', fontsize=14)
            
            ax.legend(fontsize=12)
            ax.set_title(title, fontsize=16)
            
            ax.grid(True, linestyle='--', alpha=0.6)
        
        a, b, fitted_host=fitting(line_fit, time, loghost)
        y0, r, fitted_host_2=fitting(exponential_growth,data['time'], data['host'])
    
        
        fig, ax = plt.subplots(1, 2, figsize=(12, 5))  
        subplot(0, ax[0], time, loghost, fitted_host, a, b, title="Log Scale Data Before Fitting")
        subplot(0, ax[1], time, data['host'], fitted_host_2, y0, r, title="Log Scale Data After Fitting")
        
        plt.tight_layout()
        plt.show()
        
        
    
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        
    except ValueError as ve:
        print(f"Error: {ve}")
        
visualize_data('../data/phaeocystis_control.csv')
visualize_data('../data/phaeocystis_PgV_one_step.csv')
