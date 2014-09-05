var casper = require("casper").create({
    colorizerType: 'Dummy',  // no colors
});


function on_load_error(resource) {
    this.echo("ERROR: " + 'Cannot open ' + resource.url, "ERROR");
}
casper.on('load.failed', on_load_error);
casper.on('http.status.404', on_load_error);
casper.on('http.status.500', on_load_error);


casper.on('remote.message', function on_page_message(msg) {
    this.echo("INFO: " + msg);
});
casper.on('page.error', function on_page_error(msg, trace) {
    this.echo("ERROR: " + msg, "ERROR");

    for(var i=0; i<trace.length; i++) {
        var step = trace[i];
        this.echo('ERROR:      ' + step.file + ' (line ' + step.line + ')', "ERROR");
    }
});
casper.on('error', function on_script_error(msg, trace) {
    this.echo('FATAL: ' + msg, "ERROR");
    this.exit(1);
});


function capture(selector, output) {
    if(selector) {
        if (casper.exists(selector)) {
            casper.captureSelector(output, selector);
        }
        else {
            casper.emit('error', "Selector " + selector + " not found in page.");
        }
    } else {
        casper.capture(output);
    }
}


if (casper.cli.args.length < 2 || casper.cli.args.length > 2) {
    console.error('Usage: capture.js URL FILE [OPTIONS]');
    casper.exit();
}
else {
    var address = casper.cli.args[0],
        output = casper.cli.args[1];

    var method = casper.cli.options.method || 'get',
      selector = casper.cli.options.selector,
          data = casper.cli.options.data || '{}',
         width = casper.cli.options.width || 1400,
        height = casper.cli.options.height || 900,
       waitfor = casper.cli.options.waitfor,
          wait = casper.cli.options.wait;
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

    if (waitfor) {
        casper.waitForSelector(waitfor, function() {
            capture(selector, output);
        });
    } else if (wait) {
        casper.wait(wait, function() {
            capture(selector, output);
        });
    } else {
        casper.then(function() {
            capture(selector, output);
        });
    }

    casper.run();
}
