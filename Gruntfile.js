
module.exports = function(grunt) {

    grunt.initConfig({
        watch: {
            app_js: {
                //Watch js files for changes and run require on change
                files: [
                    'apps/**/static/**/*.js',
                    'yausite/assets/**/*.js'
                ],
                tasks: ['requirejs:compile_site', 'usebanner:compile_banner'],
                options: {
                    debounceDelay: 1000
                }
            },
            app_css: {
                //Watch css files for changes and run sass on change
                files: ['yausite/assets/sass/**/*.sass'],
                tasks: ['sass:compile_site'],
                options: {
                    debounceDelay: 1000
                }
            }
        },
        requirejs: {
            compile_site: {
                //Require JS compile task
                options: {
                    mainConfigFile: "yausite/assets/js/require_config.js",
                    optimize: 'none'
                }
            },
            optimize: {
                //Require JS compile task
                options: {
                    mainConfigFile: "yausite/assets/js/require_config.js",
                    optimize: 'uglify2'
                }
            },
        },
        sass: {
            compile_site: {
                options: {
                    style: 'expanded',
                    lineNumbers: true,
                    cacheLocation: 'yausite/static/.sass-cache'
                },
                files: {
                    'yausite/static/css/main.css': 'yausite/assets/sass/main.scss'
                }
            },
            optimize:{
                options: {
                    style: 'compressed',
                    cacheLocation: 'yausite/static/.sass-cache'
                },
                files: {
                    'yausite/static/css/main.css': 'yausite/assets/sass/main.scss'
                }
            }
        },
        copy: {
            //Copy require into built folder so it gets deployed
            require:{
                src: 'yausite/assets/js/vendor/requirejs/require.js',
                dest: 'yausite/static/js/require.js'
            },
            tostatic: {
                files: [
                    {
                        expand: true,
                        cwd: 'yausite/static/js/built',
                        src: '**',
                        dest: 'yausite/static/js/'
                    },
                    {
                        expand: true,
                        cwd: 'yausite/static/css/',
                        src: '**',
                        dest: 'yausite/css'
                    }
                ]
            }
        },
        bower: {
            install: {
                options: {
                    install: true,
                    copy: false //needed to stop premature exit (https://github.com/yatskevich/grunt-bower-task/issues/66)
                }
            }
        },
        usebanner:{
            compile_banner:{
                options:{
                    position: 'top',
                    banner: '/** <%= grunt.template.today("dd-mm-yyyy HH:MM:ss") %> **/',
                    linebreak: true,
                },
                files: {
                    src: ['yausite/static/js/main.js']
                }
            }
        },
        shell: {
            collectstatic: {
                 options: {
                    stdout: true
                },
                command: 'python manage.py collectstatic --noinput'
            },
        }
    });

    grunt.loadNpmTasks('grunt-contrib-requirejs');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-sass');
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-bower-task');
    grunt.loadNpmTasks('grunt-banner');
    grunt.loadNpmTasks('grunt-shell');

    //DEVELOPMENT
    grunt.registerTask('default', ['bower:install', 'copy:require', 'requirejs:compile_site', 'usebanner:compile_banner', 'sass:compile_site', 'watch']);

    //RUN PRE DEPLOY
    grunt.registerTask('deploy', ['shell:collectstatic', 'bower:install', 'copy:require', 'requirejs:optimize', 'usebanner:compile_banner', 'sass:optimize'])

};
