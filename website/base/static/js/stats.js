/*
 * Proxy statistics
 */

ProxyStatsApp = function () {

    var self = this;
    this.apiUrl;
    this.container;
    this.interval = 5000;

    this.init = function () {

        self.load()
        if(self.interval){
            setInterval(function () {
                self.load();
            }, self.interval);
        }

    }


    this.load = function() {
        $.get(self.apiUrl, function(data) {
             self.display(data);
        });
    }

    this.display = function(data) {

        $.each(data, function(k, v) {
            console.log('k', k, 'v', v);

            $('#stats_' + k, self.container).html(v)

        })

    }

}