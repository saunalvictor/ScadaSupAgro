//******************************************************************************
/// @file $Id$
/// Renvoie la date courante en différents formats
/// @param iFormat Format de date/heure :
///     - 1 : AAAA-MM-JJ hhmmss pour les noms de fichier
///     - 2 : JJ/MM/AAAA hh:mm:ss.000 pour export et faciliter import sous Excel
/// @author David Dorchies
/// @date 20/11/2014
//******************************************************************************
function [sDate,vDate] = GetCurrentDateTime(iFormat)
    vDate=getdate();
    select iFormat
    case 1
        vDate=vDate([1 2 6 7 8 9]);
        sDate=msprintf("%4d-%02d-%02d %02d%02d%02d",vDate);
    case 2
        vDate=vDate([6 2 1 7 8 9 10]);
        sDate=msprintf("%02d/%02d/%04d %02d:%02d:%02d.%03d",vDate);
    end
endfunction
