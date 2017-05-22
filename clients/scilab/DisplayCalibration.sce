///*****************************************************************************
/// @file $Id$
/// Script d'affichage de la calibration des capteurs de pression
/// @author David Dorchies
/// @date 27/11/2014
//******************************************************************************

clear
sScriptPath = get_file_path('DisplayCalibration.sce');

// Initialisation des paramètres et fonctions
exec(sScriptPath+'scilab_functions'+filesep()+'init.sce',-1);

// Load user's parameters if exist
if isfile(sScriptPath+"conf_user.sce") then
    exec(sScriptPath+'conf_user.sce',-1);
end

// Load & Display calibration of the sensors
DisplayCalibration(cfg);
