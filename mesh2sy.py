import pyglass
import os
import sys
import glob
import time
import code
import subprocess
import ntpath
import shutil
from distutils.dir_util import copy_tree

def checkForNewMeshes(oldListMeshes):
	cwd = os.getcwd()
	l = glob.glob(os.getcwd() + "\\meshes\\*")
	for each in l:
		if os.path.isdir(each) and each not in oldListMeshes:
			print("Found new data set: " + each )
			a = convertMeshes(each)
			oldListMeshes.append(each)
	return oldListMeshes
	
def copyEmpty(name):
	emptyProject = "emptyProject/emptyProject.syg"
	emptyProjectMeta = "emptyProject/emptyProject.sym"
	if not os.path.exists("output/" + name):
		os.mkdir("output/" + name)
	shutil.copy(emptyProject, "output/" + name + "/" + name + ".syg")
	shutil.copy(emptyProjectMeta, "output/" + name + "/" + name + ".sym")

def convertMeshes(path):
	name = ntpath.basename(path)
	copyEmpty(name)
	projectPath = os.path.join(os.getcwd(), "output\\" + name + "\\" + name + ".syg")
	print(projectPath)
	project = pyglass.OpenProject(pyglass.path(projectPath))
	l = glob.glob(path + "\\*.obj")
	project.ImportMeshOBJs("default", "\n".join(l))
	while project.GetMeshIOPercentage() != 100:
		print("Progress: " + str(project.GetMeshIOPercentage()) + "%")
		print("Current mesh: "  + project.GetMeshIOName() + "\n")
		time.sleep(2)
	vl = pyglass.VolumeLibrary()
	vl.ReloadLibrary()
	entry = vl.CreateEntryFromPath(projectPath, name)
	vl.PutEntry(entry)
	project.RandomizeMeshColors()
	
def importProject(projectPath):
	vl = pyglass.VolumeLibrary()
	vl.ReloadLibrary()
	entry = vl.GetEntryFromPath(projectPath)
	vl.PutEntry(entry)
	
def main():
	if not os.path.exists("output"):
		os.mkdir("output")
	if not os.path.exists("meshes"):
		os.mkdir("meshes")
	oldListMeshes = []#glob.glob(os.getcwd() + "\\meshes\\*")
	while True:
		print("Sleeping for a minute.")
		time.sleep(1) 
		print("Checking for new meshes files.")
		oldListMeshes = checkForNewMeshes(oldListMeshes)
		
		



if __name__ == "__main__": main()