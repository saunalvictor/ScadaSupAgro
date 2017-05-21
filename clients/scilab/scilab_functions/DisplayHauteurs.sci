//******************************************************************************
/// @warning !!! EBAUCHE DE CODE NON TERMINEE ET NON TESTEE !!!
//******************************************************************************
/// @file $Id$
/// Trace les courbes des mesures de hauteurs d'eau
/// @param cfg Configuration du SCADA
/// @param scf0 Identifiant du graphique. Facultatif, si absent, le graphique est créé et l'identifiant est renvoyé
/// @param vT [nb pas de temps x 1] Temps de mesures
/// @param mD [nb pas de temps x nb de registres] Mesures de hauteurs d'eau
/// @return scf0 Identifiant du graphique
/// @author David Dorchies
/// @date 15/11/2013
//******************************************************************************
function scf0 = DisplayHauteurs(cfg,scf0,vT,mD)

    nTS = cfg.TimeDuration/cfg.TimeStep; // Nb de pas temps affichés
    nCol = size(cfg.tiRegisters,2); // 
    mD2 = ones(nTS,nCol)*%nan;

    if ~isdef("scf0") then
        scf0 = scf();
    else
        scf(scf0);
        if size(mD,1) > nTS then
            mD2 = mD(size(mD,1)-nTS+1:$,:);
        else
            mD2(nTS-size(mD,1)+1:$,:) = mD;
        end
    end
    
    clf(scf0)
    plot(mD2)
    
    a=gca();
    a.title.text = "toto";

endfunction
