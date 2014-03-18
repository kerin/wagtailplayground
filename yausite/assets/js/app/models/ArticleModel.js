define(['backbone'], function(Backbone){

    var ArticleModel = Backbone.Model.extend({

        urlRoot: '/',

        url: function(){
            return this.urlRoot + this.get('path');
        }

    });

    return ArticleModel;
});
