// 纯JS省市区三级联动
// 2011-11-30 by http://www.cnblogs.com/zjfree
var birthdayInit = function (cmbYear, cmbMonth, cmbDay) {
    var cmbYear = document.getElementById(cmbYear);
    var cmbMonth = document.getElementById(cmbMonth);
    var cmbDay = document.getElementById(cmbDay);

    cmbAddOption(cmbYear, "年", "");
    for (var i = 1900; i < 2100; i++) {
        cmbAddOption(cmbYear, i, i);
    }

    cmbAddOption(cmbMonth, "月", "");
    for (var i = 1; i < 13; i++) {
        cmbAddOption(cmbMonth, i, i);
    }

    cmbAddOption(cmbDay, "日", "");
    cmbSelect(cmbYear, 0);
    cmbSelect(cmbMonth, 0);
    cmbSelect(cmbDay, 0);
    cmbMonth.onchange = changeDay;
    cmbYear.onchange = changeDay;

    function cmbSelect(cmb, str) {
        cmb.selectedIndex = str;

    }

    function cmbAddOption(cmb, text, value) {
        var option = document.createElement("OPTION");
        cmb.options.add(option);
        option.innerHTML = text;
        option.value = value;
    }

    function changeDay() {
        cmbDay.options.length = 1;
        if (cmbYear.selectedIndex) {
            if (cmbMonth.selectedIndex) {
                if (["1", "3", "5", "7", "8", "10", "12"].indexOf(cmbMonth.value)!=-1) {
                    for (i = 1; i < 32; i++) {
                        cmbAddOption(cmbDay, i, i);
                    }
                }
                if (["4", "6", "9", "11"].indexOf(cmbMonth.value)!=-1) {
                    for (i = 1; i < 31; i++) {
                        cmbAddOption(cmbDay, i, i);
                    }
                }
                if (cmbMonth.value == "2") {
                    if (cmbYear.value % 4) {
                        for (i = 1; i < 29; i++) {
                            cmbAddOption(cmbDay, i, i);
                        }
                    }
                    else {
                        for (i = 1; i < 30; i++) {
                            cmbAddOption(cmbDay, i, i);
                        }
                    }
                }
            }
        }
    }

}
