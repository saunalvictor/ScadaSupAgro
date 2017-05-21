//******************************************************************************
// Calibration des capteurs
//******************************************************************************

clear
sScriptPath = get_file_path('Calibration.sce');

// Initialisation des paramètres et fonctions
exec(sScriptPath+'scilab_functions'+filesep()+'init.sce',-1);

// Start message
bOn = %T; // Mettre à %F pour stopper les opérations de calibration
sMessage = "Capteurs connectés aux registres: "+strcat(string(cfg.tiRegisters),', ');
if messagebox([sMessage; ...
    "Pour modifier la liste des capteurs, modifier cfg.tiRegisters dans le fichier conf_user.sce."; ...
    "Démarrer le calage des capteurs ?"], "modal", "question", ["Démarrer" "Annuler"]) == 1 then
    //    cfg.Cal = ReadCalibration(cfg);
    //    if typeof(cfg.Cal) == "st" then
    //        for i = size(cfg.Cal,1)
    //            if find(cfg.Cal(i).iReg==cfg.tiRegisters) then
    //                iQ = messagebox(["Des données de calibrations existent déjà pour au moins un des capteurs."; ...
    //                    "Que voulez-vous faire ?"], "modal", "warning", ["Ecraser les données existantes" "Ajouter de nouvelles mesures"])
    //                select iQ
    //                case 0
    //                    bOn = %F
    //                case 1
    //                    cfg.Cal = null();
    //                end
    //                break;
    //            end
    //        end
    //    end
    if bOn then
        Periode=evstr(x_dialog('Période de mesure (secondes)','2'));
        Duration=evstr(x_dialog('Durée de mesure (secondes)','20'));
        nbStep = floor(Duration/Periode);
    end
    nbMesure = 0; // Nombre de mesure réalisé pour tous les capteurs
    mRawData = []; // Matrice de stockage des mesures capteurs
    mWtrLvl = 0; // Matrice de stockage des hauteurs correspondantes au mesures

    while bOn
        for iReg = cfg.tiRegisters
            numReg = find(iReg==cfg.tiRegisters);
            iMb = messagebox( ...
            ["Stabilisez les niveaux d''eau dans les canaux avant de démarrer la mesure."; ...
            msprintf("Démarrer la mesure n°%i du capteur n°%i (registre n°%i) ?",nbMesure+1,numReg,iReg)], ...
            "modal", "question", ["Démarrer" "Annuler"]);
            if iMb~=1 then
                bOn = %F;
                break;
            end
            mD = [];
            realtimeinit(Periode);
            winH = waitbar(0,"Capture en cours...");
            tic();
            for i = 0:nbStep
                sMsg = msprintf("Mesure n°%i / Capteur n°%i\n Acquisition %i/%i - Temps %3.1f/%3.1f sec.",nbMesure+1,numReg,i,nbStep,toc(),Duration);
                if i>0 then
                    sMsg = [sMsg ; msprintf("\nMesures brutes du capteur : Last = %i, Min = %i, Moy = %i, Max = %i",mD($),tDmin,tDmean,tDmax)]
                end
                waitbar(i/nbStep,sMsg,winH);
                realtime(i);
                mD = [mD;GetRawData(cfg,iReg)];
                // Calcul des stats des mesures
                tDmean = mean(mD,"r");
                tDmin = min(mD,"r");
                tDmax = max(mD,"r");
            end
            close(winH);

            mRawData(nbMesure+1,numReg) = tDmean;
            if cfg.socket.bUse then
                sDef = "0";
            else
                sDef = string(tDmean/500);
            end
            mWtrLvl(nbMesure+1,numReg)=evstr(x_dialog( ...
            [msprintf("Mesure n°%i",nbMesure+1); ...
            msprintf("Capteur n°%i (registre n°%i)",numReg,iReg); ...
            msprintf("Mesures brutes du capteur : Min = %i, Moy = %i, Max = %i",tDmin,tDmean,tDmax); ...
            "Hauteur d''eau mesurée en mètres ?"], ...
            sDef));
        end
        if bOn then
            nbMesure = nbMesure + 1;
        end
    end

    // On ne garde que les mesures complètes de tous les capteurs
    mRawData = mRawData(1:nbMesure,:);
    mWtrLvl = mWtrLvl(1:nbMesure,:);    

    if nbMesure > 1 then
        // Enregistrement des paramètres
        if ~isfield(cfg,"Cal") then
            cfg.Cal = struct();
        end

        for iCal = 1:size(cfg.tiRegisters,2)
            cfg.Cal(iCal).iReg = cfg.tiRegisters(iCal);
            cfg.Cal(iCal).m = [];
            cfg.Cal(iCal).m = [cfg.Cal(iCal).m;mRawData(:,iCal),mWtrLvl(:,iCal)];
        end

        if isfile(cfg.sCalPath) then
            tOldFileInfo = fileinfo(cfg.sCalPath);
            sOldFileName = cfg.sCalPath+"_"+msprintf("%i",getdate(tOldFileInfo(6))');
            movefile(cfg.sCalPath,sOldFileName);
        end

        f = mopen(cfg.sCalPath,'w')
        for i = 1:size(cfg.Cal,1)
            for j = 1:size(cfg.Cal(i).m,1)
                mfprintf(f,"%i\t%i\t%6.4f\n",cfg.Cal(i).iReg,cfg.Cal(i).m(j,:)); 
            end
        end
        mclose(f);
        messagebox(["Mesures de calibrations enregistrées dans :";cfg.sCalPath],"modal","info");
        DisplayCalibration(cfg)
    else
        messagebox(["Nombre de mesures insuffisant";"Il faut faire au moins 2 mesures à chaque capteur."],"modal","error");
    end
end


