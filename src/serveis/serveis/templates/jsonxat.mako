<html>

<head>
    <meta charset="utf-8" />
    <script src="http://code.jquery.com/jquery-1.11.0.min.js"></script>
    <script lang="javascript">
        
        var urlbase = "/";
        
        function carrega() {
            var canal = $("#canal").val()
            
            $.ajax({
                url: urlbase + "xat_get_canal_ws",
                dataType: "jsonp",
                //type: "get", // jsonp is only get
                data: {"canal": canal},
                error: function( request, status, error ) {
                    alert("error al recarregar missatges "+request.responseText);
                },
                success: function( dades ) {
                    // test errors
                    if( !dades["status"] ) {
                        alert("error: "+dades["missatge"]);
                        return;
                    }
                    // esborrem la llista
                    $("#xatsession").empty();
                    // carreguem missatges
                    var llista_missatges = dades["missatges"];
                    llista_missatges.forEach(function(elem) {
                        var $rem, $msg, $reg, $id;
                        if("remitent" in elem) {
                            $rem = $("<div class='remitent'>"+ elem["remitent"] + " :</div>");
                        }
                        if("missatge" in elem) {
                            $msg = $("<div class='missatge'>"+ elem["missatge"] +"</div>");
                        }
                        if("id" in elem) {
                            $id =  $("<div class='id'>"+ elem["id"] +"</div>");
                        }
                        $reg = $("<div class='registre'></div>");
                        $reg.append($rem,$msg,$id);
                        $("#xatsession").append($reg);
                    });
                    // anem al final de la llista de missatges
                    $("#xatsession").scrollTop( 20000 );
                }
            });
        }

        function envia() {
            if( $("#noumissatge").val() ) {
                // enviar
                var peticio = {
                    "remitent":$("#nick").val(),
                    "missatge":$("#noumissatge").val()
                };
                $.ajax({
                    url: urlbase + "xat_set_missatge_ws",
                    dataType: "jsonp",
                    //type: "get", // jsonp is only get method
                    //contentType:"application/json;charset=UTF-8",
                    //scriptCharset:"UTF-8",
                    data: peticio,
                    error: function( request, status, error ) {
                        alert("fail: "+request.responseText);
                    },
                    success: function( dades ) {
                        if( dades["status"] ) {
                            // esborrem el text input i recarreguem
                            $("#noumissatge").val("");
                            carrega();
                        } else // error
                            alert(dades["missatge"]);
                    }
                });
            } else {
                // no hi ha missatge, recarreguem
                carrega();
            }            
            // evita recàrrega de la pàgina
            return false;
        }
    </script>
    <style>
        body {
            background-image: url('http://thumbs.dreamstime.com/z/dos-personas-que-tienen-una-charla-c%C3%B3moda-15967023.jpg');
            background-position: 0px -300px;
            font-family: Helvetica,sans;
        }
        .remitent {
            //background-color:yellow;
            color: #9900ff;
            display:inline;
            padding: 0 0.6em;
        }
        .missatge {
            //background-color:green;
            display:inline;
            padding:0;
        }
        #xatsession {
            padding: 10px;
            height: 300px;
            width: 600px;
            background-color: #ccccff;
            overflow: scroll;
        }
    </style>
</head>

<body onload="carrega()">
    <h2>JsonP Xat</h2>
    <p>Interfície de test pels alumnes de DAW Lacetània.</p>
    <p>Amb aquest exemple de JS podeu testejar els serveis web a implementar.</p>
    <button onclick="carrega()">carrega missatges</button>
    <form method="post" onsubmit="return envia()">
        Canal:<input type="text" id="canal" value="principal" /><br>
        Nick: <input type="text" id="nick" /><br>
        Text: <input type="text" id="noumissatge" />
        <br><input type="submit" />
    </form>
    <div id="xatsession">
    </div>
    
</body>

</html>
