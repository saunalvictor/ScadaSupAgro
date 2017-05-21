//******************************************************************************
/// @file $Id$
/// Ecrit les dernières mesures dans les fichiers de mesures
/// @param cfg Configuration du SCADA
/// @param fOut [1 x 3] Numéros des fichiers de mesure
/// @param Q [1 x nb registres] Débits (m3/s)
/// @param Y [1 x nb registres] Débits (m)
/// @param D [1 x nb registres] Mesures brutes des capteurs
/// @author David Dorchies
/// @date 20/11/2014
//******************************************************************************
function WriteOutputFiles(cfg,fOut,Q,Y,D)
    m = [Q,Y,D]'
    sOutFormat = "%s\t"+strcat(repmat("%8.6f",size(cfg.tiRegisters,2),1),"\t")+"\n";
    for i=1:3
        mfprintf(fOut(i),sOutFormat,GetCurrentDateTime(2),m(i,:))
    end
endfunction
