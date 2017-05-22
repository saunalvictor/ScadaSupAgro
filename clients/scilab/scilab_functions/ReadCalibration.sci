//******************************************************************************
/// Lecture des données de calibration des capteurs
/// @param cfg Configuration du SCADA
/// @return Cal Structure [1 x nb registres] :
///     - Cal(:).iReg : n° du registre
///     - Cal(:).m [nb mesures x 2]: correspondances mesures brutes/hauteurs d'eau(m)
///     - Cal(:).a [1 x 1] Coefficient directeur de la droite de régression des mesures
///     - Cal(:).b [1 x 1] Ordonnée à l'origine de la droite de régression des mesures
/// @author David Dorchies
/// @date 8/11/2013
//******************************************************************************
function Cal = ReadCalibration(cfg)
    if isfile(cfg.calcfg.sPath) then
        M = fscanfMat(cfg.calcfg.sPath);
        Cal = CalInitCal(cfg)
        for i=1:length(cfg.tiRegisters)
            iLignes = find(M(:,1)==cfg.tiRegisters(i));
            if iLignes~=[] then
                Cal(i).iReg = cfg.tiRegisters(i);
                Cal(i).m = M(iLignes,2:3);
                [Cal(i).a,Cal(i).b]=reglin(Cal(i).m(:,1)',Cal(i).m(:,2)')
            end
        end
    else
        Cal = %F;
    end
endfunction
