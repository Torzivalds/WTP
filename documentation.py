import config
import os
from color import c

def mini():
	# Affiche une mini doc (help)
	print("Web Transfer Protocol	V"+str(config.readConfFile("Version")))
	print("Here are the main functions:")
	print("update		Check for updates")
	print("stats 		Shows your peer statistics")
	print("config 		Edit the configuration")
	print("exit 		Stop WTP")
	print("dns 		Edit the VPN configuration")
	print("doc 		How to use wtp")
	print("checkFiles 	Check the ADDFILES and HOSTEDFILES")
	print("delAll 		Delete all : Config, DB, Files.")
	print("majDNS		Update the DNS database")
	print("client 		Use WTP in console")
	print("blacklist 	Edit the BlackList configuration")
	print("For more informations, enter doc")

def maxi():
	# Affiche la grande documentation interactive (doc)
	print("Welcome to the WTP documentation.")
	print(str(c("highlighted"))+"1. Basics"+str(c("")))
	print("To be able to use WTP from your browser, you need to install the browser extension. Link : "+str(c("underline"))+"https://github.com/Torzivalds/WTP/tree/master/Extention%20Firefox"+str(c(""))+"  A configuration wizard is included.\n")
	print("To add files to the network, you must go to the file named ADDFILES and copy / paste them. Path : "+str(os.getcwd())+"/ADDFILES  WTP will automatically add them. \n"+str(c("bold"))+"Pro tip : WTP checks this folder every 5 minutes. If you are in a hurry, you can enter this request : checkFiles."+str(c(""))+" \n"+str(c("red"))+"DISCLAMER : A file can not be deleted from the network. Be careful when you add some."+str(c("")))
	print("For more information on the possible commands here, enter the name of the command below.\n")
	print(str(c("highlighted"))+"2. Advenced"+str(c("")))
	print("You found a bug or improvement ? Contact us on our website :\n"+str(c("underline"))+"https://myrasp.fr/WTP"+str(c("")))
	print("Developer ressources are in the Wiki part of our GitHub.\n"+str(c("underline"))+"https://github.com/Torzivalds/WTP/wiki"+str(c("")))
	print(str(c("highlighted"))+"3. Contribute"+str(c("")))
	print("You can contribute by improving the code with us, by talking about Web Transfer Protocol to your friends, your family, your colleagues, and if you can not contribute in these ways, you can donate via PayPal.\nYour contributions make us happy and help us to move forward, thank you!\n")
	print(str(c("highlighted"))+"4. External ressources"+str(c("")))
	print("GitHub : "+str(c("underline"))+"https://github.com/Torzivalds/WTP"+str(c(""))+"\nPayPal : "+str(c("underline"))+"https://paypal.me/torzivalds"+str(c(""))+"\nWebsite : "+str(c("underline"))+"https://myrasp.fr/WTP"+str(c(""))+"\nFirefox Extension : "+str(c("underline"))+"https://github.com/Torzivalds/WTP/tree/master/Extention%20Firefox"+str(c("")))
	while 1:
		print(str(c("bold"))+"Enter an order, press enter or enter exit"+str(c("")))
		cmd = str(input(str(c("highlighted"))+">> "))
		print(str(c(""))+"", end="")
		if cmd == "exit":
			break
		elif cmd == "update":
			print("This function allows you to update the source code of WTP, which allows you to add new features and fix bugs. A check is made every 24 hours, and the update is installed as soon as it is detected.")
			print(str(c("yellow"))+"A restart may be required"+str(c("")))
		elif cmd == "stats":
			print("This command allows to know some statistics of his peer, which allows to have some information about the use of peer by the network. They are for informational purposes only, they are not necessarily exact, because it is very easy to modify them via the database (WTP.db which is a SQlite database)")
		elif cmd == "config":
			print("This function allows you to modify the wtp.conf configuration file, accessible via this path : "+str(os.getcwd())+"/wtp.conf")
			print("You can also edit it with your favorite text editor.")
			print(str(c("bold"))+"Think after changing settings to restart WTP for these to take effect."+str(c("")))
		elif cmd == "dns":
			print("The DNS is a system for replacing the names of files that are very long with domain names that are much shorter and easier to remember.\nThis command is used to access a program that allows you to add, modify and delete DNS entries. You can do this on your peer (127.0.0.1) or on a remote peer. So you can add your own domain name, for free and very easily.\n"+str(c("yellow"))+"Be careful, when you add a new domain name, manually check that it does not already exist!"+str(c("")))
		elif cmd == "vpn":
			print("This section is being created.")
		elif cmd == "wtp":
			print("Web Transfer Protocol	V"+str(config.readConfFile("Version")))
			print("WTP is a new peer to peer network for the web under the GPL v3 lisence coded by a student on his free time.")
			print("This version is not stable. WTP is being created, it's taking  time.  You can contribute by improving the code with us, by talking about Web Transfer Protocol to your friends, your family, your colleagues, and if you can not contribute in these ways, you can donate via PayPal.Your contributions make us happy and help us to move forward, thank you!")
		elif cmd == "license":
			print("WTP is free software, and is under GPL v3 license.This means that you can use, share, modify, redistribute as much as you want WTP. For more information, you can consult the license on the official GNU website :")
			print(str(c("underline"))+"https://www.gnu.org/licenses/gpl.html"+str(c("")))
		elif cmd == "blacklist":
			print("The blacklist is a system to block the files you want, such as advertisements and explicit documents. You can add or delete files from this list locally, and you can also use the list of a remote peer. This command allows you to modify the BlackList easily.")
		elif cmd[:6] == "client":
			print(str(c("yellow"))+"This command is used to send orders by hand to other peers or yours (IP: 127.0.0.1). Most users should not use this command, but it may be useful in some cases."+str(c("")))
			cmd = cmd[7:]
			if cmd == "DemandePresence":
				print("This command verifies that a peer is still connected to the network. It is done automatically every day. If the peer does not respond, it is moved into a sort of quarantine in the database, and after 10 days, it is permanently deleted.")
			elif cmd == "DemandeNoeud":
				print("This command requests 48 peers IP addresses from the network to a known peer to add them to the database. If you want to receive all the peers in the remote peer's database, prefer to use =cmd DemandeListeNoeuds")
			elif cmd == "DemandeFichier":
				print("This command is used to download a file. Takes into parameters the ip and the port of the peer, and the name of the file which one wishes to download. If you do not know which peer is hosting the file, use =cmd rechercher")
			elif cmd == "DemandeListeNoeuds":
				print("This command allows to receive all the peers known by another peer. \n"+str(c("yellow"))+"It can be very long if the peer knows a lot of peers."+str(c(""))+"\nIf you want to know only a few peers (48 to be precise), use =cmd DemandeNoeud")
			elif cmd == "DemandeListeFichiers":
				print("This command asks a peer for a list of all the files it hosts. The received list is processed and the files are added to the database. \n"+str(c("yellow"))+"Attention, this action could take time if the peer hosts a lot of files."+str(c("")))
			elif cmd == "rechercher":
				print("This function is used to search for a file on the network. It takes as parameter a domain name, or the exact name of the file. If it finds one of the file locations on the network, it is downloaded.")
			else:
				print(str(c("red"))+"Unknown command."+str(c(""))+" Enter client then :")
				print("DemandePresence		DemandeNoeud		DemandeFichier")
				print("DemandeListeNoeuds	DemandeListeFichiers	rechercher")
		elif cmd == "majDNS":
			print("This command makes it easy to update your peer's DNS entries with a trusted remote peer "+str(c("yellow"))+"(Beware of phishing)"+str(c(""))+". The DNS is a system for replacing the names of files that are very long with domain names that are much shorter and easier to remember.")
		elif cmd == "delAll":
			print(str(c("yellow"))+"This function deletes all settings, all files, the entire WTP database. It's irreversible."+str(c("")))
			print("To be precise, it removes the following folders : .TEMP, ADDFILES, HOSTEDFILES, and the folloing files : .TempMaintenance24H, .TempMaintenance5M, logs, wtp.conf and the database : WTP.db")
		elif cmd == "checkFiles":
			print("This command is used to check if there are new files in ADDFILES. If so, they will be added to the most deleted network from this folder. This command also makes it possible to check that all the files in HOSTEDFILES are well known, otherwise they are sent to ADDFILES so that they are added to the network. And finally, this removes all the old temporary files in .TEMP")
		elif cmd == "folder tree":
			print("WTP is on this path : "+str(os.getcwd()))
			print("In there, you can find :")
			print("WTP source files that allow it to work. If you modify or delete it, WTP will not work properly.")
			print(str(c("bold")+".TEMP"+str(c(""))))
			print("This folder contains a number of small temporary files. Normally, they are very quickly removed.")
			print(str(c("yellow"))+"If you delete the folder or files inside, WTP may not be doing what it is doing or even crashing."+str(c("")))
			print(str(c("bold")+"ADDFILES"+str(c(""))))
			print("This is a folder for you! This is the folder in which you can put all the files you want. After a few minutes, they will be available on the network. If you do not want to wait, you can start the checkFiles command. \n"+str(c("bold"))+"Once the files on the network, they are deleted from this folder. Remember to save them elsewhere! Attention, so that the files are sent on the network, they must not be in a subfolder of ADDFILES, otherwise they will be removed."+str(c(""))+" \n"+str(c("red"))+"Once a file is on the network, no one can delete it. Pay attention !"+str(c("")))
			print(str(c("bold")+"HOSTEDFILES"+str(c(""))))
			print("This folder contains all the files that your peer knows. If you delete them, WTP will have to download them again if you need them. Deleting the contents of this folder frees disk space, but it takes longer if you want to access the file again. If you delete files, they will most certainly be accessible on the network thanks to other peers.")
		else:
			# On affiche toutes les commandes possibles ici
			# Chaque commande permet d'afficher une documentation précise, plus que help
			print("Here are all the possible commands here :")
			print("update			vpn			majDNS")
			print("stats			wtp			delAll")
			print("config			license			checkFiles")
			print("dns			blacklist		client <cmd>")
			print("folder tree")
