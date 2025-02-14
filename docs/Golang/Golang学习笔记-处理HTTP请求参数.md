```
func body(w http.ResponseWriter, r *http.Request) {
	fmt.Println(r.Header)
	// 获取请求头信息：r.Header
	// 获取请求头的某条信息：h := r.Header["Accept-Encoding"]或h := r.Header.Get("Accept-Encoding")
	// 判断请求方式
	if r.Method == "GET" {
		// 方法1：获取GET请求的请求参数，接收application/x-www-form-urlencoded编码的数据
		//r.ParseForm()
		//fmt.Println(r.Form["name"])
		// 方法2：获取GET请求的请求参数，接收application/x-www-form-urlencoded编码的数据
		fmt.Println(r.URL.Query())
		// 方法3：获取GET请求的请求参数，接收application/x-www-form-urlencoded编码的数据。
		fmt.Println(r.FormValue("name"))
		// 响应内容
		fmt.Fprintln(w, r.FormValue("name"))
	} else {
		// 方法1：获取POST请求的请求参数
		// 分别使用Form和PostForm方法获取POST的请求参数
		// 使用Form和PostForm之前必须调用ParseForm方法
		// 接收application/x-www-form-urlencoded编码的数据
		//r.ParseForm()
		//fmt.Println(r.Form["name"][0])
		//fmt.Println(r.PostForm["name"][0])

		// MultipartForm用于文件上传，使用前需要调用ParseMultipartForm方法
		// 接收multipart/form-data编码
		// 注意：FormFile是MultipartForm的简化功能
		//r.ParseMultipartForm(1024)
		//fmt.Println(r.MultipartForm)

		// 方法2：获取POST请求的请求参数，但无法获取Multipart编码，即无法读取文件上存的数据
		// FormValue将Form的功能简化，接收application/x-www-form-urlencoded编码的数据
		// 注意：PostFormValue将PostForm的功能简化，接收application/x-www-form-urlencoded编码的数据
		fmt.Println(r.FormValue("name"))

		// 方法3：接收POST的JSON数据，因为JSON数据使用application/json编码
		con, _ := ioutil.ReadAll(r.Body)
		fmt.Println(string(con))

		// 响应内容
		fmt.Fprintln(w, r.FormValue("name"))
	}
}

```
