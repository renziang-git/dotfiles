#version 110

uniform sampler2D u_tex;
varying vec2 v_texcoord;

void main() {
    vec4 color = texture2D(u_tex, v_texcoord);
    // 取平均值實現黑白效果
    float gray = dot(color.rgb, vec3(0.299, 0.587, 0.114));
    gl_FragColor = vec4(vec3(gray), color.a);
}
