
function log(str) {
    console.log(str);
}

var allLeafNum;

var votes = {};

function initTimer() {
    updateMainTable();
    // call this method repeatedly.
    setTimeout(initTimer, 3000);
}

function updateResultTables() {
    var old_results = { "1": 0, "-1": 0, "0": 0 };
    var new_results = { "1": 0, "-1": 0, "0": 0 };
    var old_total = 0;
    var new_total = 0;
    $.each(votes, function(i, v) {
        k = "" + v.value;
        if (v.level && v.level == 1) {
            old_results[k] += 1;
            old_total += 1;
        }
        new_results[k] += 1;
        new_total += 1;
    });
    log("old: " + old_results["1"] + " vs " + old_results["-1"] + ", gg: " + old_results["0"]);
    log("new: " + new_results["1"] + " vs " + new_results["-1"] + ", gg: " + new_results["0"]);
    var old_u_ratio = (old_results["1"] / old_total * 100)
        var old_n_ratio = (old_results["0"] / old_total * 100)
        var old_d_ratio = (old_results["-1"] / old_total * 100)
        var new_u_ratio = (new_results["1"] / new_total * 100)
        var new_n_ratio = (new_results["0"] / new_total * 100)
        var new_d_ratio = (new_results["-1"] / new_total * 100)
        log("old: " + old_u_ratio + " vs " + old_d_ratio);
    log("new: " + new_u_ratio + " vs " + new_d_ratio);
    $("#old_result div.cUp").width(old_u_ratio + "%");
    $("#old_result div.cNeu").width(old_n_ratio + "%");
    $("#old_result div.cDown").width(old_d_ratio + "%");
    $("#new_result div.cUp").width(new_u_ratio + "%");
    $("#new_result div.cNeu").width(new_n_ratio + "%");
    $("#new_result div.cDown").width(new_d_ratio + "%");
    $("#old_result div.cUp").text(old_results["1"] + "(" + ratioStr(old_u_ratio) + ")");
    $("#old_result div.cNeu").text(old_results["0"] + "(" + ratioStr(old_n_ratio) + ")");
    $("#old_result div.cDown").text(old_results["-1"] + "(" + ratioStr(old_d_ratio) + ")");
    $("#new_result div.cUp").text(new_results["1"] + "(" + ratioStr(new_u_ratio) + ")");
    $("#new_result div.cNeu").text(new_results["0"] + "(" + ratioStr(new_n_ratio) + ")");
    $("#new_result div.cDown").text(new_results["-1"] + "(" + ratioStr(new_d_ratio) + ")");

}

function ratioStr(ratio) {
    return ("" + ratio).substr(0, 4) + "%";
}

function updateMainTable() {
    log("updateMainTable called");
    $.getJSON('/voted_list', function(data) {
        log("votedlist get success");
        votes = data.votes;
        updateResultTables();
        $.each(votes, function(i, v) {
            if(v.value == 1) { 
                $.each($("#table td"), function() {
                    if ($(this).html() == v.name) {
                        $(this).css("background-color", "blue");
                    }
                });
            } else if(v.value == 0) {
                $.each($("#table td"), function() {
                    if($(this).html() == v.name) {
                        $(this).css("background-color", "gray");
                    }
                });
            } else if(v.value == -1) {
                $.each($("#table td"), function() {
                    if($(this).html() == v.name) {
                        $(this).css("background-color", "red");
                    }
                });
            }
            //log(v.name + " voted for " + v.value);
        });
    });
}

function loadData() {
	$.getJSON("/hier_json", function(hier) {
		var maxLevel = hier["max_level"] + 1;
		log(maxLevel);
		var names = []
		delete hier["max_level"];
		var users = {} // user_id, user
		$.each(hier, function(k, v) {
			$.each(v, function(k2, v2) {
				v2._parent = k;
				users[v2.user_id] = v2;
			});
		});
		var levels = {};
		for (var i = 0; i < maxLevel; ++i) {
			levels[i] = [];	
		}
		$.each(users, function(k, user) {
			levels[user.level][levels[user.level].length] = user;
			names[names.length] = user.name;
		});
		var row0 = table.insertRow(0);
		var cell00 = $(row0.insertCell(0));
		function calcColspan(u) {
			if (!hier[u.user_id])
				return 1;
			var span = 0;
			$.each(hier[u.user_id], function(k, v) {
				span += calcColspan(v);
			});
			return span;
		}
		function setCellAttrs(c, u) {
			c.text(u.name);
			c.attr("colspan", calcColspan(u));
			c.attr("citizen_name", u.name);
		}
		cell00.text(hier[0][0].name);
		cell00.attr("colspan", calcColspan(hier[0][0]));
		cell00.attr("citizen_name", hier[0][0].name);

		for(var i = 1; i < maxLevel; i++) {
			cols = levels[i];
			var row = table.insertRow(i);

			for(var j = 0; j < cols.length; j++) {
				var cell = $(row.insertCell(j));
				setCellAttrs(cell, cols[j]);
			}
		}

		names.sort();
		$.each(names, function(k, v) {
			var optionElem = $("<option></option>").text(v);
			$("#voter_name").append(optionElem);
		});


	});
}

function loadData2() {
    var names = [];
    allLeafNum = $("#hier > div > div > div").length;
    var seniors = $("#hier > div > div");

    var president = $("#hier > div");
    var senior = $("#hier > div > div");
    var citizen = $("#hier > div > div > div");

    var presidentCount = president.length;
    var seniorCount = senior.length;
    var citizenCount = citizen.length;

    var senior_leafnums = seniors.length;

    var presidentColspan;
    var seniorColspan = [];
    $.each(president, function(index, value) { presidentColspan=$(value).find(".citizen").length; });
    $.each(senior, function(index, value) { seniorColspan[index]=$(value).find(".citizen").length; });

    console.log("presidentColspan: " + presidentColspan);
    console.log("seniorColspan: " + seniorColspan);

    var trNum = [];
    trNum[0] = presidentCount;
    trNum[1] = seniorCount;
    trNum[2] = citizenCount;

    var maxLevel = 0;
    $.each($("#hier div"), function(i, v) {
        v._colspan = $(v).find("div:not(:has(>div))").length;
        v._level = 0;
        var cur = $(v);
        while (cur.is("div.citizen")) {
            v._level += 1;
            cur = cur.parent();
        }
        if (maxLevel < v._level) maxLevel = v._level;
        // log(v._level + ", " + v._colspan);
        var name = $(v).find(">span").text();
        var optionElem = $("<option></option>").text(name);
        $("#voter_name").append(optionElem);

        $(v).attr("_level", v._level);
        $(v).attr("_colspan", v._colspan);
    });


    var table = document.getElementById("table");

    var depth = $(".citizen").parents("*").not("body,html").size();
    log("depth: " + maxLevel);
    for(var i = 0; i < maxLevel; i++) {

        cols = $("#hier").find("div[_level="+(i+1)+"]");

        var row = table.insertRow(i);

        for(var j = 0; j < cols.length; j++) {
            var cell = $(row.insertCell(j));
            var name = $(cols[j]).find(">span").text();
            cell.text(name);
            cell.attr("colspan", cols[j]._colspan);
            cell.attr("citizen_name", cols[j].name)
        }

    }

}

$(document).ready(function() {
    loadData();
    initTimer();
    $("form button").click(function(event) {
        event.preventDefault();
        var votedValue = this.value;
        var name = $("#voter_name").val();
        var subj = $("#vote_subject").val();
        $.get("/voting", { name: name, subject: subj, value: this.value })
            .done(function(data) {
                log("voting succeeded for " + votedValue);
                updateMainTable();
            })
        return false;
    });
});

