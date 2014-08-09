/*
 * Proxy statistics
 * This is just a really quick and dirty implementation - _for demonstration purpose only_.
 */

ProxyStatsApp = function () {

    var self = this;
    this.apiUrl;
    this.container;
    this.interval = 30000;

    this.init = function () {
        self.load()
        if(self.interval){
            setInterval(function () {
                self.load();
            }, self.interval);
        }
    };


    this.load = function() {
        $.get(self.apiUrl, function(data) {
             self.display(data);
        });
    };

    this.display = function(data) {
        $.each(data, function(k, v) {
            $('#stats_' + k, self.container).html(v)
        })
    };
};