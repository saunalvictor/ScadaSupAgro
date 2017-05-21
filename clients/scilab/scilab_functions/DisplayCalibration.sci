//******************************************************************************
/// @file $Id$
/// Trace les courbes de tarage des capteurs
/// @param cfg Configuration du SCADA
/// @author David Dorchies
/// @date 27/11/2013
//******************************************************************************
function scf0 = DisplayCalibration(cfg,scf0)
    cfg.Cal = ReadCalibration(cfg)
    c = sqrt(size(cfg.tiRegisters,2));
    nL = floor(c);
    nC = floor(c+0.9999);

    if ~isdef("scf0","local") then
        scf0 = scf();
    else 
        scf(scf0);
    end
    for iCal = 1:size(cfg.tiRegisters,2)
        subplot(nL,nC,iCal);
        plot2d(cfg.Cal(iCal).m(:,1),cfg.Cal(iCal).m(:,2),-4);
        // Extension de la zone de traçage 5% autour des valeurs extrêmes
        mDB = scf0.children(1).data_bounds
        tMarges = 0.05.*(mDB(2,:)-mDB(1,:))
        mDB(1,:) = mDB(1,:) - tMarges
        mDB(2,:) = mDB(2,:) + tMarges
        scf0.children(1).data_bounds = mDB
        scf0.children(1).font_size = 3
        // Coloration des points de mesure en bleu
        scf0.children(1).children(1).children(1).mark_foreground = 9;
        // Traçage de la droite de régression
        plot2d(mDB(:,1),cfg.Cal(iCal).a.*mDB(:,1)+cfg.Cal(iCal).b)
        xtitle(msprintf("Calibration registre n°%i",cfg.Cal(iCal).iReg))
        tRange = mDB(2,:)-mDB(1,:)
        xstring(mDB(1,1)+tRange(1)*0.3,mDB(1,2)+tRange(2)*0.1,...
            msprintf("$y = %7.5f x + %7.5f$",cfg.Cal(iCal).a,cfg.Cal(iCal).b))
    end
endfunction
