//******************************************************************************
/// Récupère une série de données sur une liste de registre
/// @author David Dorchies
/// @date 12/11/2013
/// @param cfg
/// @param tiRegisters [1 x nb registres] Liste des registres à lire (facultatif)
/// @return tD [1 x nb registres] vecteur avec les valeurs entières des registres
//******************************************************************************
function tD = GetRawData(cfg,tiRegisters)
    if ~isdef("tiRegisters","local") then
        tiRegisters = cfg.tiRegisters
    end
    
    sQuery = msprintf("GET %s",strcat("A"+string(tiRegisters),','))
    mprintf("Sending ""%s"" to %s:%i\n",sQuery,cfg.socket.sHost,cfg.socket.iPort)
    if cfg.socket.bUse then
        if ~cfg.socket.Connected then
            mprintf("Open socket %i; Host %s:%i\n", cfg.socket.number,cfg.socket.sHost,cfg.socket.iPort)
            SOCKET_open(cfg.socket.number,cfg.socket.sHost,cfg.socket.iPort);
            cfg.socket.Connected = %T
        end
        SOCKET_write(cfg.socket.number,sQuery)
        t1 = now()
        tD = []
        while tD==[] & now()-t1 < cfg.socket.TimeOut
            sResp = SOCKET_read(cfg.socket.number)
            if sResp<>[] then
                for i= 1:size(sResp,1)
                    mprintf("Received %s\n",sResp(i))
                    tsD = strsplit(sResp(i),";")
                    iS = size(tsD,1)
                    if iS==1+size(cfg.tiRegisters,2) then
                        tD = evstr(tsD(2:$))'
                        mprintf("Data =")
                        mprintf("%i ",tD')
                        mprintf("\n")
                        break
                    end
                end
            end
        end
    else
        tD =  repmat(string(int(90+rand()*20)),1,size(tiRegisters,2));
    end
    if tD==[] then
        mprintf("Connection time out\n")
    end
    
endfunction
