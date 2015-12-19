
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
    $.getJSON('/voted_list/', function(data) {
        log("votedlist get success");
        votes = data;
		new_votes = {};
		$.each(votes, function(k, v) {
			new_votes[Number(k)] = v;
		});
		votes = new_votes;
        updateResultTables();
		function getEffectiveVote(user_id) {
			var pid = users[user_id]._parent;
			var cnt = 0;
			while (pid != undefined && pid != 0) {
				if (votes[pid].value != 0)
					return votes[pid].value
				pid = users[pid]._parent;
			}
			return 0;
		}
		function clearClass(elem) {
			$(elem).removeClass("up");
			$(elem).removeClass("gray");
			$(elem).removeClass("down");
			$(elem).removeClass("gray inhr_up");
			$(elem).removeClass("gray inhr_down");
		}

        $.each(data, function(i, v) {
			var name = name;
            if(v.value == 1) { 
                $.each($("#table td[user_id="+i+"]"), function() {
					clearClass(this);
					$(this).addClass("up");
				});
			} else if(v.value == 0) {
				$.each($("#table td[user_id="+i+"]"), function() {
					clearClass(this);
					$(this).addClass("gray");
					var v = getEffectiveVote($(this).attr("user_id"));
					if (v == 1) 
						$(this).addClass("gray inhr_up");
					else if (v == -1)
						$(this).addClass("gray inhr_down");
				});
			} else if(v.value == -1) {
				$.each($("#table td[user_id="+i+"]"), function() {
					clearClass(this);
					$(this).addClass("down");
				});
            }
            //log(v.name + " voted for " + v.value);
        });
    });
}

var names = [];
var users = {};
var levels = {};

function loadData() {
	$.getJSON("/hier_json/", function(hier) {
		var maxLevel = hier["max_level"] + 1;
		log(maxLevel);
		names = [];
		delete hier["max_level"];
		users = {} // user_id, user
		$.each(hier, function(k, v) {
			$.each(v, function(k2, v2) {
				v2._parent = k;
				users[v2.user_id] = v2;
			});
		});
		levels = {};
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
			c.attr("user_id", u.user_id);
		}
		setCellAttrs(cell00, hier[0][0]);

		for(var i = 1; i < maxLevel; i++) {
			var row = table.insertRow(i);
			levels[i-1].sort(function(o1, o2) {
				return o1.name.localeCompare(o2.name);
			});
			var cellCount = 0;
			for (var k = 0; k < levels[i-1].length; ++k) {
				cols = hier[levels[i-1][k].user_id];

				log(cols);
				cols.sort(function(o1, o2) {
					return o1.name.localeCompare(o2.name);
				});
				for(var j = 0; j < cols.length; j++) {
					var cell = $(row.insertCell(cellCount++));
					setCellAttrs(cell, cols[j]);
				}
			}
		}

		names.sort();
		$.each(names, function(k, v) {
			var optionElem = $("<option></option>").text(v);
			$("#voter_name").append(optionElem);
		});
		initTimer();
	});
}

$(document).ready(function() {
    loadData();
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
    });
	$("#btn_refresh").click(function(event) {
		event.preventDefault();
		updateMainTable();
	});
});

