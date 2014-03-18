define(['backbone'], function(Backbone) {

    var HomePageAppRouter = Backbone.Router.extend({

        routes: {
            "*path": "post"
        }

    });

    return HomePageAppRouter;
});
