#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 11:01:46 2018

@author: Suyong Choi (Department of Physics, Korea University suyong@korea.ac.kr)

This script applies nanoaod processing to one file
"""

import sys
import cppyy
import ROOT

from importlib import import_module
from argparse import ArgumentParser

if __name__=='__main__':
    parser = ArgumentParser(usage="%prog inputfile outputfile jobconfmod")
    parser.add_argument("infile")
    parser.add_argument("outfile")
    parser.add_argument("jobconfmod")
    args = parser.parse_args()
    infile = args.infile
    outfile = args.outfile
    jobconfmod = args.jobconfmod

    # load job configuration python module and get bjects
    mod = import_module(jobconfmod)
    config = getattr(mod, 'config')
    procflags = getattr(mod, 'procflags')
    print(config)

    intreename = "outputTree2"
    outtreename = "outputTree3"
    saveallbranches = 0


    # load compiled C++ library into ROOT/python
    cppyy.load_reflection_info("libcorrectionlib.so")
    cppyy.load_reflection_info("libMathMore.so")
    cppyy.load_reflection_info("libnanoadrdframe.so")
    t = ROOT.TChain(intreename)
    t.Add(infile)
    print("Inside process one file..!!")

    #aproc = ROOT.FourtopAnalyzer(t, outfile)
    aproc = ROOT.TTZAnalyser(t, outfile)
    aproc.setParams(config['year'], config['runtype'],config['datatype'])

    #aproc.setParams(config[year])
    # setup JSONS for corrections
    #aproc.setupCorrections(config['goodjson'], config['pileupfname'], config['pileuptag']\
    #    , config['btvfname'], config['btvtype'], config['jercfname'], config['jerctag'], config['jercunctag'])
    # prepare for processing

    aproc.defineCuts()
    #aproc.defineMoreVars()
    aproc.bookHists()
    aproc.setupCuts_and_Hists()
    aproc.setupTree()
    aproc.run(saveallbranches, outtreename)
