var page = require('webpage').create(),
    system = require('system');

/** 
 * arguments:
 * [1] => URL
 * [2] => output. Use /dev/stdout if you want to capture.
 * [3] => size
 */

var address = system.args[1],
    output  = system.args[2];

config = {}
system.args.forEach(function(arg, i) {
    if (i > 2) {
        namev = arg.split('=');
        config[namev[0].replace('--', '')] = namev[1];
    }
});

var method = config.method || 'get',
     width = config.width || 1400,
    height = config.height || 1,
      wait = config.wait || 200;

/**
 * please note: the default height is intentionaly left as 1.
 * the thing is, if you skip the height, phantomjs falls back
 * to some default viewport. and that's not what we want. we
 * want to set the width, and let the height auto-calculate.
 */
page.viewportSize = {width: width, height: height}

format = config.format || 'png';

if (format == 'pdf') {
    page.paperSize = {
        format: 'A4',
        orientation: config.orientation || 'portrait',
        margin: config.margin || '0cm'
    }
}

page.open(address, function(status){
    if (status == 'success') {
        setTimeout(function(){
            page.render(output, {format: format});
            phantom.exit();
        }, wait);
    }
});
