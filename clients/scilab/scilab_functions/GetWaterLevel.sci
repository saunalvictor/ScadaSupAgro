//******************************************************************************
/// @file $Id$
/// Interroge le SCADA pour récupérer les hauteurs d'eau
/// @param cfg Configuration du SCADA
/// @param tiRegisters [1 x nb registres] vecteur des n° de registre à interroger
/// @return tY [1 x nb registres] Hauteurs d'eau (m)
/// @return tD [1 x nb registres] Valeurs brutes des capteurs
/// @author David Dorchies
/// @date 15/11/2013
//******************************************************************************
function [tY, tD] = GetWaterLevel(cfg,tiRegisters)
    if ~isdef("tiRegisters","local") then
        tiRegisters = cfg.tiRegisters
    end
    tD = GetRawData(cfg)';

    // Conversion des valeurs entières en hauteur
    for iCal=1:size(tiRegisters,2)
        select cfg.iModeCalibration
        case 1 then
            tY(iCal) = interpln(cfg.Cal(iCal).m',tD(iCal));
        case 2 then
            tY(iCal) = tD(iCal)*cfg.Cal(iCal).a+cfg.Cal(iCal).b;
        end
    end

endfunction
