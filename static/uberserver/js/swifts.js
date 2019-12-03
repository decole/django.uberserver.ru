$(document).ready(function() {


    $(".relay-control[data-swift-topic]").click(function () {
        let $this = $(this);
        alert('click!');
        /*
        $.get("/api/relay-set?a="+$this.data("id")+"&r="+Number(!$this.hasClass("on")), function (data) {
            $(".relay-status[data-id='"+$this.data("id")+"']").text(re(data));
            if (data == 0) {
                $this.removeClass("on").addClass("off");
            }
            if (data == 1) {
                $this.removeClass("off").addClass("on");
            }
        });
        */
    });

});