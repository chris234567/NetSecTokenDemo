Beispiel zur Demo von Accesstoken mit JWT

Komponenten
 - Nginx Proxy: zum Routing der Anfragen zwischen frontend und backend
 - Flask Backend: Zum Einloggen der User, Austellen der Tokens und Verarbeitung der API Anfragen auf User Ressourcen
 - Vue Frontend: Zum Einloggen & Anzeigen/Manipulation der User Ressourcen via der API

Flow:
 - User loggt sich ein (username: pete, password: 132; app.py Z.24)
 - Backend stellt bei gueltigen Credentials einen JWT Token auf 15 Sekunden aus
 - Auf Page-Refresh werden API-Daten vom Backend geholt, Anfragen verifiziert mit Token als Authorization Header 
   - Alle API-Methoden werden mit einem Decorator geschuetzt, der jede Request auf einen gueltigen JWT Bearer Token prueft
   - Sollte der Token abgelaufen sein oder anderweitig ungueltig sein, werden die Anfragen abgelehnt
    (werden in unserem Beispiel aber nicht weiter behandelt, lediglich Werte auf "undefined")

Der Flow/Grant aehnelt am ehesten dem Client Credentials Flow & Implicit Grant von OAuth 2.0.

Achtung! Bei dem Beispiel wurde Sichherheit zum Zweck der Anschaulichkeit ausser Acht gelassen.
(Token sollten zum Beispiel nie im Local/Session Storage geseichert werden, da Sie dort per XSS ausgelesen werden koennten)
