# 简介
> Kubernetes Ingress 是一种 API 对象，用于管理对集群内服务的外部访问。它通常用于 HTTP/HTTPS 流量的路由，并提供负载均衡、SSL/TLS 终止和基于名称的虚拟主机等功能。Ingress 本身并不直接处理流量，而是通过 Ingress Controller 来实现这些功能。常见的 Ingress Controller 有 Nginx、Traefik、HAProxy 等。

# 安装
```
helm repo add appstore https://charts.grapps.cn
helm repo update appstore
helm install ingress-nginx appstore/ingress-nginx  --version 4.7.1
```
# 样例
```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: example-ingress # Ingress 资源的名称
  annotations: # 用于配置 Ingress Controller 的特定行为
    nginx.ingress.kubernetes.io/rewrite-target: /  # 重写目标路径
    nginx.ingress.kubernetes.io/ssl-redirect: "true"  # 强制重定向到 HTTPS
spec:
  tls:
    - hosts:
        - example.com  # 域名
      secretName: example-tls  # TLS 证书的 Secret 名称
  rules:
    - host: example.com  # 域名
      http:
        paths:
          - path: /service1  # 请求路径
            pathType: Prefix  # 路径类型(Prefix/Exact/ImplementationSpecific)
            backend:
              service:
                name: service1  # 服务名称(集群内部)
                port:
                  number: 80  # 服务端口(集群内部)
          - path: /service2
            pathType: Prefix
            backend:
              service:
                name: service2
                port:
                  number: 80
```
# 对外提供服务使用Ingress和NodePort的区别？
> 在 Kubernetes 中，Service 的 NodePort 类型确实可以将服务暴露到集群外部，但使用 Ingress 有更多的优势和适用场景

## 更灵活的路由规则
- NodePort 的限制：
  - NodePort 只能通过特定的端口暴露服务，无法根据请求的路径或域名进行路由。
  - 如果有多个服务，每个服务都需要占用一个不同的端口，管理起来非常麻烦。
- Ingress 的优势：
  - Ingress 可以根据请求的路径 (path) 或域名 (host) 将流量路由到不同的服务。
  - 例如：
    - example.com/service1 路由到 service1。
    - example.com/service2 路由到 service2。
  - 这样，多个服务可以共享同一个端口（通常是 80 或 443）。

---
## 支持 HTTPS
- NodePort 的限制：
  - NodePort 本身不支持 HTTPS，如果需要 HTTPS，需要在应用层或外部负载均衡器上配置。
- Ingress 的优势：
  - Ingress 原生支持 HTTPS，可以通过配置 TLS 证书实现安全的 HTTPS 访问。
  - 大多数 Ingress Controller（如 Nginx、Traefik）都支持自动管理 TLS 证书（例如通过 Let's Encrypt）。

---
## 集中管理外部访问
- NodePort 的限制：
  - 每个 NodePort 服务都需要单独管理，端口冲突和端口范围限制可能导致管理复杂度增加。
- Ingress 的优势：
  - Ingress 提供了一个统一的入口，集中管理所有外部访问。
  - 通过一个 Ingress 资源可以管理多个服务的路由规则，简化了配置和维护。

---
## 负载均衡
- NodePort 的限制：
  - NodePort 本身不提供高级负载均衡功能，流量会直接转发到某个节点的端口。
  - 如果需要负载均衡，通常需要依赖外部的负载均衡器（如云服务商的 LB）。
- Ingress 的优势：
  - Ingress Controller（如 Nginx、Traefik）通常内置了负载均衡功能，可以根据权重、会话保持等策略分发流量。
  - 支持更复杂的流量管理，如蓝绿部署、金丝雀发布等。

---
## 减少端口暴露
- NodePort 的限制：
  - NodePort 需要在每个节点上开放一个端口（默认范围是 30000-32767），这会增加安全风险。
- Ingress 的优势：
  - Ingress 只需要暴露 80（HTTP）和 443（HTTPS）端口，减少了端口暴露的数量，降低了安全风险。

---
## 支持高级功能
- Ingress 的优势：
  - Ingress 支持许多高级功能，例如：
    - URL 重写
    - 流量镜像
    - 请求速率限制
    - 身份验证（如 OAuth、JWT）
    - 自定义错误页面
  - 这些功能在 NodePort 中是无法实现的。

---
## 与云服务集成
- Ingress 的优势：
  - 在云环境中，Ingress 通常与云服务商的负载均衡器（如 AWS ALB、GCP Load Balancer）集成，提供更强大的功能。
  - 例如，AWS ALB Ingress Controller 可以自动创建和管理 AWS 应用负载均衡器。

## 总结
- 使用 NodePort 的场景：
  - 适合简单的测试环境或临时暴露服务。
  - 不需要复杂的路由规则或 HTTPS。
- 使用 Ingress 的场景：
  - 适合生产环境，尤其是需要 HTTPS、复杂路由规则、负载均衡和高级功能的场景。
  - 提供了更强大、更灵活的外部访问管理能力。
因此，在生产环境中，Ingress 通常是更好的选择，而 NodePort 更适合临时或简单的场景。