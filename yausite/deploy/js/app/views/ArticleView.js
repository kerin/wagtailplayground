define(['backbone', 'models/ArticleModel'], function(Backbone, ArticleModel){

    var ArticleView = Backbone.View.extend({

        el: '#article',

        initialize: function(){
            this.model = new ArticleModel();
            this.model.on('change:path', this.changePath, this);
            this.model.on('change:html', this.render, this);
        },

        changePath: function(){
            if(this.model.get('path')){
                this.model.fetch();
            }else{
                this.model.set('html', null);
            }
        },

        render: function(){
            this.$el.html(this.model.get('html'));
            return this;
        }

    });

    return ArticleView;
});
