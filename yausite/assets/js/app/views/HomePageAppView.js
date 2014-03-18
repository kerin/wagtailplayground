define(['backbone', 'views/ArticleView'], function(Backbone, ArticleView){

    var HomePageAppView = Backbone.View.extend({

        el: document.getElementById('homepage'),

        events: {
            'click h3 a': 'navigate'
        },

        initialize: function(){
            this.articleView = new ArticleView();
            window.YAU.HomePageAppRouter.on('route:post', this.showPost, this);
        },

        navigate: function(e){
            e.preventDefault();
            var href = $(e.target).attr('href');
            window.YAU.HomePageAppRouter.navigate(href, {trigger: true});
        },

        showPost: function(path){
            if(path){
                this.articleView.model.set('path', path);
            }
        }

    });

    return HomePageAppView;
});
