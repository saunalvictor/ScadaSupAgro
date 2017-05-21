//******************************************************************************
/// Lecture des scénarios de prélèvement (débits objectifs)
/// @param cfg Configuration du SCADA
/// @return mObj [3 x nb opérations] 1 ligne par opération contenant :
///     - n° du registre
///     - temps (sec.)
///     - débit objectif (m3/s)
/// @author David Dorchies
/// @date 15/11/2013
//******************************************************************************
function mObj = ReadObjectiveSeries(cfg)
    errcatch(-1,"pause");
    M = fscanfMat(cfg.sObjPath);
    stObj = struct();
    tCpt = zeros(1,size(cfg.tiRegisters,2));
    for i=1:size(M,1)
        iCal = find(cfg.tiRegisters==M(i,1));
        if iCal ~=[] then
            c = tCpt(iCal);
            if c > 0 then
                // Ajout de l'échelon avant la manoeuvre pour l'interpolation
                c = c + 1;
                stObj(iCal).t(c) = M(i,2)-cfg.TimeStep;
                stObj(iCal).Q(c) = stObj(iCal).Q(c-1);
            end
            c = c + 1;
            stObj(iCal).t(c) = M(i,2);
            stObj(iCal).Q(c) = M(i,3);
            tCpt(iCal) = c;
        end
    end
    tTime = 0:cfg.TimeStep:cfg.TimeDuration;
    mObj=zeros(size(tTime,2),size(cfg.tiRegisters,2));
    for i=1:size(cfg.tiRegisters,2)
        if stObj(i).t($)<cfg.TimeDuration then
            stObj(i).t(tCpt(i)+1) = cfg.TimeDuration;
            stObj(i).Q(tCpt(i)+1) = stObj(i).Q(tCpt(i));
        end
        mObj(:,i) = interpln([stObj(i).t';stObj(i).Q'],tTime)';
    end
    
endfunction
