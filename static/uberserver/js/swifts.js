$(document).ready(function() {


    $(".relay-control[data-swift-topic] > button").click(function () {
        let $this = $(this);
        let topic = $this.parent().data('swift-topic');

        $.post( "/api/mqtt/post", { topic: topic, payload: $this.val() })
            .fail(function() { alert( "error posting to swift" ) })
            .done(function( data ) { console.log( data ); });
    });

    function swiftStateRefrash() {
        if($("div").is($(".relay-control"))) {
            let $this = $(".relay-control[data-swift-topic]");
            $this.map(function (key, value) {
                let topic = $(value).data('swift-topic');
                let topic_check = $(value).data('swift-topic-check');
                let state_on = $(value).data('swift-on');
                let state_off = $(value).data('swift-off');

                $.get("/api/mqtt/get?topic="+topic_check, function (data) {
                    let state = 'none';
                    let payload = data[0]['payload'];
                    if(payload == state_on) {
                        state = 'On'
                    }
                    if(payload == state_off) {
                        state = 'Off'
                    }
                    $("span[data-swift-value='"+topic+"']").text(state);
                });

            });

            setTimeout(swiftStateRefrash, 10000);
        }
    }

    swiftStateRefrash();

});