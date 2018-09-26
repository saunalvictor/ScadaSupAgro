///*****************************************************************************
/// Script TD régulation sur le canal extérieur de SupAgro
/// @author David Dorchies
/// @date Novembre 2013
//******************************************************************************

clear
sScriptPath = get_file_path('TP_regulation.sce');

// Initialisation des paramètres et fonctions
exec(sScriptPath+'scilab_functions'+filesep()+'init.sce',-1);

// Load user's parameters if exist
if isfile(sScriptPath+"conf_user.sce") then
    exec(sScriptPath+'conf_user.sce',-1);
end

// Load calibration of the sensors
cfg.Cal = ReadCalibration(cfg);

// Load objective parameters
cfg.mObj = ReadObjectiveSeries(cfg);

cfg.TimeLine = 0:(cfg.TimeDuration/cfg.TimeStep); // Vecteur des temps à mesurer

// Contrôle de la configuration
// TODO

mQ = []; // Mémorisation de la série de mesures
scf0 = DisplayRegulation(cfg,mQ);

if messagebox(["TP régulation"; msprintf("Durée : %i minutes",cfg.TimeDuration/60);...
        "Prêt pour démarrer ?"], "modal", "question", ["Démarrer" "Annuler"]) == 1 then
    
    fOut = OpenOutputFiles(cfg);
    if ~cfg.socket.Connected then
        mprintf("Open socket %i; Host %s:%i\n", cfg.socket.number,cfg.socket.sHost,cfg.socket.iPort)
        SOCKET_open(cfg.socket.number,cfg.socket.sHost,cfg.socket.iPort);
        cfg.socket.Connected = %T
    end
    // Defining time step for real time control
    realtimeinit(cfg.TimeStep);
    // Boucle sur le temps déf dans les param
    for t = cfg.TimeLine
        // Controle du déclenchement en temps réel
        realtime(t);
        // Réception des données
        [Q,Y,D] = GetDischarge(cfg);
        WriteOutputFiles(cfg,fOut,Q,Y,D);
        mQ = [mQ;Q'];
        
        // Affichage et calcul des indicateurs
        DisplayRegulation(cfg,mQ,scf0);
    end
    
    CloseOutputFiles(fOut);
    if cfg.socket.Connected then
        SOCKET_close(cfg.socket.number);
    end
end
