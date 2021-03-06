/**
 * Require Config for yausite
 */
requirejs.config({
    name: 'yausite',
    out: '../../../static/js/yausite.js',
    paths: {
        jquery: '../vendor/jquery/dist/jquery',
        backbone: '../vendor/backbone/backbone',
        underscore: '../vendor/underscore/underscore',
        handlebars : '../vendor/handlebars/handlebars.amd',
        async : '../vendor/requirejs-plugins/src/async',
        goog : '../vendor/requirejs-plugins/src/goog',
        propertyParser : '../vendor/requirejs-plugins/src/propertyParser'
    }
});
