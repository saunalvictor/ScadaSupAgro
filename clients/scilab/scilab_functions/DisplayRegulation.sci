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
        plot2d(cfg.TimeLine*cfg.TimeStep,[cfg.mObj(:,i),cfg.mObj(:,i)*0.8,cfg.mObj(:,i)*1.2,mD2(:,i)]*1E3);
        e=gce(); p1=e.children(1); p2=e.children(2);
        e.children(4).foreground=color("forestgreen");
        e.children(3).foreground=color("grey");
        e.children(2).foreground=color("grey");
        e.children(1).foreground=color("navyblue");
        a=gca();
        if size(mD,1) > 1 then
            Vobj = inttrap(cfg.mObj(1:size(mD,1),i));
            Vdis = inttrap(mD(:,i));
            RMSE = sqrt(sum((mD(:,i)-cfg.mObj(1:size(mD,1),i)).^2)/size(mD,1));
            r = Vdis/Vobj
            a.title.text = msprintf("Mesure n°%i - r%i = %4.2f - RMSE%i = %5.3f", ...
            i,i,r,i,RMSE);
        end
    end
endfunction
