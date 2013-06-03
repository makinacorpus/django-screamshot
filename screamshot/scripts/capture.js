var casper = require("casper").create({
    //verbose: true,
    //logLevel: 'debug',
    onError: function(self, m) {   // Any "error" level message will be written
        console.log('FATAL:' + m); // on the console output and PhantomJS will
        self.exit();               // terminate
    },
});

function pageerror(resource) {
    casper.log('Cannot open ' + resource.url, 'error');
};
casper.on('load.failed', pageerror);
casper.on('http.status.404', pageerror);
casper.on('http.status.500', pageerror);

function capture(context, selector, output) {
    if(selector) {
        if (context.exists(selector)) {
            context.captureSelector(output, selector);
        }
        else {
            context.die("Selector " + selector + " not found in page.", 1);
        }
    } else {
        context.capture(output);
    }
}


if (casper.cli.args.length < 2 || casper.cli.args.length > 2) {
    console.error('Usage: capture.js URL FILE [OPTIONS]');
    casper.exit();
}
else {
    var address = casper.cli.args[0],
        output = casper.cli.args[1];
    
    var method   = casper.cli.options.method || 'get',
      selector   = casper.cli.options.selector,
          data   = casper.cli.options.data || '{}',
          width  = casper.cli.options.width || 1400,
          height = casper.cli.options.height || 900,
         waitfor = casper.cli.options.waitfor;
    casper.options.viewportSize = {width: width, height: height};
    
    data = JSON.parse(data);
    
    casper.start();
 
    casper.open(address, {
        method: method,
        data: data
    });
    
    casper.thenEvaluate(function () {
        var bodyclass = document.querySelector('body').getAttribute('class');
        bodyclass = bodyclass + " screamshot";
        document.querySelector('body').setAttribute('class', bodyclass);
    });

    if(waitfor) {
        casper.waitForSelector(waitfor, function() {
            capture(this, selector, output);
        });
    } else {
        casper.then(function() {
            capture(this, selector, output);
        });
    }
    
    casper.run();
}
