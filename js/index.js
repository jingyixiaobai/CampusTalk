			mui.plusReady(function(){
				var subPages = ["main.html", "setting.html", "post.html", "personal.html"];
				var subPagesStyle={
					bottom:"50px"
				};
				var mainView=plus.webview.currentWebview();
				for(var i=0;i<subPages.length;i++){
					var url=subPages[i];
					var subView=plus.webview.create(url,url,subPagesStyle);
					subView.hide();
					mainView.append(subview)
				}
				plus.webview.show(subPages[0]);
				mui(".mui-bar-tab").on("tap","a",function(){
					var id=this.getAttribute("href");
					plus.webview.show(id);
				});
				
			});