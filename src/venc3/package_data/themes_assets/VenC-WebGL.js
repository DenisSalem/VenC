/*
 * Copyright 2016, 2025 Denis Salem
 * 
 * This file is part of VenC.
 * 
 * VenC is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.

 * VenC is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with VenC.  If not, see <http://www.gnu.org/licenses/>.
 */

// TODO : The following work as expected but the overall code is quite dirty in its internal structure and naming convention.

var VENC_WEB_GL = {
    version: "0.0.0",
    // Matrix related function are based on glMatrix.js
    mat4_create: function() {
        var matrix = new Float32Array(16);            
        matrix[0] = 1;
        matrix[5] = 1;
        matrix[10] = 1;
        matrix[15] = 1;
        return matrix;
    },
    mat4_perspective: function perspective(fovy, aspect, near, far) {
        var f = 1.0 / Math.tan(fovy / 2);
        
        var matrix = new Float32Array(16);                        
        matrix[0] = f / aspect;                
        matrix[5] = f;
        matrix[11] = -1;
      
        if (far != null && far !== Infinity) {
          var nf = 1 / (near - far);
          matrix[10] = (far + near) * nf;
          matrix[14] = 2 * far * near * nf;
        } else {
          matrix[10] = -1;
          matrix[14] = -2 * near;
        }
      
        return matrix;
    },
    mat4_translate: function (a, v) {
        var matrix = a.slice(0);            

        var x = v[0];
        var y = v[1];
        var z = v[2];
                      
        matrix[12] = a[0] * x + a[4] * y + a[8] * z + a[12];
        matrix[13] = a[1] * x + a[5] * y + a[9] * z + a[13];
        matrix[14] = a[2] * x + a[6] * y + a[10] * z + a[14];
        matrix[15] = a[3] * x + a[7] * y + a[11] * z + a[15];
      
        return matrix;
    },
    mat4_scale : function(a, v) {
        var matrix = a.slice(0);            

        var x = v[0];
        var y = v[1];
        var z = v[2];
      
        matrix[0] = a[0] * x;
        matrix[1] = a[1] * x;
        matrix[2] = a[2] * x;
        matrix[3] = a[3] * x;
        matrix[4] = a[4] * y;
        matrix[5] = a[5] * y;
        matrix[6] = a[6] * y;
        matrix[7] = a[7] * y;
        matrix[8] = a[8] * z;
        matrix[9] = a[9] * z;
        matrix[10] = a[10] * z;
        matrix[11] = a[11] * z;
      
        return matrix;
    },
    mat4_rotate: function rotate(a, rad, axis) {
      var matrix = a.slice(0);            

      var x = axis[0];
      var y = axis[1];
      var z = axis[2];
      
      var s = Math.sin(rad);
      var c = Math.cos(rad);
      var t = 1 - c;        
            
      var len = Math.hypot(x, y, z);
      if (len < 0.000001) {
        return a;
      }
                    
      let a00, a01, a02, a03;
      let a10, a11, a12, a13;
      let a20, a21, a22, a23;
    
      let b00, b01, b02;
      let b10, b11, b12;
      let b20, b21, b22;
    
      len = 1 / len;
    
      x *= len;
    
      y *= len;
    
      z *= len;
    
      a00 = a[0]; a01 = a[1]; a02 = a[2];  a03 = a[3]; 
      a10 = a[4]; a11 = a[5]; a12 = a[6];  a13 = a[7];
      a20 = a[8]; a21 = a[9]; a22 = a[10]; a23 = a[11];
    
      // Construct the elements of the rotation matrix
    
      b00 = x * x * t + c;
      b01 = y * x * t + z * s;
      b02 = z * x * t - y * s;
    
      b10 = x * y * t - z * s;
      b11 = y * y * t + c;
      b12 = z * y * t + x * s;
    
      b20 = x * z * t + y * s;
      b21 = y * z * t - x * s;
      b22 = z * z * t + c;
    
      // Perform rotation-specific matrix multiplication
    
      matrix[0] = a00 * b00 + a10 * b01 + a20 * b02;
      matrix[1] = a01 * b00 + a11 * b01 + a21 * b02;
      matrix[2] = a02 * b00 + a12 * b01 + a22 * b02;
      matrix[3] = a03 * b00 + a13 * b01 + a23 * b02;
      matrix[4] = a00 * b10 + a10 * b11 + a20 * b12;
      matrix[5] = a01 * b10 + a11 * b11 + a21 * b12;
      matrix[6] = a02 * b10 + a12 * b11 + a22 * b12;
      matrix[7] = a03 * b10 + a13 * b11 + a23 * b12;
      matrix[8] = a00 * b20 + a10 * b21 + a20 * b22;
      matrix[9] = a01 * b20 + a11 * b21 + a21 * b22;
      matrix[10] = a02 * b20 + a12 * b21 + a22 * b22;
      matrix[11] = a03 * b20 + a13 * b21 + a23 * b22;
    
      return matrix;
    },
    mat4_multiply: function(a, b) {
        var matrix = VENC_WEB_GL.mat4_create();;            
        
        let a00 = a[0],  a01 = a[1],  a02 = a[2],  a03 = a[3];
        let a10 = a[4],  a11 = a[5],  a12 = a[6],  a13 = a[7];
        let a20 = a[8],  a21 = a[9],  a22 = a[10], a23 = a[11];
        let a30 = a[12], a31 = a[13], a32 = a[14], a33 = a[15];
                      
        let b0 = b[0], b1 = b[1], b2 = b[2], b3 = b[3];
      
        matrix[0] = b0 * a00 + b1 * a10 + b2 * a20 + b3 * a30;
        matrix[1] = b0 * a01 + b1 * a11 + b2 * a21 + b3 * a31;
        matrix[2] = b0 * a02 + b1 * a12 + b2 * a22 + b3 * a32;
        matrix[3] = b0 * a03 + b1 * a13 + b2 * a23 + b3 * a33;
      
        b0 = b[4]; b1 = b[5]; b2 = b[6]; b3 = b[7];
      
        matrix[4] = b0 * a00 + b1 * a10 + b2 * a20 + b3 * a30;
        matrix[5] = b0 * a01 + b1 * a11 + b2 * a21 + b3 * a31;
        matrix[6] = b0 * a02 + b1 * a12 + b2 * a22 + b3 * a32;
        matrix[7] = b0 * a03 + b1 * a13 + b2 * a23 + b3 * a33;
      
        b0 = b[8]; b1 = b[9]; b2 = b[10]; b3 = b[11];
      
        matrix[8] = b0 * a00 + b1 * a10 + b2 * a20 + b3 * a30;
        matrix[9] = b0 * a01 + b1 * a11 + b2 * a21 + b3 * a31;
        matrix[10] = b0 * a02 + b1 * a12 + b2 * a22 + b3 * a32;
        matrix[11] = b0 * a03 + b1 * a13 + b2 * a23 + b3 * a33;
      
        b0 = b[12]; b1 = b[13]; b2 = b[14]; b3 = b[15];
      
        matrix[12] = b0 * a00 + b1 * a10 + b2 * a20 + b3 * a30;
        matrix[13] = b0 * a01 + b1 * a11 + b2 * a21 + b3 * a31;
        matrix[14] = b0 * a02 + b1 * a12 + b2 * a22 + b3 * a32;
        matrix[15] = b0 * a03 + b1 * a13 + b2 * a23 + b3 * a33;
      
        return matrix;
    },
    mat4_invert: function(a) {
      var matrix = VENC_WEB_GL.mat4_create();;            

      let a00 = a[0],  a01 = a[1],  a02 = a[2],  a03 = a[3];
      let a10 = a[4],  a11 = a[5],  a12 = a[6],  a13 = a[7];
      let a20 = a[8],  a21 = a[9],  a22 = a[10], a23 = a[11];
      let a30 = a[12], a31 = a[13], a32 = a[14], a33 = a[15];
    
      let b00 = a00 * a11 - a01 * a10;
      let b01 = a00 * a12 - a02 * a10;
      let b02 = a00 * a13 - a03 * a10;
      let b03 = a01 * a12 - a02 * a11;
      let b04 = a01 * a13 - a03 * a11;
      let b05 = a02 * a13 - a03 * a12;
      let b06 = a20 * a31 - a21 * a30;
      let b07 = a20 * a32 - a22 * a30;
      let b08 = a20 * a33 - a23 * a30;
      let b09 = a21 * a32 - a22 * a31;
      let b10 = a21 * a33 - a23 * a31;
      let b11 = a22 * a33 - a23 * a32;
    
      let det = b00 * b11 - b01 * b10 + b02 * b09 + b03 * b08 - b04 * b07 + b05 * b06;
    
      if (!det) {
        return null;
      }
    
      det = 1.0 / det;
    
      matrix[0] = (a11 * b11 - a12 * b10 + a13 * b09) * det;
      matrix[1] = (a02 * b10 - a01 * b11 - a03 * b09) * det;
      matrix[2] = (a31 * b05 - a32 * b04 + a33 * b03) * det;
      matrix[3] = (a22 * b04 - a21 * b05 - a23 * b03) * det;
      
      matrix[4] = (a12 * b08 - a10 * b11 - a13 * b07) * det;
      matrix[5] = (a00 * b11 - a02 * b08 + a03 * b07) * det;
      matrix[6] = (a32 * b02 - a30 * b05 - a33 * b01) * det;
      matrix[7] = (a20 * b05 - a22 * b02 + a23 * b01) * det;

      matrix[8] = (a10 * b10 - a11 * b08 + a13 * b06) * det;              
      matrix[9] = (a01 * b08 - a00 * b10 - a03 * b06) * det;
      matrix[10] = (a30 * b04 - a31 * b02 + a33 * b00) * det;
      matrix[11] = (a21 * b02 - a20 * b04 - a23 * b00) * det;
    
      matrix[12] = (a11 * b07 - a10 * b09 - a12 * b06) * det;
      matrix[13] = (a00 * b09 - a01 * b07 + a02 * b06) * det;
      matrix[14] = (a31 * b01 - a30 * b03 - a32 * b00) * det;
      matrix[15] = (a20 * b03 - a21 * b01 + a22 * b00) * det;
    
      return matrix;
    
    },
    mat4_transpose: function(a) {
        var matrix = a.slice(0);     
               
        let a01 = a[1], a02 = a[2], a03 = a[3];
        let a12 = a[6], a13 = a[7];
        let a23 = a[11];
    
        matrix[1] = a[4];
        matrix[2] = a[8];
        matrix[3] = a[12];
        matrix[4] = a01;
        matrix[6] = a[9];
        matrix[7] = a[13];
        matrix[8] = a02;
        matrix[9] = a12;
        matrix[11] = a[14];
        matrix[12] = a03;
        matrix[13] = a13;
        matrix[14] = a23;
        
        return matrix;
    },
    vertex_shader_source : `
        attribute vec3 vertex_position;
        attribute vec3 vertex_normal;

        uniform mat4 normal_matrix;
        uniform mat4 model_view_matrix;
        uniform mat4 projection_matrix;
        
        varying highp vec3 lighting;

        void main() {
            vec3 ambient_light = vec3(0.25, 0.25, 0.25);
            vec3 directional_light_color = vec3(0.75, 0.75, 0.75);
            vec3 directional_vector = normalize(vec3(1, 1, 1));
            
            vec4 transformed_normal = normal_matrix * vec4(vertex_normal, 1.0);

            float directional = max(dot(transformed_normal.xyz, directional_vector), 0.0);
            
            lighting = ambient_light + (directional_light_color * directional);
        
            gl_Position = projection_matrix *  model_view_matrix * vec4(vertex_position,1.0);
        }
    `,
    fragment_shader_source : `
        varying highp vec3 lighting;

        void main() {
          gl_FragColor = vec4(lighting.rgb, 1.0);
        }
    `,
    touch_start: function(e) {
        this.VENC_WEB_GL_CONTEXT.tracking = true;
        if (e.touches.length === 1) {
            this.VENC_WEB_GL_CONTEXT.touch_motions = {
                touch: true,
                start: {
                    x: e.touches[0].clientX,
                    y: e.touches[0].clientY,
                },
            };
            e.preventDefault();
        } else if (e.touches.length === 2){
            X = e.touches[0].clientX - e.touches[1].clientX;
            Y = e.touches[0].clientY - e.touches[1].clientY;
            this.VENC_WEB_GL_CONTEXT.touch_motions.pinch_start = Math.sqrt(X*X + Y*Y);
            e.preventDefault();
        }
    },                                                
    touch_move: function(e) {
        if (e.touches.length === 1) {
            this.VENC_WEB_GL_CONTEXT.mouse_motions.current_x -= (this.VENC_WEB_GL_CONTEXT.touch_motions.start.x - e.touches[0].clientX)*0.01;
            this.VENC_WEB_GL_CONTEXT.mouse_motions.current_y -= (this.VENC_WEB_GL_CONTEXT.touch_motions.start.y - e.touches[0].clientY)*0.01;
            this.VENC_WEB_GL_CONTEXT.touch_motions.start.x = e.touches[0].clientX;
            this.VENC_WEB_GL_CONTEXT.touch_motions.start.y = e.touches[0].clientY;
            e.preventDefault();
        } else if (e.touches.length >= 2) {
            X = e.touches[0].clientX - e.touches[1].clientX;
            Y = e.touches[0].clientY - e.touches[1].clientY;
            len = Math.sqrt(X*X + Y*Y);
            
            ratio = Math.abs(len / this.VENC_WEB_GL_CONTEXT.touch_motions.pinch_start);
            if (ratio > 1) {
                this.VENC_WEB_GL_CONTEXT.scale_ratio *= 1.02;
                this.VENC_WEB_GL_CONTEXT.touch_motions.pinch_start = len; 
            }
            else if (ratio < 1) {
                this.VENC_WEB_GL_CONTEXT.scale_ratio *= 0.98;
                this.VENC_WEB_GL_CONTEXT.touch_motions.pinch_start = len;
            }
            if (this.VENC_WEB_GL_CONTEXT.scale_ratio < canvas.VENC_WEB_GL_CONTEXT.min_scale_ratio) {
                this.VENC_WEB_GL_CONTEXT.scale_ratio = canvas.VENC_WEB_GL_CONTEXT.min_scale_ratio;
            }
            e.preventDefault();

        }
        return false;
    },
    touch_end: function(e) {
      if (e.touches.length === 0 ) {
          this.VENC_WEB_GL_CONTEXT.tracking = false;
          this.VENC_WEB_GL_CONTEXT.touch_motions.touch = false;
          this.VENC_WEB_GL_CONTEXT.mouse_motions = {
              current_x : 0,
              current_y : 0,
              base_x: (this.VENC_WEB_GL_CONTEXT.mouse_motions.base_x + this.VENC_WEB_GL_CONTEXT.mouse_motions.current_x) % (2*3.141592),
              base_y: (this.VENC_WEB_GL_CONTEXT.mouse_motions.base_y + this.VENC_WEB_GL_CONTEXT.mouse_motions.current_y) % (2*3.141592)
          };
      } else if (e.touches.length === 1){
            this.VENC_WEB_GL_CONTEXT.touch_motions.start.x = e.touches[0].clientX;
            this.VENC_WEB_GL_CONTEXT.touch_motions.start.y = e.touches[0].clientY;
      }
    },
    init_shader_program : function(gl) {
        const vertex_shader = this.load_shader(gl, gl.VERTEX_SHADER, this.vertex_shader_source);
        const fragment_shader = this.load_shader(gl, gl.FRAGMENT_SHADER, this.fragment_shader_source);
            
        const shader_program = gl.createProgram();
        gl.attachShader(shader_program, vertex_shader);
        gl.attachShader(shader_program, fragment_shader);
        gl.linkProgram(shader_program);
  
        if (!gl.getProgramParameter(shader_program, gl.LINK_STATUS)) {
            console.log("VenC: gl.getProgramParameter(shaderProgram, gl.LINK_STATUS) has failed with the following message:\n"+gl.getProgramInfoLog(shader_program));
            return null;
        }
  
        return shader_program;
    },
    load_shader : function(gl, type, source) {
        const shader = gl.createShader(type);
        gl.shaderSource(shader, source);
        gl.compileShader(shader);
              
        if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
            console.log("VenC: gl.getShaderParameter(shader, gl.COMPILE_STATUS) has failed with the following message:\n"+ gl.getShaderInfoLog(shader));
            gl.deleteShader(shader);
            return null;
        }
    
        return shader;
    },
    init: function(canvas, mesh_url) {
        canvas.VENC_WEB_GL_CONTEXT = {
          gl: canvas.getContext("webgl"),
          rotation_x: 0,
          rotation_y: 0,
          mesh : {
              positions : [],
              normals : []
          },
          ready: false,
          mesh_url: mesh_url
        };
        
        if (!canvas.VENC_WEB_GL_CONTEXT.gl) {
            console.log("VenC: Cannot initialize WebGL.");
            return null;
        }
        
        canvas.VENC_WEB_GL_CONTEXT.tracking = false;
        canvas.VENC_WEB_GL_CONTEXT.mouse_motions = {
            current_x : 0,
            current_y : 0,
            base_x: 0,
            base_y: 0
        };
        
        canvas.VENC_WEB_GL_CONTEXT.touch_motions = {
            touch: false,
            touch_start: {x: 0, y: 0},
            pinch_start: {x: 0, y: 0}
        };
        
        canvas.addEventListener('touchstart', VENC_WEB_GL.touch_start, false);        
        canvas.addEventListener('touchmove',  VENC_WEB_GL.touch_move,  false);        
        canvas.addEventListener('touchend',   VENC_WEB_GL.touch_end,   false);
    
        canvas.VENC_WEB_GL_CONTEXT.mouseup_callback = function(event) {
                this.VENC_WEB_GL_CONTEXT.tracking = false;
                this.VENC_WEB_GL_CONTEXT.mouse_motions = {
                    current_x : 0,
                    current_y : 0,
                    base_x: (this.VENC_WEB_GL_CONTEXT.mouse_motions.base_x + this.VENC_WEB_GL_CONTEXT.mouse_motions.current_x) % (2*3.141592),
                    base_y: (this.VENC_WEB_GL_CONTEXT.mouse_motions.base_y + this.VENC_WEB_GL_CONTEXT.mouse_motions.current_y) % (2*3.141592)
                };
        };
        
        canvas.addEventListener('mouseup', canvas.VENC_WEB_GL_CONTEXT.mouseup_callback);
        
        canvas.VENC_WEB_GL_CONTEXT.mousedown_callback = function(event) {
                this.VENC_WEB_GL_CONTEXT.tracking = true;
        };
        
        canvas.addEventListener('mousedown', canvas.VENC_WEB_GL_CONTEXT.mousedown_callback);

        canvas.VENC_WEB_GL_CONTEXT.mousemove_callback = function(event) {
                if (this.VENC_WEB_GL_CONTEXT.tracking) {
                    this.VENC_WEB_GL_CONTEXT.mouse_motions.current_x += event.movementX*0.05;
                    this.VENC_WEB_GL_CONTEXT.mouse_motions.current_y += event.movementY*0.05;
                }
        };
        canvas.addEventListener('mousemove', canvas.VENC_WEB_GL_CONTEXT.mousemove_callback);
        
        canvas.VENC_WEB_GL_CONTEXT.wheel_callback = function(event) {
            this.VENC_WEB_GL_CONTEXT.scale_ratio += event.deltaY * -0.000001;
            event.preventDefault();
        };
        canvas.addEventListener("wheel", canvas.VENC_WEB_GL_CONTEXT.wheel_callback, false);
                          
        var query = new XMLHttpRequest();        
        query.VENC_WEB_GL_CONTEXT = canvas.VENC_WEB_GL_CONTEXT;
        query.open("GET", mesh_url);
        query.responseType = "arraybuffer";
        query.onreadystatechange = function(e) {
            if (this.readyState == 4) {
                var array_buffer = query.response;
                var byte_array = new Uint8Array(array_buffer);
                triangles_count =
                    byte_array[80] +
                    (byte_array[81] << 8 ) +
                    (byte_array[82] << 16) +
                    (byte_array[83] << 24);

                console.log("VenC: WebGL: "+mesh_url+" is "+byte_array.length.toString()+" bytes.");                          
                console.log("VenC: WebGL: "+mesh_url+" has "+triangles_count.toString()+" triangles.");
                
                for (i = 84; i < byte_array.length; i+=50) {
                    // Duplicate each normal for each vertex
                    for (var j = 0; j < 3; j++) { 
                        this.VENC_WEB_GL_CONTEXT.mesh.normals.push(new DataView(byte_array.slice(i,i+4).reverse().buffer).getFloat32(0));
                        this.VENC_WEB_GL_CONTEXT.mesh.normals.push(new DataView(byte_array.slice(i+4,i+8).reverse().buffer).getFloat32(0));
                        this.VENC_WEB_GL_CONTEXT.mesh.normals.push(new DataView(byte_array.slice(i+8,i+12).reverse().buffer).getFloat32(0));
                    }
                    
                    this.VENC_WEB_GL_CONTEXT.mesh.positions.push(new DataView(byte_array.slice(i+12,i+16).reverse().buffer).getFloat32(0));
                    this.VENC_WEB_GL_CONTEXT.mesh.positions.push(new DataView(byte_array.slice(i+16,i+20).reverse().buffer).getFloat32(0));
                    this.VENC_WEB_GL_CONTEXT.mesh.positions.push(new DataView(byte_array.slice(i+20,i+24).reverse().buffer).getFloat32(0));
                    
                    this.VENC_WEB_GL_CONTEXT.mesh.positions.push(new DataView(byte_array.slice(i+24,i+28).reverse().buffer).getFloat32(0));
                    this.VENC_WEB_GL_CONTEXT.mesh.positions.push(new DataView(byte_array.slice(i+28,i+32).reverse().buffer).getFloat32(0));
                    this.VENC_WEB_GL_CONTEXT.mesh.positions.push(new DataView(byte_array.slice(i+32,i+36).reverse().buffer).getFloat32(0));
                    
                    this.VENC_WEB_GL_CONTEXT.mesh.positions.push(new DataView(byte_array.slice(i+36,i+40).reverse().buffer).getFloat32(0));
                    this.VENC_WEB_GL_CONTEXT.mesh.positions.push(new DataView(byte_array.slice(i+40,i+44).reverse().buffer).getFloat32(0));
                    this.VENC_WEB_GL_CONTEXT.mesh.positions.push(new DataView(byte_array.slice(i+44,i+48).reverse().buffer).getFloat32(0));
                }
                
                this.VENC_WEB_GL_CONTEXT.shader_program = VENC_WEB_GL.init_shader_program(this.VENC_WEB_GL_CONTEXT.gl);
                
                this.VENC_WEB_GL_CONTEXT.program_info = {
                    attributes_locations: {
                      vertex_position: this.VENC_WEB_GL_CONTEXT.gl.getAttribLocation(this.VENC_WEB_GL_CONTEXT.shader_program, "vertex_position"),
                      normal: this.VENC_WEB_GL_CONTEXT.gl.getAttribLocation(this.VENC_WEB_GL_CONTEXT.shader_program, "vertex_normal"),
                    },
                    uniform_locations: {
                      projection_matrix: this.VENC_WEB_GL_CONTEXT.gl.getUniformLocation(this.VENC_WEB_GL_CONTEXT.shader_program, "projection_matrix"),
                      model_view_matrix: this.VENC_WEB_GL_CONTEXT.gl.getUniformLocation(this.VENC_WEB_GL_CONTEXT.shader_program, "model_view_matrix"),
                      normal_matrix:     this.VENC_WEB_GL_CONTEXT.gl.getUniformLocation(this.VENC_WEB_GL_CONTEXT.shader_program, "normal_matrix")
                    }
                };

                const normal_buffer = this.VENC_WEB_GL_CONTEXT.gl.createBuffer();
                const position_buffer = this.VENC_WEB_GL_CONTEXT.gl.createBuffer();
              
                this.VENC_WEB_GL_CONTEXT.gl.bindBuffer(this.VENC_WEB_GL_CONTEXT.gl.ARRAY_BUFFER, position_buffer);
                this.VENC_WEB_GL_CONTEXT.gl.bufferData(this.VENC_WEB_GL_CONTEXT.gl.ARRAY_BUFFER, new Float32Array(this.VENC_WEB_GL_CONTEXT.mesh.positions), this.VENC_WEB_GL_CONTEXT.gl.STATIC_DRAW);
                
                this.VENC_WEB_GL_CONTEXT.gl.bindBuffer(this.VENC_WEB_GL_CONTEXT.gl.ARRAY_BUFFER, normal_buffer);
                this.VENC_WEB_GL_CONTEXT.gl.bufferData(this.VENC_WEB_GL_CONTEXT.gl.ARRAY_BUFFER, new Float32Array(this.VENC_WEB_GL_CONTEXT.mesh.normals), this.VENC_WEB_GL_CONTEXT.gl.STATIC_DRAW);
                
                this.VENC_WEB_GL_CONTEXT.buffers =  {
                    vertex_count: this.VENC_WEB_GL_CONTEXT.mesh.positions.length / 3,
                    position: position_buffer,
                    normal: normal_buffer
                };
                
                x_positions = [];
                y_positions = [];
                z_positions = [];
                
                for (var i = 0; i< this.VENC_WEB_GL_CONTEXT.mesh.positions.length; i+=3) {
                    x_positions.push(this.VENC_WEB_GL_CONTEXT.mesh.positions[i]);
                    y_positions.push(this.VENC_WEB_GL_CONTEXT.mesh.positions[i+1]);
                    z_positions.push(this.VENC_WEB_GL_CONTEXT.mesh.positions[i+2]);
                }                         
                
                x_max = Math.max.apply(Math, x_positions); x_min = Math.min.apply(Math, x_positions);
                y_max = Math.max.apply(Math, y_positions); y_min = Math.min.apply(Math, y_positions); 
                z_max = Math.max.apply(Math, z_positions); z_min = Math.min.apply(Math, z_positions); 

                canvas.VENC_WEB_GL_CONTEXT.scale_ratio = 1 / Math.max(
                    x_max - x_min,
                    y_max - y_min,
                    z_max - z_min
                );
                
                canvas.VENC_WEB_GL_CONTEXT.min_scale_ratio = canvas.VENC_WEB_GL_CONTEXT.min_scale_ratio / 100;
                
                this.VENC_WEB_GL_CONTEXT.offset_x = (x_max + x_min ) / 2;
                this.VENC_WEB_GL_CONTEXT.offset_y = (y_max + y_min ) / 2;
                this.VENC_WEB_GL_CONTEXT.offset_z = (z_max + z_min ) / 2;
      
                this.VENC_WEB_GL_CONTEXT.mesh.normals = [];
                this.VENC_WEB_GL_CONTEXT.mesh.positions = [];
                this.VENC_WEB_GL_CONTEXT.ready = true;
            }
        };
         
        query.send(); 

        canvas.VENC_WEB_GL_CONTEXT.rendering_loop = setInterval(VENC_WEB_GL.render, 20,  canvas.VENC_WEB_GL_CONTEXT);

        return canvas.VENC_WEB_GL_CONTEXT;
    },
    draw_scene: function(context, buffers) {
        context.gl.clearDepth(1.0);
        context.gl.enable(context.gl.DEPTH_TEST);
        context.gl.depthFunc(context.gl.LEQUAL);

        context.gl.clearColor(0.0, 0.0, 0.0, 0.0);           
        context.gl.clear(context.gl.COLOR_BUFFER_BIT | context.gl.DEPTH_BUFFER_BIT);
      
        const field_of_view = (45 * Math.PI) / 180; // en radians
        const aspect = context.gl.canvas.clientWidth / context.gl.canvas.clientHeight;
        const z_near = 0.1;
        const z_far = 1000.0;
        const projection_matrix = VENC_WEB_GL.mat4_perspective(field_of_view, aspect, z_near, z_far);

        model_matrix = VENC_WEB_GL.mat4_translate(
            VENC_WEB_GL.mat4_create(),
            [
              -context.offset_x*context.scale_ratio,
              -context.offset_y*context.scale_ratio,
              -context.offset_z*context.scale_ratio
            ]
        );
        
        model_matrix = VENC_WEB_GL.mat4_scale(
            model_matrix,
            [
              context.scale_ratio,
              context.scale_ratio,
              context.scale_ratio
            ]
        );

        view_matrix = VENC_WEB_GL.mat4_translate(
            VENC_WEB_GL.mat4_create(), 
            [
              0,
              0,
              -1.5
            ]
        );
        
        view_matrix = VENC_WEB_GL.mat4_rotate(
            view_matrix,
            context.mouse_motions.base_y,
            [1, 0, 0],
        );
        
        view_matrix = VENC_WEB_GL.mat4_rotate(
            view_matrix,
            context.mouse_motions.base_x,
            [0, 1, 0]
        );
        
        model_view_matrix = VENC_WEB_GL.mat4_multiply(view_matrix, model_matrix);
        
        var normal_matrix = VENC_WEB_GL.mat4_transpose(
            VENC_WEB_GL.mat4_invert(view_matrix)
        );
        
        context.gl.useProgram(context.shader_program);
                      
        context.gl.uniformMatrix4fv(
            context.program_info.uniform_locations.projection_matrix,
            false,
            projection_matrix,
        );
        
        context.gl.uniformMatrix4fv(
            context.program_info.uniform_locations.model_view_matrix,
            false,
            model_view_matrix,
        );
        
        context.gl.uniformMatrix4fv(
          context.program_info.uniform_locations.normal_matrix,
          false,
          new Float32Array(normal_matrix)
        );

        context.gl.bindBuffer(context.gl.ARRAY_BUFFER, context.buffers.position);
        context.gl.vertexAttribPointer(
            context.program_info.attributes_locations.vertex_position,
            3, // components count
            context.gl.FLOAT, // type
            false, // normalize
            0, // stride
            0, // offset
        );
        
        context.gl.enableVertexAttribArray(context.program_info.attributes_locations.vertex_position);

        context.gl.bindBuffer(context.gl.ARRAY_BUFFER, context.buffers.normal);
        context.gl.vertexAttribPointer(
            context.program_info.attributes_locations.normal,
            3, // components count
            context.gl.FLOAT, // type
            false, // normalize
            0, // stride
            0, // offset
        );
        
        context.gl.enableVertexAttribArray(context.program_info.attributes_locations.normal);
        
        context.gl.drawArrays(
            context.gl.TRIANGLES,
            0, // offset
            context.buffers.vertex_count, // vertex count
        );
    },
    render: function(context) {
        if (context.ready) {
            context.mouse_motions = {
                current_x : 0,
                current_y : 0,
                base_x: (context.mouse_motions.base_x + context.mouse_motions.current_x) % (2*3.141592),
                base_y: (context.mouse_motions.base_y + context.mouse_motions.current_y) % (2*3.141592)
            };
            VENC_WEB_GL.draw_scene(context);
        }
        else {
            console.log("VenC: WebGL: Mesh", context.mesh_url, "is not ready.");
        }
    }
};


function VENC_WEB_GL_ADD_NEW_CANVAS() {
    nodes = document.evaluate('//*[@data-venc-webgl-mesh]', document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);    
    for (var i = 0; i < nodes.snapshotLength; i++) {
        node = nodes.snapshotItem(i)
        if (! ("VENC_WEB_GL_CONTEXT" in node)) {
            VENC_WEB_GL.init(node, node.dataset.vencWebglMesh);
        }
    }
}

function VENC_WEB_GL_ON_LOAD() {
    VENC_WEB_GL.timer = setInterval(VENC_WEB_GL_ADD_NEW_CANVAS, 250);
}

if (! typeof VENC_SCRIPT_BOOTSTRAP === 'undefined') {
    VENC_SCRIPT_BOOTSTRAP.callbacks_register.push(VENC_WEB_GL_ON_LOAD);
}
