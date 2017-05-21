function iCal = GetCalIndex(cfg,i)
    iCal = -1; // Par défaut non trouvé
    for j = 1:size(cfg.Cal,1)
        if isfield(cfg.Cal,"iReg") then
            if cfg.Cal(j).iReg == i then
                iCal = j;
                break;
            end
        end
    end
endfunction
