
// Niri CRT Retro Shader
// 特性：掃描線、RGB 偏移、屏幕閃爍、暗角

void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    vec2 uv = v_texcoord;
    
    // 1. RGB 偏移 (模擬物理像素排列)
    float offset = 0.0015;
    float r = texture(u_tex, uv + vec2(offset, 0.0)).r;
    float g = texture(u_tex, uv).g;
    float b = texture(u_tex, uv - vec2(-offset, 0.0)).b;
    vec3 color = vec3(r, g, b);

    // 2. 掃描線 (Scanlines)
    // 數字 800.0 控制線條粗細，可根據你的分辨率調整
    float scanline = sin(uv.y * 1200.0) * 0.08 + 0.92;
    color *= scanline;

    // 3. 屏幕閃爍 (Flicker) - 模擬老電視不穩定的電壓
    // 使用 u_time 是 Niri 提供的內置時間變量
    float flicker = 1.0 + 0.005 * sin(u_time * 60.0);
    color *= flicker;

    // 4. 邊緣暗角 (Vignette)
    float vignette = uv.x * uv.y * (1.0 - uv.x) * (1.0 - uv.y);
    vignette = clamp(pow(16.0 * vignette, 0.1), 0.0, 1.0);
    color *= vignette;

    // 5. 略微提升亮度補償暗角
    color *= 1.1;

    fragColor = vec4(color, texture(u_tex, uv).a);
}
