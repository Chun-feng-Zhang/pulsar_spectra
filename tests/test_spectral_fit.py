#! /usr/bin/env python
"""
Tests the spectral_fit.py script
"""
import os
import numpy as np
from numpy.testing import assert_almost_equal
import csv

from pulsar_spectra import catalogues
from pulsar_spectra.spectral_fit import find_best_spectral_fit
from pulsar_spectra.catalogues import collect_catalogue_fluxes

import logging
logger = logging.getLogger(__name__)


def test_find_best_spectral_fit():
    """Tests the find_best_spectral_fit funtion.
    """
    cat_dict, cat_list = collect_catalogue_fluxes()
    #print(cat_dict)
    #pulsars = ['J0034-0534','J0953+0755', 'J1645-0317']
    pulsars = ['J0820-1350', 'J0835-4510', 'J0837+0610', 'J0953+0755', 'J1453-6413', 'J1456-6843', 'J1645-0317', 'J1731-4744']
    for pulsar in pulsars:
        print(f"\nFitting {pulsar}")
        #print(cat_dict[pulsar])
        #print(cat_list[pulsar])
        freq_all = np.array(cat_list[pulsar][0])*1e6
        flux_all = np.array(cat_list[pulsar][1])*1e-3
        flux_err_all = np.array(cat_list[pulsar][2])*1e-3
        #print(freq_all, flux_all, flux_err_all)
        models, fit_results = find_best_spectral_fit(pulsar, freq_all, flux_all, flux_err_all, plot_compare=True, data_dict=cat_dict[pulsar])
        print(models)

def test_compare_fits_to_Jankowski_2018():
    # Get the pulsars in the Jankowski paper
    jank_pulsar_dict = {}
    with open("{}/test_data/best_model_for_Jankowski_2018.tsv".format(os.path.dirname(os.path.realpath(__file__))), "r") as file:
        tsv_file = csv.reader(file, delimiter="\t")
        lines = []
        for li, line in enumerate(tsv_file):
            if li < 38:
                continue
            pulsar = line[0].strip().replace("–", "-")
            if line[1] == "":
                jank_pulsar_dict[pulsar] = "no_fit"
            elif line[1] == "pl":
                jank_pulsar_dict[pulsar] = "simple_power_law"
            elif line[1] == "broken pl":
                jank_pulsar_dict[pulsar] = "broken_power_law"
            elif line[1] == "lps":
                jank_pulsar_dict[pulsar] = "log_parabolic_spectrum "
            elif line[1] == "hard cut-off":
                jank_pulsar_dict[pulsar] = "high_frequency_cut_off_power_law"
            elif line[1] == "low turn-over":
                jank_pulsar_dict[pulsar] = "low_frequency_turn_over_power_law"
            else:
                print("Not found", line[1])
                exit()

    # Fit all the pulsars
    wrong_count = 0
    cat_dict, cat_list = collect_catalogue_fluxes()
    print(cat_list.keys())
    for pulsar in jank_pulsar_dict.keys():
        if pulsar in cat_list.keys():
            freq_all = np.array(cat_list[pulsar][0])*1e6
            flux_all = np.array(cat_list[pulsar][1])*1e-3
            flux_err_all = np.array(cat_list[pulsar][2])*1e-3
            #print(freq_all, flux_all, flux_err_all)
            models, fit_results = find_best_spectral_fit(pulsar, freq_all, flux_all, flux_err_all, plot=False, data_dict=cat_dict[pulsar])
        else:
            models = [None, "no_fit"]
        print(f"{pulsar} {models[1]} {jank_pulsar_dict[pulsar]}")
        if models[1] != jank_pulsar_dict[pulsar]:
            print(models[1], jank_pulsar_dict[pulsar])
            wrong_count += 1
            #raise AssertionError()
    print(f"wrong_count: {wrong_count}")

if __name__ == "__main__":
    """
    Tests the relevant functions in spectral_fit.py
    """
    # introspect and run all the functions starting with 'test'
    for f in dir():
        if f.startswith('test'):
            print(f)
            globals()[f]()