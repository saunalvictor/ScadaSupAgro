function [tY,tQ] = GetData(cfg)

    if cfg.socket.bUse then
        SOCKET_open(cfg.socket.number,cfg.socket.sHost,cfg.socket.iPort);
        SOCKET_write(1,msprintf("GET %s",strcat(string(cfg.tiRegisters),',')))
        sResp = SOCKET_read(1)
        SOCKET_close(cfg.socket.number)
    else
        sResp =  strcat(repmat("100",1,size(cfg.tiRegisters,2),','));
    end
    
    tD = evstr("["+sResp+"]");
    
    // Conversion des valeurs entières en hauteur
    for i=1:length(cfg.tiRegisters)
        tY(i) = interpln(cfg.Calibration(i).m,tD(i));
    end
     
    
    // Conversion de la hauteur en débit
    
    
endfunction
