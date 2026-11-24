# quickpool (awsquick2api) on Unikraft Cloud

Amazon Quick 多账号网关，部署在 `was`（美东 Washington DC）。

- `python -m quickpool`，API 8045，OAuth 回调 18080（回环），SSH 2222
- 数据目录 `/app/data`（`api.key` / `admin.key` / `encryption.key` / `quickpool.db`）
- `workers=1` 硬限制：单进程持有 OAuth 回调、刷新锁、账号租约

## 授权必须在实例内完成

`POST /api/accounts/{id}/login` 强制校验来源是 127.0.0.1，OAuth 回调写死 `127.0.0.1:18080`。
所以先建隧道，再从浏览器开 `http://127.0.0.1:8045/` 授权：

```
ssh -o ProxyCommand="openssl s_client -quiet -verify_return_error -connect %h:2222 -servername %h" \
    -i ~/.ssh/quickpool_ukc -p 2222 root@<fqdn> -N \
    -L 8045:127.0.0.1:8045 -L 18080:127.0.0.1:18080
```

## 销毁

```
unikraft instances delete quickpool --metro was
```
