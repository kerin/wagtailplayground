require(['jquery', 'backbone', 'HomepageAppRouter', 'views/HomePageAppView'],
        function($, Backbone, HomePageAppRouter, HomePageAppView) {

    window.YAU = window.YAU || {};

    $(function(){

        if($('#homepage').length){

            window.YAU.HomePageAppRouter = new HomePageAppRouter();
            var view = new HomePageAppView();

            Backbone.history.start({
                pushState: true
            });

        }else{

            /*
            window.onpopstate = function(e){
                window.location.replace(window.location.href);
            }
            */

        }

    });

});
