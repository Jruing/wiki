## Hook fetch
```
(function() {
    const origFetch = window.fetch;
    window.fetch = function(input, init) {
        let url = typeof input === 'string' ? input : input.url;

        // 打印请求 URL 和参数
        console.log('%c[Hook Fetch] 请求地址:', 'color: blue; font-weight: bold;', url);
        console.log('%c请求配置:', 'color: green;', init);

        // 可选：修改请求头
        if (init && init.headers) {
            init.headers['X-Requested-With'] = 'Hooked by Console';
        }

        // 返回原始 fetch，并拦截响应
        return origFetch(input, init).then(response => {
            // 克隆响应以便读取 body
            const contentType = response.headers.get("content-type");

            if (contentType && contentType.includes("application/json")) {
                const copy = response.clone();
                copy.json().then(data => {
                    console.log('%c[Hook Fetch] 响应数据:', 'color: purple;', data);
                });
            } else {
                console.log('%c[Hook Fetch] 非 JSON 响应', 'color: gray;');
            }

            return response;
        });
    };
})();
```

## Hook XMLHttpRequest
```
(function() {
    const origOpen = XMLHttpRequest.prototype.open;
    const origSetRequestHeader = XMLHttpRequest.prototype.setRequestHeader;
    const origSend = XMLHttpRequest.prototype.send;

    const pendingRequests = new WeakMap();

    XMLHttpRequest.prototype.open = function(method, url) {
        this._url = url;
        pendingRequests.set(this, { method, url, headers: {}, body: null });
        return origOpen.apply(this, arguments);
    };

    XMLHttpRequest.prototype.setRequestHeader = function(header, value) {
        const data = pendingRequests.get(this);
        if (data) {
            data.headers[header] = value;
        }
        return origSetRequestHeader.apply(this, arguments);
    };

    XMLHttpRequest.prototype.send = function(body) {
        const data = pendingRequests.get(this);
        if (data) {
            data.body = body;
            console.log('%c[Hook XHR] 请求地址:', 'color: blue; font-weight: bold;', this._url);
            console.log('%c请求方法:', 'color: green;', data.method);
            console.log('%c请求头:', 'color: green;', data.headers);
            console.log('%c请求体:', 'color: green;', body);
        }

        this.addEventListener('load', function() {
            const response = this.responseText;
            try {
                const json = JSON.parse(response);
                console.log('%c[Hook XHR] 响应数据:', 'color: purple;', json);
            } catch (e) {
                console.log('%c[Hook XHR] 非 JSON 响应:', 'color: gray;', response);
            }
        });

        return origSend.apply(this, arguments);
    };
})();
```