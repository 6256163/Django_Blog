/**
 * Created by Administrator on 2016/11/8/008.
 */


String.prototype.replaceAll = function (s1, s2) {
    return this.replace(new RegExp(s1, "gm"), s2);
};

$(document).ready(function () {
    var current_blog_url = "";

    // blog list 翻页
    $("form#blog_list_page_turn").submit(function () {
        var validate_data = $("form#blog_list_page_turn").find("input").val();
        if (isNaN(validate_data)) {
            return false;
        }
        else if (validate_data > parseInt($("form#blog_list_page_turn").find("p").text())) {
            return false;
        }
        else {
            $.ajax({
                type: "GET",
                url: "/blog/?page=" + $("form#blog_list_page_turn").find("input").val(),
                contentType: "application/json",
                data: {},
                dataType: "json",
                success: function (response_data) {
                    load_blog_list(response_data)

                }
            });
            return false;
        }

    });


    // 提交新blog
    $("button#post_blog").click(function () {
        var blogtext = "";
        for (var i = 0; i < $("#blog_text").contents().length; i++) {
            if ($("#blog_text").contents()[i].nodeName == "IMG") {
                blogtext += $("#blog_text").contents()[i].outerHTML;
            }
            if ($("#blog_text").contents()[i].nodeName == "#text") {
                blogtext += $("#blog_text").contents()[i].data + "\n";
            }
            if ($("#blog_text").contents()[i].nodeName == "DIV") {
                blogtext += $("#blog_text").contents()[i].innerText + (($("#blog_text").contents()[i].innerText == "\n") ? "" : "\n");
            }

        }

        $.ajax({
            type: "POST",
            url: "",
            data: JSON.stringify({
                "blog_title": $("#blog_title").val(),
                "blog_text": blogtext
            }),
            contentType: "application/json",
            dataType: "json",
            success: function (msg) {
                var data = {"href": msg.blog.url};
                show_blog_detail(data);

            }
        });
    });

})


function get_right(dom) {
    var detail_page_x = dom.offset().left + dom.outerWidth();
    var detail_page_w = document.body.clientWidth - detail_page_x;
    var detail_page_y = dom.offset().top;
    return {x: detail_page_x, y: detail_page_y, w: detail_page_w}
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
function load_blog_title(response_data){
    var $blog_title = $('<div class="blog_detail_title" style="display: none;">' +
        '<strong> <p id="blog_title">' + response_data.blog.blog_title + '</p> </strong> </div>');

    $("#blog_detail_outer").append($blog_title);
    $blog_title.slideDown();
}

function load_blog_detail(response_data) {
    //动态添加blog detail


    var $blog_detail = $('<div class="hidden">' +
        '<div class="user_info_outer">' +
        '<div class="lz_corner">楼主 </div>' +
        '<div style="text-align:center;margin:10px">' +
        '<p><img class="head_img" src="' + response_data.blog.head_img + '"width="100" height="100"/></p>' +
        '</div><div style="text-align:center"><p><a>' + response_data.blog.user +
        '</a></p></div></div><div class="blog_text_outer"><div class="blog_text">' +
        '<p id="blog_text">' + response_data.blog.blog_text +
        '</p></div><div class="blog_detail_info hidden"><div id="blog_reply_button"style="float:right;">' +
        '<p><a> 回复 </a>   </p></div><div style="float:right"><p>' + response_data.blog.pub_date.substr(5, 5) + ' ' + response_data.blog.pub_date.substr(11, 5) +
        '</p></div><div style="float:right"><p>1 楼</p></div></div> </div></div>')

    $("#blog_detail_outer").append($blog_detail);
    $blog_detail.slideDown();
}

function load_replies_detail(response_data) {
    //动态添加replies detail
    for (var i = 0; i < response_data.replies.results.length; i++) {
        var $reply_detail = $('<div style="overflow:hidden;border-top:solid 1px #999999;">' +
            '<div class="user_info_outer"><div id="lz"+"' + i + '" class="lz_corner">楼主</div><div style="text-align:center;margin:10px"><p >' +
            '<img class="head_img" src=' + response_data.replies.results[i].head_img + ' width="100" height="100"/>' +
            '</p></div><div style="text-align:center"><p ><a>' + response_data.replies.results[i].user +
            '</a></p></div></div><div class="blog_text_outer"><div class="blog_text">' +
            '<p class="reply_text" id="reply_text">' + response_data.replies.results[i].reply_text +
            '</p></div><div class="blog_detail_info hidden">' +
            '<div onclick="hide_replay(this)" id="hide_reply_index" class="hide_reply_index">' +
            '<p >收起回复</p></div><div onclick="show_reply(this,reply_id=' + response_data.replies.results[i].id +
            ')" id="reply_button" style="float:right;" name="on"><p > <a>回复</a>(' + response_data.replies.results[i].reply_counter + ')</p>' +
            '</div><div style="float:right"><p >' + response_data.replies.results[i].pub_date.substr(5, 5) + ' ' + response_data.replies.results[i].pub_date.substr(11, 5) +
            '</p></div><div style="float:right"><p >' + (response_data.replies.results[i].floor + 1) + '楼  ' +
            '</p></div></div><div id="reply_in_reply" style="display:none"></div></div></div>')

        $("#blog_detail_outer").append($reply_detail);
        $reply_detail.slideDown();
    }
}


function load_replies_detail_pagination(response_data) {
//动态添加 分页
    var $reply_pagination_outer = $('<div class="page_outer hidden"></div>');
    var $page_previous = $('<div class="page_previous_next"></div>')
    var $turn_page = $('<div id=page></div>')
    var $page_next = $('<div class="page_previous_next"></div>')
    $reply_pagination_outer.append($page_previous);
    $reply_pagination_outer.append($turn_page);
    $reply_pagination_outer.append($page_next);

    var $turn_page_form = $('<form id="blog_detail_page_turn"></form>');
    $turn_page_form.appendTo($turn_page);
    var $turn_page_input = $('<input id="page_to_turn" style="width: 20px;float: left;padding: 0;height: 20px;" value="1"/>');
    $turn_page_input.appendTo($turn_page_form);
    var $turn_page_p = $('<p class="total_page" style="float: left;margin: 0">  </p>');
    $turn_page_p.text(Math.ceil(response_data.replies.count / 10));
    $turn_page_p.appendTo($turn_page_form);
    var $turn_page_button = $('<button type="submit" style="float: left">GO</button>');
    $turn_page_button.appendTo($turn_page_form);

    if (response_data.replies.previous) {
        $page_previous.append($('<a onclick="show_blog_detail(this);return false;"></a>').attr("href", response_data.replies.previous).text("上一页"))
        if(!response_data.replies.next){
            $turn_page_input.val(Math.ceil(response_data.replies.count / 10))
        }
        else{
            $turn_page_input.val(parseInt(response_data.replies.next.split("=")[1]) - 1)
        }
    }
    if (response_data.replies.next) {
        $page_next.append($('<a onclick="show_blog_detail(this);return false;"></a>').attr("href", response_data.replies.next).text("下一页"))
        if(!response_data.replies.previous){
            $turn_page_input.val(1)
        }
        else{
            $turn_page_input.val(parseInt(response_data.replies.previous.split("=")[1]) + 1)
        }
    }

    $("#blog_detail_outer").append($reply_pagination_outer);
    $reply_pagination_outer.slideDown();

//动态添加 回帖编辑框
    var $reply_blog_outer = $('<div></div>', {
        class: "post_blog_outer"
    });
    var $reply_blog_text = $('<div></div>').css("margin", "10px").html("<a><strong>发表回复</strong></a>").appendTo($reply_blog_outer);
    var $reply_blog_editor_outer = $('<div></div>').css("margin", "10px").css("width", "90%").css("border", "1px solid black").appendTo($reply_blog_outer);
    var $insert = $('<div></div>').addClass("insert_media").appendTo($reply_blog_editor_outer);
    var $insert_img = $('<a id="a_insert_img">图片</a>').appendTo($insert);
    var $insert_vedio = $('<a>视频</a>').appendTo($insert);
    var $insert_music = $('<a>音乐</a>').appendTo($insert);
    var $insert_emoji = $('<a>表情</a>').appendTo($insert);
    var $insert_attach = $('<a>附件</a>').appendTo($insert);
    var reply_editor = $('<div id="reply_text_reply" name="reply_text" class="blog_text_edit" contenteditable="true"></div>').appendTo($reply_blog_editor_outer);
    var $at = $('<div style="display: none;"> <div>想用@提到谁？</div> <ul></ul> </div>').appendTo($reply_blog_editor_outer);
    var $topic = $('<div style="display: none;"> <div>添加什么话题?</div> <ul></ul> </div>').appendTo($reply_blog_editor_outer);
    var $reply_submit = $('<div> <button id="subbtn" title="Ctrl+Enter快捷发表">发 表 </button> </div> <br/>').appendTo($reply_blog_outer);

    $("#blog_detail_outer").append($reply_blog_outer);
    $reply_blog_outer.slideDown();


}

function show_blog_detail(dom) {
    $("#blog_detail_outer").children().remove()
    $("#blog_list_outer").animate({
        margin: 0,
        width: document.body.clientWidth * 0.4
    }, "slow", function () {
        $("#blog_detail_outer").css("left", get_right($("#blog_list_outer")).x).css("width", get_right($("#blog_list_outer")).w - 5).css("bottom", "0").css("top", $("#nav_in").height()).css("display", "block")
    }).css("float", "left");
    $("#sidebar").animate({
        left: document.body.clientWidth * 0.4,
        marginLeft: -$("#sidebar ul").outerWidth(),
        opacity: 0.3
    }, "slow")


    $.ajax({
        type: "GET",
        url: dom.href,
        contentType: "application/json",
        data: {},
        dataType: "json",
        success: function (response_data) {
            current_blog_url = response_data.blog.url;
            load_blog_title(response_data)
            load_blog_detail(response_data)
            load_replies_detail(response_data)
            //Blog图片处理
            show_blog_img("#blog_text", ".reply_text");
            load_replies_detail_pagination(response_data)

            //绑定事件 提交回复
            $("button#subbtn").one("click", function () {
                var replytext = "";
                for (var i = 0; i < $("#reply_text_reply").contents().length; i++) {
                    if ($("#reply_text_reply").contents()[i].nodeName == "IMG") {
                        replytext += $("#reply_text_reply").contents()[i].outerHTML;
                    }
                    if ($("#reply_text_reply").contents()[i].nodeName == "#text") {
                        replytext += $("#reply_text_reply").contents()[i].data + "\n";
                    }
                    if ($("#reply_text_reply").contents()[i].nodeName == "DIV") {
                        replytext += $("#reply_text_reply").contents()[i].innerText + (($("#blog_text").contents()[i].innerText == "\n") ? "" : "\n");
                    }

                }
                $.ajax({
                    type: "POST",
                    url: "/replies/",
                    data: JSON.stringify({
                        "blog": current_blog_url,
                        "reply_text": replytext
                    }),
                    contentType: "application/json",
                    dataType: "json",
                    success: function (msg) {
                        var data = {"href": msg.blog};
                        show_blog_detail(data);
                    }
                });
            });


            // 绑定事件 blog detail 翻页
            $("form#blog_detail_page_turn").one("submit", function () {
                var validate_data = $("form#blog_detail_page_turn").find("input").val();
                if (isNaN(validate_data)) {
                    return false;
                }
                else if (validate_data > parseInt($("form#blog_detail_page_turn").find("p").text())) {
                    return false;
                }
                else {
                    $.ajax({
                        type: "GET",
                        url: current_blog_url + "?page=" + $("form#blog_detail_page_turn").find("input").val(),
                        contentType: "application/json",
                        data: {},
                        dataType: "json",
                        success: function (response_data) {
                            $("#blog_detail_outer").children().remove()
                            $("#blog_list_outer").animate({
                                margin: 0,
                                width: document.body.clientWidth * 0.4
                            }, "slow", function () {
                                $("#blog_detail_outer").css("left", get_right($("#blog_list_outer")).x).css("width", get_right($("#blog_list_outer")).w - 5).css("bottom", "0").css("top", $("#nav_in").height()).css("display", "block")
                            }).css("float", "left");
                            $("#sidebar").animate({
                                left: document.body.clientWidth * 0.4,
                                marginLeft: -$("#sidebar ul").outerWidth(),
                                opacity: 0.3
                            }, "slow")
                            load_blog_title(response_data);
                            load_replies_detail(response_data);
                            //Blog图片处理
                            show_blog_img("#blog_text", ".reply_text");
                            load_replies_detail_pagination(response_data);


                        }
                    });
                    return false;
                }

            });

        }
    });
}

function load_blog_list(response_data) {
    var $blog_li = $('<li onmouseover="onmouseover_blog(this)" onmouseout="onmouseout_blog(this)"style="border-top:1px solid black"></li>')
    var $blog = $('<div class="hidden"></div>').appendTo($blog_li);
    var $bubble = $('<div class="reply_bubble" align="center"> <span id="reply_count" style="background:url(/static/blog/pic/reply_bubble.png); background-size:cover;"></span> </div>').appendTo($blog);
    var $blog_outer = $('<div class="blog_outer hidden"></div>').appendTo($blog);
    var $blog_info = $('<div class="hidden blog_info"></div>').appendTo($blog_outer);
    var $blog_title = $('<div class="text blog_title"> <a id="blog_title"  onclick="show_blog_detail(this);return false;"></a> </div>').appendTo($blog_info);
    var $blog_date = $('<div class="blog_date"> <p id="blog_date"></p> </div>').appendTo($blog_info);
    var $blog_user = $('<div class="text blog_user"> <p id="blog_user"></p> </div>').appendTo($blog_info);
    var $reply_info = $('<div class="hidden reply_info"></div>').appendTo($blog_outer);
    var $blog_text = $('<div class="blog_title" style="font-size:12px"> <div style="width: 95%;"> <p id="blog_text" class="text"></p> </div> </div>').appendTo($reply_info);
    var $reply_date = $('<div class="blog_date"> <p id="reply_date"> </p> </div>').appendTo($reply_info);
    var $reply_user = $('<div class="text blog_user" style=""> <p id="reply_user"> </p> </div>').appendTo($reply_info)

    //分页
    if (response_data.blog.previous) {
        $("#blog_list_previous_page")[0].innerHTML = '<a href="' + response_data.blog.previous + '" onclick="show_blog_list(this);return false;">上一页</a>';
        if (response_data.blog.previous.split("=")[1]) {
            $("form#blog_list_page_turn").find("input#page_to_turn").val(parseInt(response_data.blog.previous.split("=")[1]) + 1)
        }
    }
    else {
        $("#blog_list_previous_page")[0].innerHTML = '<a></a>';
    }
    if (response_data.blog.next) {
        $("#blog_list_next_page")[0].innerHTML = '<a href=' + response_data.blog.next + ' onclick="show_blog_list(this);return false;">下一页</a>';
        if (response_data.blog.next.split("=")[1]) {
            $("form#blog_list_page_turn").find("input#page_to_turn").val(parseInt(response_data.blog.next.split("=")[1]) - 1)
        }
    }
    else {
        $("#blog_list_next_page")[0].innerHTML = '<a></a>';
    }

    $("#blog_list_outer ul").children().remove();
    for (var i = 0; i < response_data.blog.results.length; i++) {
        var b = $blog_li.clone(true);
        b.find("#reply_count").text(response_data.blog.results[i].reply_counter);
        b.find("#blog_title").text(response_data.blog.results[i].blog_title)
            .attr("href", response_data.blog.results[i].url);
        ;
        b.find("#blog_date").text(response_data.blog.results[i].pub_date.substr(5, 5) + ' ' + response_data.blog.results[i].pub_date.substr(11, 5));
        b.find("#blog_user").text(response_data.blog.results[i].user);
        b.find("#blog_text").text(response_data.blog.results[i].blog_text);
        b.find("#reply_date").text(response_data.blog.results[i].latest_reply.substr(5, 5) + ' ' + response_data.blog.results[i].latest_reply.substr(11, 5));
        b.find("#reply_user").text(response_data.blog.results[i].latest_reply_user);
        //Blog图片处理
        show_blog_img(".blog_title", "");
        $("#blog_list_outer ul").append(b);
        b.slideDown();
    }


}

function show_blog_list(dom) {
    $.ajax({
        type: "GET",
        url: dom.href,
        contentType: "application/json",
        data: {},
        dataType: "json",
        success: function (response_data) {
            load_blog_list(response_data)

        }
    });
}


function show_blog_img(blog_selector, reply_selector) {

    for (var i = 0; i < $(reply_selector).length; i++) {
        var ss = $(reply_selector)[i].innerHTML;
        ss = ss.replaceAll("&gt;", ">");
        ss = ss.replaceAll("&lt;", "<");
        ss = ss.replaceAll("\n", "<br/>");
        ss = ss.replaceAll("&quot;", "'");
        $(reply_selector)[i].innerHTML = ss;
    }

    for (var i = 0; i < $(blog_selector).length; i++) {
        var s = $(blog_selector)[i].innerHTML;
        s = s.replaceAll("&gt;", ">");
        s = s.replaceAll("&lt;", "<");
        s = s.replaceAll("\n", "<br/>");
        s = s.replaceAll("&quot;", "'");
        $(blog_selector)[i].innerHTML = s;
    }
}