/*global json show*/

// 重置查询
function refresh(changeTopic){
    var topic = document.getElementById("topicChoice").value;
    var msgKey = document.getElementById("msgKeyChoice").value;
    var filterTime = document.getElementById("filterTime").value;
    var postJson = {};
    postJson["reqType"] = "1";
    postJson["topic"] = topic;
    if(changeTopic){
        postJson["currentMsgKey"] = "";
    }else{
        postJson["currentMsgKey"] = msgKey;
    }
    postJson["filterTime"] = filterTime;
    postJson["offset"] = "0";

    var postData = JSON.stringify(postJson, null, 2);
    $.ajax({
        type: "POST",
        url: "",
        contentType: "application/json; charset=utf-8",
        data: postData,
        dataType: "html",
        success: function (res) {
            // 替换record html
            $('body').html(res);
         },
        error: function (res) {
            alert("操作失败");
        }
        });
}

// 滚动条在Y轴上的滚动距离
function getScrollTop() {
    var scrollTop = 0;
    var bodyScrollTop = 0;
    var documentScrollTop = 0;
    if(document.body){
        bodyScrollTop = document.body.scrollTop;
    }
    if(document.documentElement){
        documentScrollTop = document.documentElement.scrollTop;
    }
    scrollTop = (bodyScrollTop - documentScrollTop > 0) ? bodyScrollTop : documentScrollTop;
    return scrollTop;
}

// 文档的总高度
function getScrollHeight() {
    var scrollHeight = 0;
    var bodyScrollHeight = 0;
    var documentScrollHeight = 0;
    if(document.body){
        bodyScrollHeight = document.body.scrollHeight;
	}
	if(document.documentElement){
		documentScrollHeight = document.documentElement.scrollHeight;
	}
	scrollHeight = (bodyScrollHeight - documentScrollHeight > 0) ? bodyScrollHeight : documentScrollHeight;
	return scrollHeight;
}

// 浏览器视窗的总高度
function getWindowHeight() {
    var windowHeight = 0;
    if(document.compatMode == "CSS1Compat"){
		windowHeight = document.documentElement.clientHeight;
	}else{
		windowHeight = document.body.clientHeight;
	}
	return windowHeight;
}

//js原生监听 滚动事件的---因为项目框架和jquery不兼容
function scrollFunction() {
    var topic = document.getElementById("currentTopic").value;
    var msgKey = document.getElementById("currentMsgKey").value;
    var filterTime = document.getElementById("filterTime").value;
    var offset = document.getElementById("offset").value;

    // 查询topic消息的下一页的消息
    if(offset == "0"){
        return;
    }
    var postJson = {};
    postJson["reqType"] = "1";
    postJson["topic"] = topic;
    postJson["currentMsgKey"] = msgKey;
    postJson["filterTime"] = filterTime;
    postJson["offset"] = offset;
    var postData = JSON.stringify(postJson, null, 2);
    $.ajax({
        type: "POST",
        url: "",
        contentType: "application/json; charset=utf-8",
        data: postData,
        dataType: "html",
        success: function (res) {
            // 替换record html
            var recordHtml = $(res).find('#recordContainer').html();
            var divRecord = document.getElementById("recordContainer");
            divRecord.innerHTML = divRecord.innerHTML + recordHtml;
            // 刷新数据后更新offset, 为下一次刷新做准备
            var offsetHtml = $(res).find('#offsetLast').html();
            document.getElementById("offsetLast").innerHTML = offsetHtml;
            // 刷新筛选列表
            var topicHtml = $(res).find('#topicChoice').html();
            document.getElementById("topicChoice").innerHTML = topicHtml;
            var msgKeyHtml = $(res).find('#msgKeyChoice').html();
            document.getElementById("msgKeyChoice").innerHTML = msgKeyHtml;
         },
        error: function (res) {
            alert("操作失败");
        }
        });
}