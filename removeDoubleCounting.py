#!/usr/bin/env python3
import ROOT
import sys
import os


sep='-'*15

if len( sys.argv )!=2:
    print("USAGE : % s < input file >"%(sys.argv[0]))
    sys.exit(1)

inFileName = sys.argv[1]

while not os.path.exists(inFileName):
    print('File not found')
    inFileName = input('Enter file name: ')


print("Processing", inFileName)

inFile = ROOT.TFile.Open(inFileName)
tree=inFile.Get("outputTree2")
outfile = ROOT.TFile.Open(inFileName, "UPDATE")
newtree=tree.CloneTree(0)

EventID = []
print("Processing ", tree.GetEntries(), " events")
print(sep)
print("Getting all the entries")
print(sep)
for i in range(tree.GetEntries()):
    try:
        tree.GetEntry(i)
    except:
        print("Error with entry", i, ". Quitting...")
        sys.exit(1)
    # For every entries, get the identification triplet [run,lumiblock,eventid], and associate it with the event number i in the file
    EventID.append([getattr(tree,"run"),getattr(tree,"luminosityBlock"), getattr(tree,"event"),i])
print("Sorting")
print(sep)
# Sort event by run, then lumiblock, then eventid
EventID.sort()
PosToRemove = [0] * tree.GetEntries() # 0 and 1, if 1 then remove
print("Finding the double events")
print(sep)
for i in range(len(EventID)-1):
    # Compare the triplet for event i and i+1 (and verify if the events number are not the same, don't really remember what's the use but it's just being too precocious)
    # Since they are sorted, only look to the neighbourhood
    if EventID[i][0]==EventID[i+1][0] and EventID[i][1]==EventID[i+1][1] and EventID[i][2]==EventID[i+1][2] and EventID[i][3]!=EventID[i+1][3]:
        # If they are the same, only remove the second one
        PosToRemove[EventID[i+1][3]]=1
print("Removing them")
print(sep)
nbDouble=0.0
for i in range(len(PosToRemove)):
    tree.GetEntry(i)
    if PosToRemove[i]==0:
        newtree.Fill()
        #Write them into the new file, or nothing if it is possible to remove the oders directly
    else:
        nbDouble+=1.0

print("Double counted : ", int(nbDouble))
print("Percentage : ", round(nbDouble/tree.GetEntries()*100,2), "%")
print("Writting new tree")
print(sep)
newtree.Write("outputTree2", ROOT.TObject.kOverwrite)
print("Done")
print(sep)
print(sep*2)
print(sep)
