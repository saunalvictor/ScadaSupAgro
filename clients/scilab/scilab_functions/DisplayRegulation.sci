//******************************************************************************
/// @file $Id$
/// Trace les courbes des mesures de débit et des objectifs de régulation
/// pour le TP "Régulation manuelle"
/// @param cfg Configuration du SCADA
/// @param mD [nb pas de temps x nb de registres] Mesures de débits
/// @param scf0 Identifiant du graphique. Facultatif, si absent, le graphique est créé et l'identifiant est renvoyé
/// @return scf0 Identifiant du graphique
/// @author David Dorchies
/// @date 15/11/2013
//******************************************************************************
function scf0 = DisplayRegulation(cfg,mD,scf0)
    if ~isdef("scf0") then
        scf0 = scf();
        bTitle = %t;
    else
        scf(scf0);
        bTitle = %f;
    end
    
    c = sqrt(size(cfg.tiRegisters,2));
    nL = floor(c);
    nC = floor(c+0.9999);
    
    mD2 = ones(cfg.mObj)*%nan;
    if size(mD,1) > 0 then
        mD2(1:size(mD,1),:) = mD;
    end

    for i = 1:size(cfg.tiRegisters,2)
        subplot(nL,nC,i);
        plot2d(cfg.TimeLine*cfg.TimeStep,[cfg.mObj(:,i),mD2(:,i)]*1E3);
        a=gca();
        if size(mD,1) > 1 then
            Vobj = inttrap(cfg.mObj(1:size(mD,1),i));
            Vdis = inttrap(mD(:,i));
            RMSE = sqrt(sum((mD(:,i)-cfg.mObj(1:size(mD,1),i)).^2));
            r = Vdis/Vobj
            a.title.text = msprintf("Mesure n°%i - r%i = %4.2f - RMSE%i = %3.1f", ...
            i,i,r,i,RMSE);
        end
    end
endfunction
