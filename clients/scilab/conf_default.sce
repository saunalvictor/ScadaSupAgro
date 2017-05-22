//******************************************************************************
/// Script TD régulation sur le canal extérieur de SupAgro
/// Paramètres de configuration par defaut
/// @note Ce fichier ne doit pas être modifié. Il faut écraser les valeurs par 
/// défaut en utilisant un fichier conf_user.sce
/// @author David Dorchies
/// @date Novembre 2013

//******************************************************************************
cfg = struct();

// Main folder for these Scilab scripts (sScriptPath comes from load_conf.sce)
cfg.sScriptPath = sScriptPath;

// Time parameters
cfg.TimeStep = 1; // Time step of data acquisition in seconds
cfg.TimeDuration = 5*60; // Duration of the experiment in seconds

// List of registers for data acquisition
cfg.tiRegisters = 3:6; // 3:6 = Entrées analogiques 1 à 4

//******************************************************************************
// [ C A L I B R A T I O N ]
//******************************************************************************

// Fichier contenant la calibration des capteurs
cfg.calcfg.sPath = cfg.sScriptPath + "calibration.txt";
// Format du fichier %n %m %h avec :
// - %n le n° du registre
// - %m la valeur de sortie du capteur (entier entre 0 et 1023)
// - %h le tirant d'eau en mètres dans le canal

// Default measurement period
cfg.calcfg.init.period = 2;

// Default measurement duration
cfg.calcfg.init.duration = 30;

//******************************************************************************
// [ M E A S U R E M E N T  S E T T I N G S ]
//******************************************************************************

// Mode de calcul du calage des capteurs :
// - 1 interpolation entre les points de mesures 
// - 2 utilisation d'une régression linéaire sur les points de mesure
cfg.iModeCalibration = 2;

// Fichier de sortie des chroniques
cfg.sOutputPath = cfg.sScriptPath + "outputs" + filesep();

// Configuration of socket communication
cfg.socket.bUse = %T; // Si %F le socket n'est pas utilisé (pour débuggage du script)
cfg.socket.number = 1; // Internal scilab number of the socket
cfg.socket.sHost = "147.99.14.30"; // IP address of the server
cfg.socket.iPort = 443; // IP listening port of the server
cfg.socket.TimeOut = 10 / 86400; // Time out for aborting communication (day unit)
cfg.socket.Connected = %F; // Variable managing the connection state

// Fichier à lire contenant les objectifs aux prises
cfg.sObjPath = cfg.sScriptPath + "objectives.txt";
// Format du fichier %n %t %v avec :
// - %n le n° de la prise
// - %t le temps de changement de manoeuvre en secondes
// - %v le débit objectif en m3/s

// Paramètres de calcul du débit
// Caractéristique des seuils triangulaires
cfg.Ouv.SeuilTriangulaire.Type = "SeuilTriangulaire";
cfg.Ouv.SeuilTriangulaire.p = 0.1; // Pelle
cfg.Ouv.SeuilTriangulaire.a = 1.32; // Formule de King (Coefficient)
cfg.Ouv.SeuilTriangulaire.b = 5/2; // Formule de King (Puissance)

// Caractéristiques des seuils rectangulaire à Cd Fixe
cfg.Ouv.SeuilRectangulaire.Type = "SeuilRectangulaire";
cfg.Ouv.SeuilRectangulaire.Cd = 0.4; // Coefficient de débit
cfg.Ouv.SeuilRectangulaire.p = 0.1; // Pelle
cfg.Ouv.SeuilRectangulaire.l = 0.2; // Largeur

cfg.CalQ = struct();
cfg.CalQ(1) = cfg.Ouv.SeuilTriangulaire;
cfg.CalQ(2) = cfg.Ouv.SeuilTriangulaire;
cfg.CalQ(3) = cfg.Ouv.SeuilTriangulaire;
cfg.CalQ(4) = cfg.Ouv.SeuilTriangulaire;

// Constantes
cfg.Cst.R2G = sqrt(2*9.81);
