//******************************************************************************
/// Chargement des functions et des paramètres
/// @author David Dorchies
/// @date 8/11/2013
//******************************************************************************

// Load default parameters
exec(sScriptPath+'conf_default.sce',-1);

// Load user's parameters if exist
if isfile(sScriptPath+"conf_user.sce") then
    exec(sScriptPath+'conf_user.sce',-1);
end

if cfg.socket.bUse then
    // Vérification de l'existence du module socket_toolbox
    if ~atomsIsInstalled("socket_toolbox") then
        atomsInstall("socket_toolbox");
    end
    if ~atomsIsLoaded("socket_toolbox") then
        atomsLoad("socket_toolbox");
    end
end

// Load functions
tsFunction = listfiles(sScriptPath+'scilab_functions/*.sci');
for i=1:size(tsFunction,1)
    if strindex(tsFunction(i),"~") == [] then // Evite de charger une fonction en cours d'édition
        exec(tsFunction(i));
    end
end
clear tsFunction;
