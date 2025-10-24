go-resty一个优秀的 HTTP 客户端库 go-resty超时控制示例 go-resty自动重示例 go-resty TLS示例 go-resty 与连接池 go-resty 与代理 go-resty 与认证 总结go-resty中提供的API

# 一. go-resty一个优秀的 HTTP 客户端库

在 Golang 标准库中提供了net/http 具体参考该文档 这里我们看一个三方库go-resty,一个优秀的 HTTP 客户端库,支持链式调用,超时控制,TLS,Cookie 管理,链接池,代理,支持多种认证方式包括基本认证和 OAuth 2.0,支持发送 JSON、XML 和 URL 编码的数据,文件上传和下载,支持发送大量请求并批量处理响应结果,同时提供简单易用的 API 接口

```
package main
import (
	"fmt"
	"github.com/go-resty/resty/v2"
)

type User struct {
	ID    int    `json:"id"`
	Name  string `json:"name"`
	Email string `json:"email"`
}

func main() {
	// 创建 Resty 客户端对象
	client := resty.New()

	// GET 请求示例
	resp, err := client.R().
		SetQueryParams(map[string]string{
			"id": "1",
		}).
		SetHeader("Accept", "application/json").
		Get("https://httpbin.org/get")

	if err != nil {
		fmt.Println("发送 GET 请求失败：", err)
		return
	}

	// 解析响应为结构体
	var user User
	err = resp.UnmarshalJSON(&user)
	if err != nil {
		fmt.Println("解析响应失败：", err)
		return
	}

	fmt.Println("User ID:", user.ID)
	fmt.Println("User Name:", user.Name)
	fmt.Println("User Email:", user.Email)

	// POST 请求示例
	reqBody := map[string]interface{}{
		"name":  "Alice",
		"email": "alice@example.com",
	}
	resp, err = client.R().
		SetHeader("Content-Type", "application/json").
		SetBody(reqBody).
		Post("https://httpbin.org/post")

	if err != nil {
		fmt.Println("发送 POST 请求失败：", err)
		return
	}

	// 解析响应为结构体
	err = resp.UnmarshalJSON(&user)
	if err != nil {
		fmt.Println("解析响应失败：", err)
		return
	}

	fmt.Println("User ID:", user.ID)
	fmt.Println("User Name:", user.Name)
	fmt.Println("User Email:", user.Email)

	//也可以这样,通过SetResult(响应结构体)将响应直接解析到指定结构体上
	result:= &response.APIJsonReturn{}
	resp, err := client.R().
		SetBody(data).
		SetResult(result).
		Post(url)

	if err != nil {
		log.ErrorLog(msgId, "%+v", err)
		return err 
	}

	if !resp.IsSuccess() {
		log.ErrorLog(msgId, "%+v", resp)
		return newErr
	}
}
```

# 2 go-resty 的优点

1. 对于 RESTful API 开发者更加友好：go-resty 通过链式调用接口使得代码更具可读性，容易实现复杂的 API 调用。
2. 容易拓展：go-resty 提供了许多官方扩展插件，如 Logger、Retryer、JSONMarshaler、XMLMarshaler、OAuth1 等等
3. 更简单的错误处理：go-resty 会在返回的 Response 中包含所有的错误信息。

# 3 go-resty 的缺点

1. 需要额外依赖库：使用 go-resty 需要引入第三方库，而 net/http 则是 Go 标准库自带的，不需要额外引用。
2. 相对较慢：由于 go-resty 是基于 net/http 封装的，所以在某些情况下可能比 net/http 要慢一些。

# 4 相对于 go-resty 来说net/http 的缺点

1. 错误信息不够全面：net/http 返回的 Response 中的错误信息不够全面。
2. URL 解析错误跑出 panic：当解析一个错误的 URL 时，net/http 会直接抛出 panic 而不是返回一个错误信息，可能会导致程序崩溃。
3. 上方在再获取到client后执行client.R()后面接连调用的函数就是链式调用,下方就不再示例

# 5 go-resty超时控制示例

```
package main
import (
	"fmt"
	"time"
	"github.com/go-resty/resty/v2"
)

type User struct {
	ID    int    `json:"id"`
	Name  string `json:"name"`
	Email string `json:"email"`
}

func main() {
	client := resty.New()

	// 设置超时时间为 5 秒钟
	client.SetTimeout(5 * time.Second)

	resp, err := client.R().
		SetQueryParams(map[string]string{
			"id": "1",
		}).
		SetHeader("Accept", "application/json").
		Get("https://httpbin.org/get")

	if err != nil {
		// 判断是否是超时错误
		if restErr, ok := err.(*resty.TimeoutError); ok {
			fmt.Println("请求超时：", restErr)
		} else {
			fmt.Println("发送 GET 请求失败：", err)
		}
		return
	}

	var user User
	err = resp.UnmarshalJSON(&user)
	if err != nil {
		fmt.Println("解析响应失败：", err)
		return
	}
}
```

# 6 go-resty自动重示例

```
package main
import (
	"fmt"
	"time"
	"github.com/go-resty/resty/v2"
)

type User struct {
	ID    int    `json:"id"`
	Name  string `json:"name"`
	Email string `json:"email"`
}

func main() {
	client := resty.New()

	// 设置最大重试次数为 3 次，重试间隔时间为 1 秒钟
	client.SetRetryCount(3).
		SetRetryWaitTime(1 * time.Second)

	resp, err := client.R().
		SetQueryParams(map[string]string{
			"id": "1",
		}).
		SetHeader("Accept", "application/json").
		Get("https://httpbin.org/get")

	if err != nil {
		fmt.Println("发送 GET 请求失败：", err)
		return
	}

	var user User
	err = resp.UnmarshalJSON(&user)
	if err != nil {
		fmt.Println("解析响应失败：", err)
		return
	}
}
```

使用 client.RetryMax() 方法来设置重试次数，使用 client.RetryWaitTime() 方法来设置重试间隔时间

SetRetryCount() 用于 Resty 对象上的全局设置，所有使用该 Resty 对象发送的请求都会遵循这个重试次数 RetryMax() 方法是应用于请求对象上的设置，即每次请求都可以根据具体需要独立地设置重试次数

```
package main
import (
	"fmt"
	"github.com/go-resty/resty/v2"
)

func main() {
	client := resty.New()

	resp, err := client.R().
		SetRetryCount(0).
		SetRetryWaitTime(1).
		SetQueryParams(map[string]string{
			"id": "1",
		}).
		SetHeader("Accept", "application/json").
		Get("https://httpbin.org/get")

	if resp.IsError() {
		resp, err = resp.Request.
			RetryMax(1).
			Get("https://httpbin.org/get")
	}

	if err != nil {
		fmt.Println("发送 GET 请求失败：", err)
		return
	}

	fmt.Println(resp)
}
```

# 7 go-resty TLS示例

```
package main
import (
	"fmt"
	"github.com/go-resty/resty/v2"
)

func main() {
	client := resty.New()

	// 设置证书文件路径和密码
	certFile := "/path/to/cert.pem"
	keyFile := "/path/to/key.pem"
	password := "secret"

	// 加载证书
	err := client.SetCertificates(certFile, keyFile, password)
	if err != nil {
		fmt.Println("加载证书失败：", err)
		return
	}

	// 关闭证书校验
	client.SetTLSClientConfig(&tls.Config{InsecureSkipVerify: true})

	resp, err := client.R().
		SetHeader("Accept", "application/json").
		Get("https://httpbin.org/get")

	if err != nil {
		fmt.Println("发送 GET 请求失败：", err)
		return
	}

	fmt.Println(resp)
}
```

# 8 go-resty 与连接池

go-resty 库使用 http.Transport 来实现 HTTP 连接池。http.Transport 提供了以下几个属性来控制连接池的行为：

* MaxIdleConns: 每个主机的最大空闲连接数。
* MaxIdleConnsPerHost: 对于每个主机，保持最大空闲连接数。
* IdleConnTimeout: 空闲连接的超时时间。
* TLSHandshakeTimeout: TLS 握手的超时时间。
* ResponseHeaderTimeout: 等待响应头的超时时间。

```
// 创建一个新的 resty 客户端实例
client := resty.New()

// 设置连接池参数
client.SetTransport(&http.Transport{
    MaxIdleConnsPerHost: 10, // 对于每个主机，保持最大空闲连接数为 10
    IdleConnTimeout: 30 * time.Second, // 空闲连接超时时间为 30 秒
    TLSHandshakeTimeout: 10 * time.Second, // TLS 握手超时时间为 10 秒
    ResponseHeaderTimeout: 20 * time.Second, // 等待响应头的超时时间为 20 秒
})
```

# 9 go-resty 与代理

go-resty 库支持使用代理来发送 HTTP 请求,通过 client.SetProxy() 方法来设置代理参数

```
import (
	"fmt"
	"github.com/go-resty/resty/v2"
	"testing"
)

func TestSend(t *testing.T){
	// 创建一个新的 resty 客户端实例
	client := resty.New()

	// 设置代理参数
	proxyURL := "http://user:password@proxyhost:port"
	client.SetProxy(proxyURL)

	// 发送 POST 请求
	resp, err := client.R().
		SetHeader("Content-Type", "application/json").
		SetBody(map[string]string{
			"name":  "John",
			"email": "john@example.com",
		}).
		Post("https://httpbin.org/post")
	if err != nil {
		fmt.Println("Error:", err)
		return
	}

	// 输出响应结果
	fmt.Println("Status Code:", resp.StatusCode())
	fmt.Println("Body:", resp.String())
}
```

除了 client.SetProxy() 方法之外，go-resty 还提供了一些其他的代理相关设置，包括： client.SetProxyURL(): 设置代理服务器地址，可以是 HTTP 或 SOCKS5 代理。 client.SetProxyHeader(): 设置代理服务器需要的请求头。 client.SetProxyAuth(): 设置代理服务器的认证信息，可以是基本认证或 NTLM 认证

# 10 使用 go-resty 发送带有基本认证的代理请求的示例

使用 client.SetProxyURL() 方法设置代理服务器的地址和端口号， 使用 resty.ProxyBasicAuth() 方法设置基本认证的认证信息， 使用 client.SetProxyHeader() 方法设置代理服务器需要的请求头

```
package main

import (
    "fmt"
    "github.com/go-resty/resty/v2"
    "net/http"
)

func main() {
    // 创建一个新的 resty 客户端实例
    client := resty.New()

    // 设置代理服务器地址和认证信息
    proxyURL := "http://proxyhost:port"
    proxyAuth := resty.ProxyBasicAuth("user", "password")

    // 设置代理参数
    client.SetProxyURL(proxyURL).
           SetProxyAuth(proxyAuth)

    // 设置代理服务器需要的请求头
    client.SetProxyHeader(http.Header{
        "User-Agent": []string{"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"},
    })

    // 发送 GET 请求
    resp, err := client.R().
        Get("http://example.com")
    if err != nil {
        fmt.Println("Error:", err)
        return
    }

    // 输出响应结果
    fmt.Println("Status Code:", resp.StatusCode())
    fmt.Println("Body:", resp.String())
}
```

# 11 go-resty 与认证

go-resty 支持以下几种代理认证方式：

* 基本认证（Basic Authentication）：使用用户名和密码进行认证，是一种最常见的 HTTP 认证方式。
* NTLM 认证（NT LAN Manager）：微软开发的认证协议，可以实现单点登录（SSO）。
* Digest 认证（Digest Authentication）：基于用户名、密码和消息摘要的认证协议，用于解决明文认证方式的安全问题 可以使用 resty.ProxyBasicAuth()、resty.ProxyNtlmAuth() 和 resty.ProxyDigestAuth() 方法来设置相应的认证信息，例如：

```
// 设置基本认证的认证信息
proxyAuth := resty.ProxyBasicAuth("user", "password")
client.SetProxyAuth(proxyAuth)

// 设置 NTLM 认证的认证信息
proxyAuth := resty.ProxyNtlmAuth("domain", "user", "password")
client.SetProxyAuth(proxyAuth)

// 设置 Digest 认证的认证信息
proxyAuth := resty.ProxyDigestAuth("user", "password")
client.SetProxyAuth(proxyAuth)
```

注意在使用某些认证方式时，需要提供相应的附加参数。例如，对于 NTLM 认证方式，需要提供域名或主机名等相关信息；对于 Digest 认证方式，需要通过 resty.ProxyDigestAuth() 方法提供一个回调函数来生成响应的摘要头部（Digest header），以便与代理服务器进行交互

# 12 总结go-resty中提供的API

Resty 对象方法

```
New() *Resty: 创建一个默认配置的 Resty 对象。
NewWithClient(client *http.Client) *Resty: 创建一个自定义配置的 Resty 对象，并使用指定的 http.Client 客户端对象。
R() *Request: 创建一个 Request 对象，并使用 Resty 对象的默认配置设置。
SetDebug(on bool) *Resty: 设置是否启用调试模式。如果启用，则会在控制台输出详细的请求和响应信息。
SetTimeout(timeout time.Duration) *Resty: 设置超时时间。可以在发送请求之前设置超时时间，单位为秒。
SetHeaders(headers map[string]string) *Resty: 设置请求头。可以通过传入一个键值对映射来设置多个请求头。
SetQueryParam(key, value string) *Request: 设置查询参数。可以通过在请求 URL 后添加查询字符串参数的方式设置。
SetFormData(data map[string]string) *Request: 设置表单数据。可以通过传入一个键值对映射来设置多个表单字段。
SetFormDataFromValues(values url.Values) *Request: 设置表单数据。可以通过传入一个 url.Values 对象来设置多个表单字段。
SetBody(body interface{}) *Request: 设置请求体。可以通过传入一个支持 io.Reader 接口的对象、字节数组或字符串来设置请求体内容。
SetResult(result interface{}) *Request: 设置响应结果类型。可以通过传入一个结构体对象类型来指定响应结果的解析方式。
SetError(err interface{}) *Request: 设置错误类型。可以通过传入一个结构体对象类型来指定解析错误信息的方式。
SetError(&ResponseError{Error: “custom error”}) *Request: 设置自定义错误信息，可以在请求返回不成功的情况下获取。
GetClient() *http.Client: 获取当前 Resty 对象使用的 http.Client 客户端对象。
SetTLSClientConfig(config *tls.Config) *Resty: 设置 TLS 客户端配置，例如关闭证书校验等安全选项。
SetCertificates(certFile, keyFile string, password string) error: 设置客户端证书和私钥，用于双向认证和 TLS 握手过程中的身份验证。
```

# 13 Request 对象方法

```
SetMethod(method string) *Request: 设置请求方法。可以设置 GET、POST、PUT、DELETE 等常见的 HTTP 请求方法。
SetHeader(key, value string) *Request: 设置请求头。可以通过传入一个键值对来设置单个请求头。
SetHeaders(headers map[string]string) *Request: 设置请求头。可以通过传入一个键值对映射来设置多个请求头。
SetQueryParam(key, value string) *Request: 设置查询参数。可以通过在请求 URL 后添加查询字符串参数的方式设置。
SetFormData(data map[string]string) *Request: 设置表单数据。可以通过传入一个键值对映射来设置多个表单字段。
SetFormDataFromValues(values url.Values) *Request: 设置表单数据。通过传入一个 url.Values 对象来设置多个表单字段
SetBody(body interface{}) *Request: 设置请求体。通过传入一个支持 io.Reader 接口的对象、字节数组或字符串来设置请求体内容。
SetResult(result interface{}) *Request: 设置响应结果类型。可以通过传入一个结构体对象类型来指定响应结果的解析方式。
SetError(err interface{}) *Request: 设置错误类型。可以通过传入一个结构体对象类型来指定解析错误信息的方式。
SetError(&ResponseError{Error: “custom error”}) *Request: 设置自定义错误信息，可以在请求返回不成功的情况下获取。
Execute() (*Response, error): 执行 HTTP 请求，并返回响应结果。如果请求出现问题或响应不成功，会返回一个错误对象
GetRequestURL() string: 获取当前请求的完整 URL。
SetBasicAuth(username, password string) *Request: 设置基本身份验证信息。通过传入用户名和密码来设置 HTTP 基本身份验证头
SetAuthToken(token string) *Request: 设置 Token 鉴权信息。可以通过传入 Token 字符串来设置 HTTP 请求头。
SetCloseConnection(cflag bool) *Request: 设置是否关闭连接。可以设置为 true 来在每次请求后关闭连接，也可以设置为 false 来保持长连接。
SetContentLength(contentLength int64) *Request: 设置请求体长度。在发送有请求体的请求时，显式地指定请求体的长度
SetContext(ctx context.Context) *Request: 设置请求上下文。可以通过传入一个 context.Context 对象来控制请求的生命周期和超时等细节。
SetCookies(cookies []*http.Cookie) *Request: 设置请求 Cookie。可以通过传入一个 Cookie 数组来设置多个 Cookie。
SetDisableWarn(bool) *Request: 设置是否禁用 Resty 警告信息。如果设为 true，则会隐藏一些警告信息。
SetDoNotParseResponse(bool) *Request: 设置是否跳过响应解析。如果设为 true，则会返回原始的响应字节数组，而不是解析后的结构体对象。
SetFile(key, filepath string) *Request: 向表单数据中添加文件。传入文件名和文件路径参数来添加文件字段和对应的文件内容
SetHeader(key, value string) *Request: 设置请求头。可以通过传入一个键值对来设置单个请求头。
SetHostURL(url string) *Request: 设置请求的基本 URL。可以在发送请求前设置基本的 URL，然后在具体请求中只传入相对路径即可。
SetOutput(output io.Writer) *Request: 设置响应输出。可以通过传入一个 io.Writer 对象来将响应结果输出到指定的流中。
SetQueryParam(key, value string) *Request: 设置查询参数。可以通过在请求 URL 后添加查询字符串参数的方式设置。
SetRedirectPolicy(policy grequests.RedirectPolicy) *Request: 设置重定向策略。可以传入一个实现了 grequests.RedirectPolicy 接口的对象来自定义重定向行为。
SetRedirectPolicyFunc(f func(*http.Request, []*http.Request) error) *Request: 设置重定向策略函数。可以传入一个自定义的函数来设置重定向行为。
SetRequestBodyStream(body io.ReadCloser) *Request: 设置请求体流。可以传入一个支持 io.ReadCloser 接口的对象来指定请求体内容。
SetRequestURI(uri string) *Request: 设置完整请求 URI。可以用于更灵活地控制请求的地址和参数等信息。
SetRetryCount(retryCount int) *Request: 设置重试次数。可以在请求失败或出错时自动重试该请求，设为 0 则不重试。
SetRetryWaitTime(retryWaitTime time.Duration) *Request: 设置重试间隔时间。可以在请求失败或出错时自动重试该请求，并设置重试之间的间隔时间。
SetTransport(transport http.RoundTripper) *Request: 设置传输层。可以通过传入一个实现了 http.RoundTripper 接口的对象来定制 HTTP 传输层行为。
ToJSON(v interface{}) error: 将请求体解析为 JSON 格式。可以传入一个结构体对象指针来解析响应结果。
ToXML(v interface{}) error: 将请求体解析为 XML 格式。可以传入一个结构体对象指针来解析响应结果。
ToString() (string, error): 将响应结果解析为字符串。如果响应结果不是字符串格式，则会返回一个解析错误。
ToBytes() ([]byte, error): 将响应结果解析为字节数组。如果响应结果无法解析，则会返回一个解析错误。
ToFile(filepath string) error: 将响应结果保存到文件中。可以传入文件路径参数来保存响应结果。
IsError(err error) bool: 判断是否出现了错误。可以在请求结束后通过该方法判断请求是否成功或出错。
```

# 14 Response 对象方法

```
StatusCode() int: 获取 HTTP 状态码。可以获取 HTTP 响应返回的状态码。
Proto() string: 获取 HTTP 协议版本。可以获取 HTTP 响应使用的协议版本。
Body() []byte: 获取响应内容。可以获取 HTTP 响应返回的原始字节流。
Result() interface{}: 获取响应结果。可以获取经过解析和转换后的响应结果。
Error() error: 获取错误信息。如果请求失败或返回结果有误，则会返回一个错误对象。
Header() http.Header: 获取响应头。可以获取 HTTP 响应返回的原始头部信息。
Cookies() []*http.Cookie: 获取响应 Cookie。可以获取 HTTP 响应返回的所有 Cookie 键值对。
String() string: 获取响应结果字符串。可以直接获取 HTTP 响应返回的字符串格式结果。
Time() time.Time: 获取响应时间。可以获取 HTTP 响应的时间戳和格式化字符串。
Request() *http.Request: 获取原始请求。可以获取 HTTP 请求的原始对象，包含所有请求头部和请求体等信息。
```
