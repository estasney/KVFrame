class ShaderTemplateMixin:
    FS_HEADER = '''
    #ifdef GL_ES
        precision highp float;
    #endif

    /* Outputs from the vertex shader */
    varying vec4 frag_color;
    varying vec2 tex_coord0;

    /* uniform texture samplers */
    uniform sampler2D texture0;
    uniform vec2 resolution;
    uniform float time;
    '''

    FS_FOOTER = '''
    void main (void){
    vec4 normal_color = frag_color * texture2D(texture0, tex_coord0);
    vec4 effect_color = effect(normal_color, texture0, tex_coord0,
                               gl_FragCoord.xy);
    gl_FragColor = effect_color;
    }'''

    VS_HEADER = '''
    #ifdef GL_ES
        precision highp float;
    #endif

    /* Outputs to the fragment shader */
    varying vec4 frag_color;
    varying vec2 tex_coord0;

    /* vertex attributes */
    attribute vec2     vPosition;
    attribute vec2     vTexCoords0;

    /* uniform variables */
    uniform mat4       modelview_mat;
    uniform mat4       projection_mat;
    uniform vec4       color;
    '''

    VS_FOOTER = '''
    void main (void) {
    frag_color = color;
    tex_coord0 = vTexCoords0;
    gl_Position = projection_mat * modelview_mat * vec4(vPosition.xy, 0.0, 1.0);
    }
'''
