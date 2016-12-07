/**
 * Created by tianzhang on 2016/12/6.
 */
function close_self_iframe(frame_id, shadow_id) {
    $(frame_id, window.parent.document).eq(0).hide()
    $(frame_id, window.parent.document)[0].src = "#"
    $(shadow_id, window.parent.document).eq(0).css("opacity", "0").css("zIndex", "-1");
}

function resize_iframe(iframe_id, inner_id) {
    $("body").height($(inner_id).height());
    $("body").width($(inner_id).width());
    parent.changeheight(id = iframe_id, height = $("body").outerHeight(true))
    parent.changewidth(id = iframe_id, width = $("body").outerWidth(true))
}