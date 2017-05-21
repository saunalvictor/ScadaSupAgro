//******************************************************************************
/// @file $Id$
/// Interroge le SCADA pour récupérer le débit
/// @param cfg Configuration du SCADA
/// @param tiRegisters [1 x nb registres] vecteur des n° de registre à interroger
/// @return tQ [1 x nb registres] Débit (m3/s)
/// @return tY [1 x nb registres] Hauteurs d'eau (m)
/// @return tD [1 x nb registres] Valeurs brutes des capteurs
/// @author David Dorchies
/// @date 15/11/2013
//******************************************************************************
function [tQ, tY, tD] = GetDischarge(cfg,tiRegisters)
    
    if ~isdef("tiRegisters","local") then
        tiRegisters = cfg.tiRegisters
    end
    
     [tY, tD] = GetWaterLevel(cfg,tiRegisters);
    
    // Conversion de la hauteur en débit
    for i=1:size(tiRegisters,2)
        CalQ = cfg.CalQ(i);
        select CalQ.Type
        case "SeuilTriangulaire"
            tQ(i) = CalQ.a * (tY(i)-CalQ.p)^CalQ.b;
        case "SeuilRectangulaire"
            tQ(i) = CalQ.Cd * CalQ.l * cfg.Cst.R2G *(tY(i)-CalQ.p)^1.5;
        end
    end
    
endfunction
