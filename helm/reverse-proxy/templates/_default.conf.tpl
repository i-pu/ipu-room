{{- define "default.conf" -}}
upstream upstream-{{ .Values.webSocketServer.service.name }} {
    server  {{ .Values.webSocketServer.service.name }}:{{ .Values.webSocketServer.port }};
}

upstream upstream-{{ .Values.databaseController.service.name }} {
    server {{ .Values.databaseController.service.name }}:{{ .Values.databaseController.port }};
}

upstream upstream-{{ .Values.client.service.name }} {
    server {{ .Values.client.service.name }}:{{ .Values.client.port }};
}

server{
    server_name    _;
    listen {{ .Values.reverseProxy.port }};

    location ^~ /web-socket-server/socket.io {
        proxy_pass    http://upstream-{{ .Values.webSocketServer.service.name }};
        # proxy_pass    http://{{ .Values.webSocketServer.service.name }};
        proxy_redirect off;

        proxy_http_version      1.1;

        proxy_set_header        Upgrade                 $http_upgrade;
        proxy_set_header        Connection              "upgrade";

        proxy_set_header        Host                    $host;
        proxy_set_header        X-Real-IP               $remote_addr;
        proxy_set_header        X-Forwarded-Host        $host;
        proxy_set_header        X-Forwarded-For         $proxy_add_x_forwarded_for;
        proxy_set_header        X-Forwarded-Server      $host;
    }

    location ^~ /database-controller {
        proxy_pass    http://upstream-{{ .Values.databaseController.service.name }};
        # proxy_pass    http://{{ .Values.databaseController.service.name }};
        proxy_redirect          off;

        proxy_set_header        Host                    $host;
        proxy_set_header        X-Real-IP               $remote_addr;
        proxy_set_header        X-Forwarded-Host        $host;
        proxy_set_header        X-Forwarded-For         $proxy_add_x_forwarded_for;
        proxy_set_header        X-Forwarded-Server      $host;
    }

    location ^~ / {
        proxy_pass    http://upstream-{{ .Values.client.service.name }};
        # proxy_pass    http://{{ .Values.client.service.name }};
        proxy_redirect          off;

        proxy_set_header        Host                    $host;
        proxy_set_header        X-Real-IP               $remote_addr;
        proxy_set_header        X-Forwarded-Host        $host;
        proxy_set_header        X-Forwarded-For         $proxy_add_x_forwarded_for;
        proxy_set_header        X-Forwarded-Server      $host;
    }
}
{{- end -}}