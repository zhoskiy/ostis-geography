module.exports = function (grunt) {
    const storesDirPath = './stores/';

    const scWebDirPath = '../../../ostis-web-platform/sc-web';
    const clientJsDirPath = scWebDirPath + '/client/static/components/js/';
    const clientCssDirPath = scWebDirPath + '/client/static/components/css/';
    const clientHtmlDirPath = scWebDirPath + '/client/static/components/html/';
    const clientImgDirPath = scWebDirPath + '/client/static/components/images/';
    const kbPath = '../../../kb/';

    grunt.initConfig({
        concat: {
            stores: {
                src: [storesDirPath + 'src/*.js'],
                dest: storesDirPath + 'static/js/stores.js'
            },
        },
        copy: {storesJs: {
                cwd: storesDirPath + 'static/js/',
                src: 'stores.js',
                dest: clientJsDirPath + 'stores/',
                expand: true,
                flatten: true
            },
            storesCss: {
                cwd: storesDirPath + 'static/css/',
                src: '*.css',
                dest: clientCssDirPath,
                expand: true,
                flatten: true
            },
            storesHtml: {
                cwd: storesDirPath + 'static/html/',
                src: ['*.html'],
                dest: clientHtmlDirPath,
                expand: true,
                flatten: true
            },
            storesImg: {
                cwd: storesDirPath + 'static/images/',
                src: '*.png',
                dest: clientImgDirPath + 'stores/',
                expand: true,
                flatten: true
            },
            storesKb: {
                cwd: storesDirPath + 'kb/',
                src: '*.scs',
                dest: kbPath + 'stores/',
                expand: true,
                flatten: true
            },
        },
        watch: {
            storesJs: {
                files: storesDirPath + 'src/**',
                tasks: ['concat:stores', 'copy:storesJs'],
            },
            storesCss: {
                files: storesDirPath + 'static/css/**',
                tasks: ['copy:storesCss'],
            },
            storesHtml: {
                files: [storesDirPath + 'static/html/**'],
                tasks: ['copy:storesHtml'],
            },
            storesImg: {
                files: [storesDirPath + 'static/images/**'],
                tasks: ['copy:storesImg'],
            },
        },
        exec: {
            updateCssAndJs: 'sh scripts/update_css_and_js.sh'
        }
    });

    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-exec');

    grunt.registerTask('default', ['concat', 'copy', 'exec:updateCssAndJs', 'watch']);
    grunt.registerTask('build', ['concat', 'copy', 'exec:updateCssAndJs']);

};
