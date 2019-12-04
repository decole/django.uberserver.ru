function re(data) {
    if (data == 0) return "off";
    if (data == 1) return "on";
}

function clearNotify() {
    $('span.label.label-warning.notifyIconInfo').remove();
    $.get("/api/notifySite?action=clear&value=all", function (data) {
        if (data === 'ok') {
            $('ul.menu').remove();
            $("ul.dropdown-menu>li.header").html('You have 0 notifications');
        }
        if (data !== 'ok') {
            alert('warning, note clear notify!');
        }
    });
}

$(document).ready(function () {
    $(".relay-control[data-id]").click(function () {
        let $this = $(this);
        $.get("/api/relay-set?a="+$this.data("id")+"&r="+Number(!$this.hasClass("on")), function (data) {
            $(".relay-status[data-id='"+$this.data("id")+"']").text(re(data));
            if (data == 0) {
                $this.removeClass("on").addClass("off");
            }
            if (data == 1) {
                $this.removeClass("off").addClass("on");
            }
        });

    });

    $(".emergencyStop[data-id]").click(function () {
        let action
        let $this = $(this);
        action = 'on';
        if($(".stateEmergencyStop").hasClass("bg-yellow") || $(".stateEmergencyStop").hasClass("bg-green")) {
            action = 'on';
        }
        if($(".stateEmergencyStop").hasClass("bg-red")) {
            action = 'off';
        }
        $.get("/api/emergency-stop?action="+action+"&topic="+$this.data("id"), function (data) {
            if (data == 0) {
                $(".stateEmergencyStop").removeClass("bg-yellow").removeClass("bg-red").addClass("bg-green");
            }
            if (data == 1) {
                $(".stateEmergencyStop").removeClass("bg-yellow").removeClass("bg-green").addClass("bg-red");
            }
        });
    });

    function leakage() {
        if($("div").is($(".leakage-control[data-id]"))) {
            let $this = $(".leakage-control[data-id]");
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
            setTimeout(leakage, 10000);
        }
    }

    leakage();

    function stateRelays() {
        $(".relay-control[data-id]").map(function (key, value) {
            topic = $(value).data("id");
            $.get("/api/relay-state?topic="+topic, function (data) {
                if (data == 1) {
                    $(value).parent().removeClass("bg-yellow").removeClass("bg-red").addClass("bg-green");
                    $(value).parent().find( "p.relay-status" ).text('on');
                    $(value).parent().find( "a" ).removeClass('off').addClass('on');
                }
                if (data == 0) {
                    $(value).parent().removeClass("bg-yellow").removeClass("bg-green").addClass("bg-red");
                    $(value).parent().find( "p.relay-status" ).text('off');
                    $(value).parent().find( "a" ).removeClass('on').addClass('off');
                }
            });
        });
        setTimeout(stateRelays, 5000);
    }

    stateRelays();

// use chart.js to make cool graphics
    var charter = $('.sensorchart[data-topic]');
    var chartTopic = []; // topics array with objects chart.js and lineCharts for chartjs
    var chartOptions = {
        legend:false,
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:false
                }
            }],
            xAxes: [{
                display: false
            }]
        },
    };

    function renderDate(charter, date, chartTopic){
        charter.map(function (key, value) {
            if(!date){
                date = 'current';
            }

            var nameTopic = $(value).data('topic');
            var topic = value['id'];
            var ctx = document.getElementById(topic);

            if (date === 'current') {
                $.get('/api/chart', {'date': 'current', 'topic': nameTopic}).done(function (dataChart) {
                    chartTopic[nameTopic] = new Chart(ctx, {
                        type: 'line',
                        data:  dataChart,
                        options: chartOptions,
                    });
                });
            }
            else {
                $.get('/api/chart', {'date': date, 'topic': nameTopic}).done(function (dataChart) {
                    // addData(chartTopic[nameTopic],dataChart['labels'],dataChart['datasets'])
                    // chartTopic[nameTopic].clear();
                    chartTopic[nameTopic].config.data = dataChart;
                    chartTopic[nameTopic].update();
                });
            }

        });
    }

    renderDate(charter, 'current', chartTopic);

    function isCurrentDateForm() {
        if ($('#isDate').val() == 'current') {
            $('#isDate').val(0);
            console.log($('#isDate').val(0));
        }
    }

    function prevDate() {
        //http://momentjs.com/docs/#/parsing/date/
        isCurrentDateForm();
        var date = $('#isDate').val();
        date--;
        $('#isDate').val(date);
        date = date * (-1);
        date = moment().subtract(date, 'days').format('YYYY-MM-DD');
        console.log(date);
        $(".dateIs").html(date);
        renderDate(charter, date, chartTopic);
    }

    function nextDate() {
        //http://momentjs.com/docs/#/parsing/date/
        isCurrentDateForm();
        var date = $('#isDate').val();
        date++;
        $('#isDate').val(date);
        date = moment().add(date, 'days').format('YYYY-MM-DD');
        console.log(date);
        $('.dateIs').html(date);
        renderDate(charter, date, chartTopic);
    }

    $('#prev-date').click(function(){ prevDate(); });
    $('#next-date').click(function(){ nextDate(); });

    function stateSensors() {
        $(".sensor-state[data-topic]").map(function (key, value) {
            topic = $(value).data("topic");
            $.get("/api/sensor-state?topic="+topic, function (data) {
                $(value).html(data);
            });
        });
        setTimeout(stateSensors, 20000);
    }

    stateSensors();

    $(".timer-click").click(function () {
        const parent = $(this).parent();
        const el = $(this);
        let id = parent.data("id");
        let minutes = parent.find( "select" ).val();
        $.get("/api/addTimer?id="+id+"&minutes="+minutes, function (data) {
            if (data === 'ok') {
                setTimeout(getTimer, 1500);
            }
        });

    });

    function getTimer() {
        $(".timer-control").map(function (key, value) {
            let id = $(value).data("id");
            let timer = [];
            let timeIntervalTicker = [];
            $.get("/api/getTimer?id="+id, function (data) {
                if(data['active'] === 1) {
                    timer[id] = data['seconds'];
                    timeIntervalTicker[id] = setInterval(function run(){
                        $(value).find("span.timer-information").text(timer[id]);
                        timer[id] = timer[id] - 1;
                        if( timer[id] < 0 ) {
                            clearTimeout(timeIntervalTicker[id]);
                            $(value).find("span.timer-information").text('off');
                            $(value).removeClass("bg-yellow").removeClass("bg-green").addClass("bg-red");
                        }
                    }, 1000);
                    $(value).removeClass("bg-yellow").removeClass("bg-red").addClass("bg-green");
                }
                if(data['active'] === 0) {
                    $(value).find("span.timer-information").text('off');
                    $(value).removeClass("bg-yellow").removeClass("bg-green").addClass("bg-red");
                }
            });
        });
    }

    if($(".timer-control").length) {
        getTimer();
    }


});
