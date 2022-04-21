## Resources for app
{{- define "lhc.resources" -}}
limits:
  memory: {{ .Values.resources_lhc.limits.memory }}
  cpu: {{ .Values.resources_lhc.limits.cpu }}
requests:
  memory: {{ .Values.resources_lhc.requests.memory }}
  cpu: {{ .Values.resources_lhc.requests.cpu }}
{{- end -}}

## Resources for database
{{- define "db.resources" -}}
limits:
  memory: {{ .Values.resources_db.limits.memory }}
  cpu: {{ .Values.resources_db.limits.cpu }}
requests:
  memory: {{ .Values.resources_db.requests.memory }}
  cpu: {{ .Values.resources_db.requests.cpu }}
{{- end -}}

## Resources for nodejs
{{- define "nodejs.resources" -}}
limits:
  memory: {{ .Values.resources_node.limits.memory }}
  cpu: {{ .Values.resources_node.limits.cpu }}
requests:
  memory: {{ .Values.resources_node.requests.memory }}
  cpu: {{ .Values.resources_node.requests.cpu }}
{{- end -}}

## Resource for other
{{- define "other.resources" -}}
limits:
  memory: {{ .Values.resources_other.limits.memory }}
  cpu: {{ .Values.resources_other.limits.cpu }}
requests:
  memory: {{ .Values.resources_other.requests.memory }}
  cpu: {{ .Values.resources_other.requests.cpu }}
{{- end -}}