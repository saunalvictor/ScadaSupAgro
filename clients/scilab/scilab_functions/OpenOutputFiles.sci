//******************************************************************************
/// @file $Id$
/// Ouvre les 3 fichiers de mesures
/// @param cfg Configuration du SCADA
/// @return fOut [1 x 3] Numéros des fichiers de mesure
/// @author David Dorchies
/// @date 20/11/2014
//******************************************************************************
function fOut = OpenOutputFiles(cfg)
    tV = ["Q","Y","D"]
    i=0
    for V=tV
        i=i+1
        sFN = cfg.sOutputPath + msprintf("%s_%s.txt",V,GetCurrentDateTime(1))
        fOut(i) = mopen(sFN,"w");
    end
endfunction
