/**
 * Require Config for yausite
 */
requirejs.config({
    name: 'yausite',
    out: '../../static/js/yausite.js',
    paths: {
        jquery: 'vendor/jquery/dist/jquery',
        sammy : 'vendor/sammy/lib/sammy',
        handlebars : 'vendor/handlebars/handlebars.amd'
    }
});
