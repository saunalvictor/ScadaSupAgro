// Set configuration for calibration process
function [bOn, cfg] = CalSetConf(cfg)

    // Initialisation of recording structure
    if ~isfield(cfg,"Cal") then
        cfg.Cal = CalInitCal(cfg)
    end

    // Initialisation of configuration parameters
    bOn = %F
    cfg.calcfg.Periode = []
    cfg.calcfg.Duration = []
    cfg.calcfg.nbStep = []
    cfg.calcfg.vNbMes = zeros(1,length(cfg.tiRegisters))


    cfg.calcfg.Periode=evstr(x_dialog('Measurement period (seconds)',string(cfg.calcfg.init.period)));
    if cfg.calcfg.Periode==[] | cfg.calcfg.Periode == 0 then
        return
    end
    cfg.calcfg.Duration=evstr(x_dialog('Measurement duration (seconds)',string(cfg.calcfg.init.duration)));
    if cfg.calcfg.Duration==[] then
        return
    end
    cfg.calcfg.nbStep = floor(cfg.calcfg.Duration/cfg.calcfg.Periode);



    bOn = %T; // Mettre à %F pour stopper les opérations de calibration

endfunction
