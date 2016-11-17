/**
 * Created by Administrator on 2016/11/8/008.
 */
String.prototype.replaceAll = function (s1, s2) {
    return this.replace(new RegExp(s1, "gm"), s2);
}

function show_blog_detail(dom) {
    $("#blog_list_outer").animate({
        margin: 0,
        width: document.body.clientWidth * 0.4
    }, "slow").css("float", "left");
    $blog_detail_outer = $("<div>aaa</div>")
    $blog_detail_outer.id = 'blog_detail_outer';
    $blog_detail_outer.className = "list_outer";
    $blog_detail_outer.css("margin", "0").css("float", "left");
    $("body").append($blog_detail_outer)


}