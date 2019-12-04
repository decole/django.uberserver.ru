$(document).ready(function() {

    function sensorsRefrash() {
        if($("div").is($(".sensor-control"))) {
            let $this = $(".sensor-control[data-sensor-topic]");
            $this.map(function (key, value) {
                console.log($(value).data('sensor-topic'));
            });
            // $(".sensor-control[data-sensor-topic]").data()
            /*
            $.get("/api/leakage?topic="+$this.data("id"), function (data) {
                if (data == 0) {
                    $(".leakage-status[data-id='"+$this.data("id")+"']").text("Норма");
                    $this.removeClass('bg-yellow').removeClass('bg-red').addClass('bg-green');
                }
                if (data == 1) {
                    $(".leakage-status[data-id='"+$this.data("id")+"']").text("Протечка");
                    $this.removeClass('bg-yellow').removeClass('bg-green').addClass('bg-red');
                    console.log("alarma!");
                    $('#carteSoudCtrl')[0].play();
                }
            });
            */
            setTimeout(sensorsRefrash, 10000);
        }
    }

    sensorsRefrash();

});