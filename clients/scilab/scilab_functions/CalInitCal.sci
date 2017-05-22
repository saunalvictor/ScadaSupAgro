function Cal = CalInitCal(cfg)
    Cal = struct();
    for i=1:length(cfg.tiRegisters)
        Cal(i).iReg = cfg.tiRegisters(i)
        Cal(i).m = []
    end
endfunction
