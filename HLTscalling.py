#!/usr/bin/env python3
import ROOT
import os
import sys
from tqdm import tqdm
import warnings

warnings.filterwarnings('ignore', category=RuntimeWarning)

def removeBranch(filename, branchnames,letter):
    infile = ROOT.TFile(filename, "READ")
    intree = infile.Get("outputTree2")
    
    try:
        nentries = intree.GetEntries()
    except:
        print(filename + ' does not have a tree')
        return
    if nentries == 0:
        # May need to copy the file to make drawhist.py work
        print('We have 0 entry. Coping file as it is')
        infile.Close()
        os.system('cp '+filename+' '+filename[:-5]+letter+filename[-5:])
        return

    for branchname in branchnames:
        intree.SetBranchStatus(branchname, 0)

    
    outfile = ROOT.TFile.Open(filename[:-5]+letter+filename[-5:], "RECREATE")
    outtree = intree.CopyTree("")
    outfile.Write()
    outfile.Close()
    infile.Close()

def renameHisto(filename):
    file = ROOT.TFile(filename, "update")
    l=filename[-6]
    if(l=='B' or l=='C' or l=='D'):
        r=filename[-8:-6]
        list=file.GetListOfKeys().Clone()
        for obj in list:
            if obj.GetClassName() == "TH1D":
                hist=obj.ReadObj()
                inname=hist.GetName()
                #We rename the histo as they were in the original file. We just add the cut but not for nocut
                if (not inname.endswith('nocut')):
                    outname=inname+r
                    outhist=hist.Clone(outname)
                    file.Delete(obj.GetName())
                    hist.Delete()
                    file.WriteTObject(outhist, outname)
                    print("new name is "+outname)
        list=None
        file.Write()
    file.Close()    

def checkHisto(filename):
    file = ROOT.TFile(filename, "read")
    list=file.GetListOfKeys().Clone()
    for obj in list:
        if obj.GetClassName() == "TH1D":
            hist=obj.ReadObj()
            inname=hist.GetName()
            print(inname)
    list=None
    file.Close()  


HLT2017B=['HLT_Ele115_CaloIdVT_GsfTrkIdT', 'HLT_IsoMu30','HLT_Ele32_WPTight_Gsf', 'HLT_Mu19_TrkIsoVVL_Mu9_TrkIsoVVL_DZ_Mass3p8', 'HLT_Mu55', 'HLT_TripleMu_5_3_3_Mass3p8to60_DZ']
HLT2017C=['HLT_IsoMu30','HLT_Ele32_WPTight_Gsf', 'HLT_Mu19_TrkIsoVVL_Mu9_TrkIsoVVL_DZ_Mass3p8', 'HLT_Mu55', 'HLT_TripleMu_5_3_3_Mass3p8to60_DZ']
HLT2017D=['HLT_TripleMu_5_3_3_Mass3p8to60_DZ']
HLT = {'B': HLT2017B, 'C': HLT2017C, 'D':HLT2017D}

#directory = 'analyzed'

# files = os.listdir(directory)

# filenames = [f for f in files if f.endswith('.root') and not f.startswith('Data')]

# for filename in tqdm(filenames):
#     filename=os.path.join(directory,filename)

filename=sys.argv[1]
print(filename)
for letter in ['B', 'C', 'D']:
    removeBranch(filename, HLT[letter], letter)
    newname=filename[:-5]+letter+filename[-5:]
    os.system('./processHLT.py '+newname+' '+newname+'new jobconfiganalysis >> outputHLT.txt && mv '+newname+'new '+newname)
    renameHisto(newname)