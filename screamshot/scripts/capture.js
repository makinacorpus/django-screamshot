var casper = require("casper").create({
    //verbose: true,
    //logLevel: 'debug',
    onError: function(self, m) {   // Any "error" level message will be written
        console.log('FATAL:' + m); // on the console output and PhantomJS will
        self.exit();               // terminate
    },
});

casper.on('remote.message', function (msg) {
    casper.log(msg, 'error');
});

function pageerror(resource) {
    casper.log('Cannot open ' + resource.url, 'error');
};
casper.on('load.failed', pageerror);
casper.on('http.status.404', pageerror);
casper.on('http.status.500', pageerror);


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
          height = casper.cli.options.height || 900;
    casper.options.viewportSize = {width: width, height: height};
    
    data = JSON.parse(data);
    
    casper.start();
 
    casper.open(address, {
        method: method,
        data: data
    });
    
    casper.then(function() {
        if(selector) {
            if (this.exists(selector)) {
                this.captureSelector(output, selector);
            }
            else {
                this.die("Selector " + selector + " not found in page.", 1);
            }
        } else {
            this.capture(output);
        }
    });
    
    casper.run();
}
