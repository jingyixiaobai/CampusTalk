// a标签不能跳转页面问题
// mui('body').on('tap','a',function({document.location.href=this.href;});
// mui('body').on('click','a',function({document.location.href=this.href;});
window.onload = function() {
  var post_form = document.getElementById("post-form");
  post_form.addEventListener("submit", post_data);
}
function post_data(e) {
  //阻止表单的默认提交行为
  e.preventDefault();
  var title = document.querySelector(".title").value;
  var content = document.querySelector(".content").value;
  if (title == "" || content == "") {
    mui.toast("标题和内容不能为空");
    return; 
  }
  mui.post("/post", {
    title: title,
    content: content
  }, function(data) {
    if (data.code == 0) {
      mui.toast("发布成功");
      //跳转到帖子列表页面或其他操作
      ...
    } else {
      mui.toast("发布失败：" + data.msg);
    }
  }, "json");
  //清空表单的输入内容
  post_form.reset();
}
