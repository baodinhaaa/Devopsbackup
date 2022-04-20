# Define Labels Template
{{- define "nginx-app.labels" }}
name: {{ .Release.Name }}
env: {{ .Values.env }}
{{- end -}}

# Define Resource Template
{{- define "nginx-app.resources" -}}
limits:
  memory: {{ .Values.resources.memory }}
  cpu: {{ .Values.resources.cpu }}
{{- end -}}

#Define Port Template
{{- define "nginx-app.port" -}}
port: {{ .port }}
targetPort: {{ .tgport }}
{{- end }}

