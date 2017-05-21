//******************************************************************************
/// @file $Id$
/// Ferme les 3 fichiers de mesures
/// @param fOut [1 x 3] Numéros des fichiers de mesure
/// @author David Dorchies
/// @date 20/11/2014
//******************************************************************************
function CloseOutputFiles(fOut)
    for i=1:3
        mclose(fOut(i))
    end
endfunction
