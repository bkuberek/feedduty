/**
 * main.js
 * Copyright: © 2013 Bastian Kuberek
 */


(function () {
  'use strict';

  var packages = [
    {name: 'app'}
  ];

  requirejs.config({
    packages: packages,
    paths: {
      jquery: 'lib/jquery/jquery-2.0.3.min',
//      jquerylayout: 'lib/jquery/jquery.layout',
//      cookie      : 'lib/jquery/jquery.cookie',
//      pubsub      : 'lib/jquery/jquery.pubsub',

//      qtip      : 'plugins/qtip/jquery.qtip.min',
//      pnotify   : 'plugins/pnotify/jquery.pnotify.min',
//      iosfix    : 'plugins/ios-fix/ios-orientationchange-fix',
//      totop     : 'plugins/totop/jquery.ui.totop.min',
//      touchpunch: 'plugins/touch-punch/jquery.ui.touch-punch.min',
//      validate  : 'plugins/validate/jquery.validate.min',
//      uniform   : 'plugins/uniform/jquery.uniform.min',

//      underscore: 'libs/underscore/underscore-min',
//      backbone  : 'libs/backbone/backbone-min',
      bootstrap: 'lib/bootstrap/bootstrap.min',
      dust: 'lib/dust/dust-full2.0.0.min',

      text: 'lib/require/text',
      templates: '../app/templates'
    },
    shim: {
      jquery: {exports: 'jQuery'},
//      underscore: {exports: '_'},
      bootstrap: {exports: 'Bootstrap'},
      handlebars: {exports: 'Handlebars'},
      dust: {exports: 'dust'}
//      backbone: {
//        deps: ['underscore', 'jquery'],
//        exports: 'Backbone'
//      },
//      jquerylayout: ['jquery'],
//      pubsub: ['jquery'],
//      cookie: ['jquery'],
//      qtip: ['jquery'],
//      pnotify: ['jquery'],
//      validate: ['jquery'],
//      uniform: ['jquery']
    }
  });

})();

require([
  'app',
], function (app) {
  'use strict';



});
