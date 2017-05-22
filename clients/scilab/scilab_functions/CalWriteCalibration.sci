// Write calibration data for one serie of measurement
function [cfg, iErr] = CalWriteCalibration(cfg, bFirstCall, vRawData, sWtrLvl)

    if bFirstCall & isfile(cfg.calcfg.sPath) then
        s = ["Existing "+cfg.calcfg.sPath+" file found";"What do you want to do for the calibration?"]
        iMb = messagebox( s, "modal", "question", ["Append to the existing file" "Archive this file and create a new one"]);
        if iMb == 2 then
            tOldFileInfo = fileinfo(cfg.calcfg.sPath);
            sOldFileName = cfg.calcfg.sPath+"_"+msprintf("%i",getdate(tOldFileInfo(6))')+".txt";
            movefile(cfg.calcfg.sPath,sOldFileName);
            messagebox(["The older file has been archived with the name :";sOldFileName],"modal","info");
        else
            cfg.Cal = ReadCalibration(cfg)
        end
    end

    for i = 1:size(sWtrLvl,1)
        cfg.Cal(sWtrLvl(i).i).m = [cfg.Cal(sWtrLvl(i).i).m; vRawData(1,sWtrLvl(i).i), sWtrLvl(i).Value] 
        f = mopen(cfg.calcfg.sPath,'a')
        mfprintf(f,"%i\t%6.4f\t%6.4f\n",cfg.Cal(sWtrLvl(i).i).iReg,cfg.Cal(sWtrLvl(i).i).m($,:));
        mclose(f);
    end
    
    for i = 1:length(cfg.tiRegisters)
        cfg.calcfg.vNbMes(1,i) = size(cfg.Cal(i).m,1)
    end

endfunction
