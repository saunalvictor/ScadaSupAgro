//******************************************************************************
/// Récupère une série de données sur une liste de registre
/// @author David Dorchies
/// @date 12/11/2013
/// @param cfg
/// @param tiRegisters [1 x nb registres] Liste des registres à lire (facultatif)
/// @return tD [1 x nb registres] vecteur avec les valeurs entières des registres
//******************************************************************************
function tD = GetRawData(cfg,tiRegisters)
    //errcatch(-1,"pause");
    if ~isdef("tiRegisters","local") then
        tiRegisters = cfg.tiRegisters
    end
    
    sResp = [];
    
    sQuery = msprintf("GET %s",strcat(string(tiRegisters),','))
    mprintf("Sending ""%s"" to %s:%i\n",sQuery,cfg.socket.sHost,cfg.socket.iPort)
    if cfg.socket.bUse then
        if ~cfg.socket.Connected then
            SOCKET_open(cfg.socket.number,cfg.socket.sHost,cfg.socket.iPort);
            cfg.socket.Connected = %T
        end
        SOCKET_write(cfg.socket.number,sQuery)
        t1 = now()
        while sResp==[] & now()-t1 < cfg.socket.TimeOut
            sResp = SOCKET_read(cfg.socket.number)
        end
    else
        sResp =  strcat(repmat(string(int(90+rand()*20)),1,size(tiRegisters,2)),' ');
    end
    if sResp~=[] then
        mprintf("Received %s from %s:%i\n",sResp,cfg.socket.sHost,cfg.socket.iPort)
        tD = evstr("["+sResp+"]");
    else 
        mprintf("Connection time out\n")
        tD = []
    end
    
endfunction
