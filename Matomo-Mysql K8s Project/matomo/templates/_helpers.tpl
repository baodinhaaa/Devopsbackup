## Resources for app
{{- define "matomo.resources" -}}
limits:
  memory: {{ .Values.resources_matomo.limits.memory }}
  cpu: {{ .Values.resources_matomo.limits.cpu }}
requests:
  memory: {{ .Values.resources_matomo.requests.memory }}
  cpu: {{ .Values.resources_matomo.requests.cpu }}
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