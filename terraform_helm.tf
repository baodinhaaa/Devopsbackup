provider "helm" {
  kubernetes {
    config_path = "C:/Users/hung/.kube/config"
  }
}
resource "kubernetes_namespace" "tiller" {
  metadata {
    name = "tiller"
  }
}
resource "helm_release" "my-chart" {
  name         = "nginx-app"
  chart        = "C:/Users/hung/Desktop/Devops/k8s/nginx-app"
  namespace    = kubernetes_namespace.tiller.metadata.0.name
  timeout      = 3600
  force_update = true
}