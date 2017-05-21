///*****************************************************************************
/// Script TD régulation sur le canal extérieur de SupAgro
/// @author David Dorchies
/// @date Novembre 2013
//******************************************************************************

clear
sScriptPath = get_file_path('MonitoringHauteurs.sce');

// Initialisation des paramètres et fonctions
exec(sScriptPath+'scilab_functions'+filesep()+'init.sce',-1);

// Load user's parameters if exist
if isfile(sScriptPath+"conf_user.sce") then
    exec(sScriptPath+'conf_user.sce',-1);
end

// Load functions
tsFunction = listfiles(sScriptPath+'scilab_functions/*.sci');
for i=1:size(tsFunction,1)
    if strindex(tsFunction(i),"~") == [] then // Evite de charger une fonction en cours d'édition
        exec(tsFunction(i));
    end
end
clear tsFunction;

// Load calibration of the sensors
cfg.Cal = ReadCalibration(cfg);

cfg.TimeLine = 0:(cfg.TimeDuration/cfg.TimeStep); // Vecteur des temps à mesurer

// Contrôle de la configuration
// TODO

vT = []; // Vecteur mémorisation de l'heure
mD = []; // Mémorisation de la série de mesures
scf0 = DisplayHauteurs(cfg);

if messagebox(["Affichage des hauteurs d''eau"; msprintf("Durée : %i minutes",cfg.TimeDuration/60);...
        "Prêt pour démarrer ?"], "modal", "question", ["Démarrer" "Annuler"]) == 1 then
    
    fOut = mopen(msprintf(strsubst(cfg.sOutputPath,"\","\\"),GetCurrentDateTime()),"w");
    sOutFormat = "%s\t"+strcat(repmat("%8.6f",size(cfg.tiRegisters,2),1),"\t")+"\n";
    // Defining time step for real time control
    realtimeinit(cfg.TimeStep);
    // Boucle sur le temps déf dans les param
    while 1==1
        // Controle du déclenchement en temps réel
        realtime(t);
        // Réception des données
        D = GetWaterLevel(cfg);
        [sDate,vDate]=GetCurrentDateTime();
        mfprintf(fOut,sOutFormat,sDate,D');
        mD = [mD;D'];
        
        // Affichage et calcul des indicateurs
        DisplayHauteurs(cfg,scf0,mD);
    end
    
    mclose(fOut);
end
