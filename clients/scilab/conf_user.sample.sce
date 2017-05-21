//cfg.socket.bUse = %F; // Si %F le socket n'est pas utilisé (pour débuggage du script)

//cfg.socket.sHost = "127.0.0.1"; // IP address of the server
//cfg.socket.iPort = 5011; // IP listening port of the server

// Caractéristique des seuils triangulaires
cfg.Ouv.SeuilTriangulaire.Type = "SeuilTriangulaire";
cfg.Ouv.SeuilTriangulaire.p = 0.1; // Pelle
cfg.Ouv.SeuilTriangulaire.a = 1.4; // Formule de King (Coefficient)
cfg.Ouv.SeuilTriangulaire.b = 5/2; // Formule de King (Puissance)
