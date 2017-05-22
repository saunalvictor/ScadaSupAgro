function sWtrLvl = CalEditWaterDepth(cfg, iAcq)
    labels = [];
    typ = list();
    for i=1:length(cfg.tiRegisters)
        labels = [labels;msprintf("Sensor #%i",i)]
    end
    
    bOk = %f
    while ~bOk then

        rep=x_mdialog([...
            msprintf("Edit measured height for acquisition #%i",iAcq);...
            "(Leave blank for no value measured)"],...
            labels,repmat("",length(cfg.tiRegisters),1))

        sWtrLvl = struct()
        s = ["Recorded values are:"]
        for i=1:length(cfg.tiRegisters)
            if rep(i)~="" then
                sWtrLvl($+1) = struct('i', i, 'iReg', cfg.tiRegisters(i), 'Value', evstr(rep(i)))
                s = [s;msprintf("Sensor#%i: %2.3f m",i,sWtrLvl($).Value)]
            end
        end
        
        iBtn = messagebox(s, "Data check", "question", ["Record data and start next measurement","Edit water heights again"], "modal")
        bOk = (iBtn==1)
    end    
endfunction
