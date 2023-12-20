### Beispiel zur Demo von Accesstoken mit JWT

Zum Ausprobieren einfach das Repo ziehen und im Ordner "docker compose up".
Die Login-Seite ist unter http://localhost:8080 zu erreichen.

#### Komponenten
 - Nginx Proxy: Zum Routing der Anfragen zwischen Frontend und Backend
 - Flask Backend: Zum Einloggen der User, Austellen der Tokens und Verarbeitung der API-Anfragen auf User-Ressourcen
 - Vue Frontend: Zum Einloggen & Anzeigen/Verändern der User Ressourcen via API-Anfragen

#### Flow
 - User loggt sich ein (username: pete, password: 132; app.py Z.24)
 - Backend stellt bei gültigen Credentials einen JWT Token auf 15 Sekunden aus (app.py Z.80)
 - Auf Page-Refresh werden API-Daten vom Backend geholt, Anfragen verifiziert mit Token als Authorization Header 
   - Alle API-Methoden werden mit einem Decorator geschützt, der jede Anfrage auf einen gültigen JWT Bearer Token prüft
   - Sollte der Token abgelaufen oder anderweitig ungültig sein, werden die Anfragen abgelehnt
    (werden in unserem Beispiel aber nicht weiter behandelt, lediglich Werte auf "undefined")

Der Flow/Grant ähnelt am ehesten dem Client Credentials Flow & Implicit Grant von OAuth 2.0.

**Achtung!** Bei dem Beispiel wurde Sichherheit zum Zweck der Anschaulichkeit außer Acht gelassen. <br>
(Token sollten zum Beispiel nie im Local/Session Storage geseichert werden, da Sie dort per XSS ausgelesen werden könnten)
