<html>
    <head>
        <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
        <link rel="stylesheet" href="https://code.getmdl.io/1.2.1/material.indigo-pink.min.css">
        <script defer src="https://code.getmdl.io/1.2.1/material.min.js"></script>
        <script
            src="https://code.jquery.com/jquery-3.1.1.min.js"
            integrity="sha256-hVVnYaiADRTO2PzUGmuLJr8BLUSjGIZsDYGmIJLv2b8="
            crossorigin="anonymous">
        </script>
    </head>
    <body>
        <div class="mdl-layout mdl-js-layout mdl-layout--fixed-header">
            <header class="mdl-layout__header">
                <div class="mdl-layout__header-row">
                    <!-- Title -->
                    <span class="mdl-layout-title">Botanick - Email harvester</span>
                    <div class="mdl-layout-spacer"></div>
                    <!-- Add spacer, to align navigation to the right -->
                    <div class="mdl-layout-spacer"></div>
                    <!-- Expandable Textfield -->
                    <!-- Navigation. We hide it in small screens. -->
                    <nav class="mdl-navigation mdl-layout--large-screen-only">
                        <a class="mdl-navigation__link" href="">About</a>
                    </nav>
               </div>
            </header>
            <div class="mdl-layout__drawer">
                <span class="mdl-layout-title">Title</span>
                <nav class="mdl-navigation">
                    <a class="mdl-navigation__link" href="">Link</a>
                    <a class="mdl-navigation__link" href="">Link</a>
                    <a class="mdl-navigation__link" href="">Link</a>
                    <a class="mdl-navigation__link" href="">Link</a>
                </nav>
            </div>
            <main class="mdl-layout__content">
                <div class="page-content">
                    <div class="mdl-grid">
                        <div class="mdl-cell mdl-cell--8-col">
                            <script>
                            function check(event) {
                                $('#results').html("");
                                $('#loader').toggle();
                                if (event.keyCode == 13) {
                                    $.ajax({
                                        url : '/domain=test.com',
                                        type : 'GET',
                                        success : function(response, statut){
                                            $('#loader').toggle();
                                            $('#results').append(response.replace(/,/gi, '<br>')) 
                                        }
                                    });
                                }
                            }
                            </script>
                            <form id='search' action="#">
                                <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
                                    <input onkeypress="check(event);" id="input-search" class="mdl-textfield__input" type="text" >
                                    <label class="mdl-textfield__label" for="sample3">Search...</label>
                                </div>
                            </form>
                            <div>
                                <div id="loader" style='display:none;' class="mdl-progress mdl-js-progress mdl-progress__indeterminate"></div>
                                <div id="results"></div>
                            
                            </div>
                        </div>
                        <div class="mdl-cell mdl-cell--4-col">
                            <!-- Wide card with share menu button -->
                            <style>
                            .demo-card-wide.mdl-card {
                                      width: 512px;
                                      }
                            .demo-card-wide > .mdl-card__title {
                                      color: #fff;
                                        height: 176px;
                                        background: url('https://www.squad.fr/static/images/theme/home/mobileChameleon.png') top / cover;
                                        background-size: 30%;
                                        background-position: 90% 100%;
                                              background-repeat: no-repeat;
                                          }
                            .demo-card-wide > .mdl-card__menu {
                                      color: #000;
                                      }
                            </style>

                            <div class="demo-card-wide mdl-card mdl-shadow--2dp">
                                <div class="mdl-card__title">
                                    <h2 class="mdl-card__title-text">Welcome</h2>
                                </div>
                                <div class="mdl-card__supporting-text">
                                    Help us to improve Botanick.
                                    Send an invitation to your friends. Give your feedback.
                                </div>
                                <div class="mdl-card__actions mdl-card--border">
                                    <a class="mdl-button mdl-button--colored mdl-js-button mdl-js-ripple-effect">
                                        Help us !
                                    </a>
                                </div>
                                <div class="mdl-card__menu">
                                    <button class="mdl-button mdl-button--icon mdl-js-button mdl-js-ripple-effect">
                                        <i class="material-icons">share</i>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </main>
       </div>
</body>
</html>
