import re

# 直接粘贴整段原始文本，不需要任何删减
raw_yaml = """
   - name: 香港-01
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10101
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 香港-02
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10102
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 香港-03
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10103
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 香港-04
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10104
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 香港-05
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10105
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 香港-06
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10106
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 香港-07
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10107
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 香港-08
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10108
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 香港-09
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10109
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 香港-10
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10110
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 香港-11
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10111
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 香港-12
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10112
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 香港-13
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10113
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 香港-14
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10114
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 香港-15
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10115
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 香港-16
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10116
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 香港-17
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10117
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 香港-18
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10118
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 香港-19
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10119
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 香港-20
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10120
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 台湾-01
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10121
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 台湾-02
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10122
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 台湾-03
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10123
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 台湾-04
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10124
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 台湾-05
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10125
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 台湾-06
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10126
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 台湾-07
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10127
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 台湾-08
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10128
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 台湾-09
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10129
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 台湾-10
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10130
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 新加坡-01
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10131
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 新加坡-02
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10132
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 新加坡-03
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10133
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 新加坡-04
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10134
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 新加坡-05
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10135
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 新加坡-06
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10136
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 新加坡-07
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10137
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 新加坡-08
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10138
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 新加坡-09
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10139
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 新加坡-10
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10140
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 日本-01
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10141
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 日本-02
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10142
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 日本-03
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10143
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 日本-04
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10144
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 日本-05
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10145
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 日本-06
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10146
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 日本-07
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10147
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 日本-08
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10148
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 日本-09
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10149
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 日本-10
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10150
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 美国-01
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10151
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 美国-02
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10152
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 美国-03
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10153
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 美国-04
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10154
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 美国-05
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10155
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 美国-06
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10156
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 美国-07
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10157
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 美国-08
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10158
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 美国-09
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10159
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 美国-10
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10160
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 英国-01
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10161
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 英国-02
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10162
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 英国-03
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10163
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 英国-04
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10164
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 英国-05
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10165
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 马来西亚-01
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10166
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 马来西亚-02
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10167
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 马来西亚-03
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10168
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 马来西亚-04
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10169
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 马来西亚-05
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10170
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 土耳其-01
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10197
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 土耳其-02
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10198
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 阿根廷-01
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10199
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
  - name: 阿根廷-02
    type: vless
    server: b0001.fmjdlogistic.com
    port: 10600
    uuid: 52a8d1ad-437c-3fa4-a378-6ea2993213f1
    udp: true
    tls: true
    flow: xtls-rprx-vision
    skip-cert-verify: true
    servername: cdn1.fmyjs.dev
    network: tcp
 """

def solve():
    # 1. 以 "- name:" 为分隔符，切分出每一个节点块
    # [1:] 是因为第一个切分结果通常是空的
    blocks = re.split(r'-\s*name:', raw_yaml)[1:]
    
    for block in blocks:
        try:
            # 2. 在每个块内部精准提取参数
            # \n 确保只匹配当前行的内容
            name = block.split('\n')[0].strip()
            port = re.search(r'port:\s*(\d+)', block).group(1)
            server = re.search(r'server:\s*([^\s\n]+)', block).group(1)
            uuid = re.search(r'uuid:\s*([^\s\n]+)', block).group(1)
            flow = re.search(r'flow:\s*([^\s\n]+)', block).group(1)
            sni = re.search(r'servername:\s*([^\s\n]+)', block).group(1)
            
            # 3. 构造 vless 链接
            link = (
                f"vless://{uuid}@{server}:{port}"
                f"?allowInsecure=true&alpn=h2%2Chttp%2F1.1&flow={flow}"
                f"&fp=chrome&headerType=none&security=tls&sni={sni}&type=tcp"
                f"#{name}"
            )
            print(link)
        except AttributeError:
            # 如果某个块缺少参数，跳过不报错
            continue

if __name__ == "__main__":
    solve()
