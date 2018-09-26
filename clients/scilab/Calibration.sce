//******************************************************************************
// Calibration des capteurs
//******************************************************************************

clear
sScriptPath = get_file_path('Calibration.sce');

// Initialisation des paramètres et fonctions
exec(sScriptPath+'scilab_functions'+filesep()+'init.sce',-1);

// Start message
if messagebox(["Sensors plugged to registers: "+strcat(string(cfg.tiRegisters),', '); ...
    "Modify cfg.tiRegisters in the file conf_user.sce for changing plugged sensors."; ...
    "Start sensor calibrations?"], "modal", "question", ["Start" "Cancel"]) == 1 then

    // Set configuration
    [bOn, cfg] = CalSetConf(cfg)
    if ~bOn then
        messagebox(["Calibration aborted"],"modal","warning");
    end

    nbMesure = 0; // Nombre de mesure réalisé pour tous les capteurs
    mRawData = []; // Matrice de stockage des mesures capteurs
    mWtrLvl = 0; // Matrice de stockage des hauteurs correspondantes au mesures
    tiSubPlotSize = GetSubPlotSize(length(cfg.tiRegisters))

    while bOn
        s = []
        if max(cfg.calcfg.vNbMes)>0 then
            s = s + msprintf("%3i ",cfg.calcfg.vNbMes');
            s = "Number of measurements: " + s
        end
        if min(cfg.calcfg.vNbMes)<2 then
            s = [s; "A minimum of 2 measures by sensor is required for achieve calibration"]
        end
        s = [s;"Stabilize the water levels in the channels before starting the measurement."; ...
            msprintf("Start measurement #%i?",nbMesure+1); "(Press Cancel for endding calibration)"]
        iMb = messagebox( s, "modal", "question", ["Start" "Cancel"]);
        if iMb~=1 then
            bOn = %F;
            break;
        end
        nbMesure = nbMesure + 1;
        mD = []; // Collected data
        mDmean = [];
        mDstd = [];
        vt = [];
        realtimeinit(cfg.calcfg.Periode);
        winH = waitbar(0,"Data acquisition in progress...");
        tic();
        for i = 0:cfg.calcfg.nbStep
            sMsg = msprintf("Processing measurement #%i / Sensors #%s\n Acquisition %i/%i - Time %3.2f/%3.2f sec.",nbMesure,strcat(string(cfg.tiRegisters),', '),i,cfg.calcfg.nbStep,toc(),cfg.calcfg.Duration);
            waitbar(i/cfg.calcfg.nbStep,sMsg,winH);
            realtime(i);
            vt = [vt; toc()];
            mD = [mD;GetRawData(cfg)];
            // Calcul des stats des mesures
            mDmean = [mDmean;mean(mD,"r")];
            mDstd = [mDstd; stdev(mD,"r")];
            clf();
            for iReg = 1:length(cfg.tiRegisters)
                subplot(tiSubPlotSize(1),tiSubPlotSize(2),iReg);
                plot(vt,[mD(:,iReg),mDmean(:,iReg),mDmean(:,iReg)+mDstd(:,iReg),mDmean(:,iReg)-mDstd(:,iReg)]);
                xtitle(msprintf("Sensor #%i\n Last = %i, Mean = %3.2f, Standard deviation = %3.2f",iReg,mD($,iReg),mDmean($,iReg),mDstd($,iReg)));
            end
        end
        close(winH);

        mRawData(nbMesure,:) = mDmean($,:);
        sWtrLvl = CalEditWaterDepth(cfg, nbMesure)
        if sWtrLvl~=struct() then
            cfg = CalWriteCalibration(cfg, nbMesure==1, mRawData(nbMesure,:), sWtrLvl)
        end
    end // while bOn

    if min(cfg.calcfg.vNbMes)<2 then
        messagebox(["Calibration aborted","Each sensor needs a minimum of 2 measures";...
            "The file "+cfg.calcfg.sPath+" is not ready to be used."],"modal","error");
    else
        messagebox(["Mesures de calibrations enregistrées dans :";cfg.calcfg.sPath],"modal","info");
        DisplayCalibration(cfg)
    end
end


