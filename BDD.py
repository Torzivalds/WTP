#! /usr/bin/python
# -*- coding:utf-8 -*-

import sys
import os
import math
import time
import logs
import sqlite3
import fctsClient

def creerBase():
	# Fonction qui a pour seul but de créer la base de données
	# si le file la contenant n'existe pas.
	conn = sqlite3.connect('WTP.db')
	cursor = conn.cursor()
	try:
		cursor.execute("""
			CREATE TABLE IF NOT EXISTS NoeudsHorsCo(
				id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
				IP TEXT,
				NbVerifs INTEGER
			)
		""")
		conn.commit()
		cursor.execute("""
			CREATE TABLE IF NOT EXISTS Fichiers(
				id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
				Nom TEXT,
				DateAjout TEXT,
				Taille INTEGER,
				Chemin TEXT
			)
		""")
		conn.commit()
		cursor.execute("""
			CREATE TABLE IF NOT EXISTS Noeuds(
				id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
				IP TEXT,
				Fonction TEXT default Simple,
				DerSync TEXT,
				DateAjout TEXT
			)
		""")
		conn.commit()
		cursor.execute("""
			CREATE TABLE IF NOT EXISTS FichiersExt(
				id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
				Nom TEXT,
				IP TEXT
			)
		""")
		conn.commit()
		cursor.execute("""
			CREATE TABLE IF NOT EXISTS Statistiques(
				NbNoeuds INTEGER,
				NbSN INTEGER,
				NbFichiersExt INTEGER,
				NbFichiers INTEGER,
				PoidsFichiers INTEGER,
				NbEnvsLstNoeuds INTEGER,
				NbEnvsLstFichiers INTEGER,
				NbEnvsLstFichiersExt INTEGER,
				NbEnvsFichiers INTEGER,
				NbPresence INTEGER,
				NbReceptFichiers INTEGER
			)
		""")
		conn.commit()
		# On initialise les Statistiques
		cursor.execute("""INSERT INTO Statistiques (NbNoeuds, NbSN, NbFichiersExt, NbFichiers, PoidsFichiers, NbEnvsLstNoeuds, NbEnvsLstFichiers, NbEnvsLstFichiersExt, NbEnvsFichiers, NbPresence, NbReceptFichiers) VALUES (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)""")
		conn.commit()
	except Exception as e:
		conn.rollback()
		logs.addLogs("ERROR : Problem with database (creerBase()) :" + str(e))
	conn.close()

def ajouterEntree(nomTable, entree, entree1 = ""):
	# Fonction qui permet d'ajouter une entrée à une table de la base
	verifExistBDD()
	# Vérifier si l'entrée existe déjà dans la BDD.
	# Si il existe on ne fait rien
	# Si il n'existe pas, on l'ajoute
	conn = sqlite3.connect('WTP.db')
	cursor = conn.cursor()
	try:
		if nomTable == "Noeuds":
			cursor.execute("""SELECT id FROM Noeuds WHERE IP = ?""", (entree,))
		elif nomTable == "Fichiers":
			cursor.execute("""SELECT id FROM Fichiers WHERE Nom = ?""", (entree,))
		elif nomTable == "FichiersExt":
			cursor.execute("""SELECT id FROM FichiersExt WHERE Nom = ? AND IP = ?""", (entree, entree1))
		elif nomTable == "NoeudsHorsCo":
			cursor.execute("""SELECT id FROM NoeudsHorsCo WHERE IP = ?""", (entree,))
	except Exception as e:
		logs.addLogs("ERROR : Problem with database (ajouterEntree()):" + str(e))
	else:
		nbRes = 0
		rows = cursor.fetchall()
		for row in rows:
			nbRes += 1
		if nbRes != 0:
			# L'entrée existe déjà
			if nbRes > 1:
				logs.addLogs("ERROR : Entry presents several times in the database. (ajouterEntree())")
		else:
			datetimeAct = str(time.time())
			datetimeAct = datetimeAct[:datetimeAct.find(".")]
			# En fonction de la table, il n'y a pas les mêmes champs à remplir
			try:
				if nomTable == "Noeuds":
					if entree1 == "":
						entree1 = str(fctsClient.CmdDemandeStatut(entree[:entree.find(":")], entree[entree.find(":")+1:]))
						if len(entree1) < 3:
							# C'est une erreur
							logs.addLogs("ERROR : When trying to find the status of the peer : " + str(entree1))
							entree1 = "Simple"
					cursor.execute("""INSERT INTO Noeuds (IP, Fonction, DerSync, DateAjout) VALUES (?, ?, ?, ?)""", (entree, entree1, datetimeAct, datetimeAct))
				elif nomTable == "Fichiers":
					pathFichier = "HOSTEDFILES/" + entree
					cursor.execute("""INSERT INTO Fichiers (Nom, DateAjout, Taille, Chemin) VALUES (?, ?, ?, ?)""", (entree, datetimeAct, os.path.getsize(pathFichier), pathFichier))
				elif nomTable == "FichiersExt":
					cursor.execute("""INSERT INTO FichiersExt (Nom, IP) VALUES (?, ?)""", (entree, entree1))
				elif nomTable == "NoeudsHorsCo":
					cursor.execute("""INSERT INTO NoeudsHorsCo (IP, NbVerifs) VALUES (?, 0)""", (entree,))
				conn.commit()
			except Exception as e:
				conn.rollback()
				logs.addLogs("ERROR : Problem with database (ajouterEntree()):" + str(e))
	conn.close()

def supprEntree(nomTable, entree, entree1 = ""):
	# Fonction qui permet de supprimer une entrée dans une table
	verifExistBDD()
	conn = sqlite3.connect('WTP.db')
	cursor = conn.cursor()
	try:
		if nomTable == "Noeuds":
			cursor.execute("""DELETE FROM Noeuds WHERE IP =  ?""", (entree,))
		elif nomTable == "Fichiers":
			cursor.execute("""DELETE FROM Fichiers WHERE Nom = ?""", (entree,))
		elif nomTable == "FichiersExt":
			cursor.execute("""DELETE FROM FichiersExt WHERE Nom = ? AND IP = ?""", (entree, entree1))
		elif nomTable == "NoeudsHorsCo":
			cursor.execute("""DELETE FROM NoeudsHorsCo WHERE IP =  ?""", (entree,))
		conn.commit()
	except Exception as e:
		conn.rollback()
		logs.addLogs("ERROR : Problem with database (supprEntree()):" + str(e))
	else:
		if nomTable == "Noeuds":
			logs.addLogs("INFO : The peer " + entree + " has been removed from the database.")
		elif nomTable == "Fichiers":
			path = "HOSTEDFILES/" + entree
			try:
				os.remove(path)
			except FileNotFoundError:
				logs.addLogs("INFO : The file " + entree + " was already deleted.")
			else:
				logs.addLogs("INFO : The file " + entree + " has been removed.")
		elif nomTable == "FichiersExt":
			logs.addLogs("INFO : The External file " + entree + " has been removed.")
		elif nomTable == "NoeudsHorsCo":
			logs.addLogs("INFO : The peer off " + entree + " has been permanently deleted from the database.")
	conn.close()

def incrNbVerifsHS(ipPort):
	# Vérifie que le noeud existe
	# Si il existe, le noeud est incémenté de 1.
	verifExistBDD()
	conn = sqlite3.connect('WTP.db')
	cursor = conn.cursor()
	try:
		cursor.execute("""SELECT ID FROM NoeudsHorsCo WHERE IP = ?""", (ipPort,))
		rows = cursor.fetchall()
	except Exception as e:
		conn.rollback()
		logs.addLogs("ERROR : Problem with database (incrNbVerifsHS()):" + str(e))
	nbRes = 0
	for row in rows:
		nbRes += 1
	if nbRes != 0:
		# Le noeud existe, on peut l'incrémenter
		try:
			cursor.execute("""UPDATE NoeudsHorsCo SET NbVerifs = NbVerifs + 1 WHERE IP = ?""", (ipPort,))
			conn.commit()
		except Exception as e:
			conn.rollback()
			logs.addLogs("ERROR : Problem with database (incrNbVerifsHS()):" + str(e))
		logs.addLogs("INFO : The number of verifications of "+ ipPort +" has been incremented by 1.")
	else:
		# Le noeud n'existe pas, juste un warning dans les logs.
		logs.addLogs("ERREUR : The peer off "+ ipPort +" could not be incremented because it no longer exists.")
	conn.close()

def verifNbVerifsHS(ipPort):
	# Vérifie que le nombre de vérifications déjà effectuées
	# S'il y en a plus que 10, le noeud est définitivement supprimé
	verifExistBDD()
	conn = sqlite3.connect('WTP.db')
	cursor = conn.cursor()
	try:
		cursor.execute("""SELECT NbVerifs FROM NoeudsHorsCo WHERE IP = ?""", (ipPort,))
		rows = cursor.fetchall()
	except Exception as e:
		conn.rollback()
		logs.addLogs("ERROR : Problem with database(verifNbVerifsHS()):" + str(e))
	nbRes = 0
	for row in rows:
		nbRes = row[0]
	if nbRes > 10:
		# Le noeud doit être supprimé
		try:
			cursor.execute("""DELETE FROM NoeudsHorsCo WHERE IP =  ?""", (ipPort,))
			conn.commit()
		except Exception as e:
			conn.rollback()
			logs.addLogs("ERROR : Problem with database (verifNbVerifsHS()):" + str(e))
		logs.addLogs("INFO : The peer off "+ ipPort +" has been removed, it no longer responds.")
	conn.close()

def verifFichier(fileName):
	# Fonction qui vérifie si le file existe dans la base de données
	verifExistBDD()
	conn = sqlite3.connect('WTP.db')
	cursor = conn.cursor()
	try:
		cursor.execute("""SELECT ID FROM Fichiers WHERE Nom = ?""", (fileName,))
		rows = cursor.fetchall()
	except Exception as e:
		conn.rollback()
		logs.addLogs("ERROR : Problem with database (verifFichier()) : " + str(e))
	FichierExiste = False
	for row in rows:
		FichierExiste = True
	conn.close()
	return FichierExiste

def modifStats(colonne, valeur=-1):
	# Si valeur = -1, on incrémente, sinon on assigne la valeur en paramètres
	verifExistBDD()
	conn = sqlite3.connect('WTP.db')
	cursor = conn.cursor()
	try:
		if valeur == -1:
			cursor.execute("UPDATE Statistiques SET "+colonne+" = 1 WHERE 1")
		else:
			cursor.execute("UPDATE Statistiques SET "+colonne+" = "+str(valeur)+" WHERE 1")
		conn.commit()
	except Exception as e:
		conn.rollback()
		logs.addLogs("ERROR : Problem with database (modifStats()):" + str(e))
		logs.addLogs(str(valeur) + colonne)
	conn.close()

def compterStats(colonne):
	verifExistBDD()
	conn = sqlite3.connect('WTP.db')
	cursor = conn.cursor()
	try:
		cursor.execute("""SELECT ? FROM Statistiques WHERE 1""", (colonne,))
		conn.commit()
	except Exception as e:
		conn.rollback()
		logs.addLogs("ERROR : Problem with database (compterStats()):" + str(e))
	conn.close()

def aleatoire(nomTable, entree, nbEntrees, fonction = ""):
	# Fonction qui a pour but de renvoyer sour forme d'un tableau nbEntrees lignes
	# contenues dans nomTable de façon aléatoire.
	error = 0
	verifExistBDD()
	conn = sqlite3.connect('WTP.db')
	cursor = conn.cursor()
	try:
		if nomTable == "Noeuds":
			if fonction == "":
				fonction = "Simple"
			cursor.execute("""SELECT IP FROM Noeuds WHERE Fonction = ? ORDER BY RANDOM() LIMIT ?""", (fonction, nbEntrees))
			conn.commit()
	except Exception as e:
		conn.rollback()
		logs.addLogs("ERROR : Problem with database (aleatoire()):" + str(e))
		error += 1
	rows = cursor.fetchall()
	tableau = []
	for row in rows:
		tableau.append(row)
		# On remplit le tableau avant de le retourner
	conn.close()
	if len(tableau) != nbEntrees:
		error += 1
		# return error
		# Ligne à activer seulement lorsque le réseau fonctionne
	return tableau

def chercherInfo(nomTable, info):
	# Fonction qui retourne une information demandée dans la table demandée dans une entrée demandé
	verifExistBDD()
	conn = sqlite3.connect('WTP.db')
	cursor = conn.cursor()
	try:
		if nomTable == "Noeuds":
			cursor.execute("""SELECT Fonction FROM Noeuds WHERE IP = ?""", (info,))
		elif nomTable == "Fichiers":
			cursor.execute("""SELECT id FROM Fichiers WHERE Nom = ?""", (info,))
		elif nomTable == "FichiersExt":
			cursor.execute("""SELECT IP FROM FichiersExt WHERE Nom = ?""", (info,))
		conn.commit()
	except Exception as e:
		conn.rollback()
		logs.addLogs("ERROR : Problem with database (chercherInfo()):" + str(e))
	for row in cursor.fetchall():
		conn.close()
		return row[0]

def verifExistBDD():
	# Fonction qui permet d'alèger le code en évitant les duplications
	try:
		with open('WTP.db'):
			pass
	except Exception:
		logs.addLogs("ERROR : Base not found ... Creating a new base.")
		creerBase()

def searchNoeud(role, nbre = 10):
	# Fonction qui  pour but de chercher 'nbre' noeuds ayant pour role 'role'
	verifExistBDD()
	conn = sqlite3.connect('WTP.db')
	cursor = conn.cursor()
	try:
		cursor.execute("""SELECT IP FROM Noeuds WHERE Fonction = ? ORDER BY RANDOM() LIMIT ?""", (role, nbre))
		conn.commit()
	except Exception as e:
		conn.rollback()
		logs.addLogs("ERROR : Problem with database (aleatoire()):" + str(e))
	rows = cursor.fetchall()
	tableau = []
	for row in rows:
		tableau.append(row)
		# On remplit le tableau avant de le retourner
	conn.close()
	return tableau
